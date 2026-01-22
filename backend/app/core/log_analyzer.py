
from app.core.config import settings
from app.models.log import LogAnalysis
from app.schemas.log_analysis import LogAnalysisResponse
from app.utils.prompts import AI_PROMPT
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_xai import ChatXAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import re

class LogAnalyzer:
    @classmethod
    def _get_llm(cls):
        return ChatGoogleGenerativeAI(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL)

    @classmethod
    def analyze_log(cls, db: Session, log_id: int, log_text: str) -> LogAnalysis:
        llm = cls._get_llm()
        log_parser = PydanticOutputParser(pydantic_object=LogAnalysisResponse)

        prompt = ChatPromptTemplate.from_messages([
            ("system", AI_PROMPT),
            ("human", "{log_text}"),
        ]).partial(
            format_instructions=log_parser.get_format_instructions()
        )
        messages = prompt.format_prompt(log_text=log_text).to_messages()
        raw_response = llm.invoke(messages)

        response_text = extract_json(_as_text(raw_response))

        parsed: LogAnalysisResponse = log_parser.parse(response_text)

        analysis = LogAnalysis(
            log_id=log_id,
            summary=parsed.summary,
            root_cause=parsed.root_cause,
            has_error=parsed.has_error,
            risk_level=parsed.risk_level,
            requires_immediate_attention=parsed.requires_immediate_attention,
            recommended_next_steps=parsed.recommended_next_steps,
            confidence=parsed.confidence,
            raw_response=response_text,
        )

        db.add(analysis)

        return analysis

def extract_json(text: str) -> str:
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    return match.group(0) if match else text

def _as_text(raw_response) -> str:
    if hasattr(raw_response, "content"):
        content = raw_response.content
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    parts.append(item["text"])
                else:
                    parts.append(str(item))
            return "\n".join(parts)
        return str(content)
    return str(raw_response)