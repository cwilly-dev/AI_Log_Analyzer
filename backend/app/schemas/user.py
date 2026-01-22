from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64)

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
