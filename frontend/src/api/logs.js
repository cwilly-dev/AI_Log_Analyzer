import api from "./axios";

export async function createLogRaw(content) {
  const res = await api.post("/logs/raw", content, {
    headers: { "Content-Type": "text/plain" },
  });
  return res.data;
}

export async function createAndAnalyzeLogRaw(content) {
  const res = await api.post("/logs/raw/analyze", content, {
    headers: { "Content-Type": "text/plain" },
  });
  return res.data;
}

export async function listMyLogs() {
  const res = await api.get("/logs/");
  return res.data;
}

export async function analyzeLog(logId) {
  const res = await api.post(`/logs/${logId}/analyze`);
  return res.data;
}

export async function getLogAnalysis(logId) {
  const res = await api.get(`/logs/${logId}/analysis`);
  return res.data;
}

export async function deleteLog(logId) {
  await api.delete(`/logs/${logId}/`);
}