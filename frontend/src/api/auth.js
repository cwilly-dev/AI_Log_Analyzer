import api from "./axios";

export async function loginJson(email, password) {
  const res = await api.post("/auth/login-json", { email, password });
  const { access_token } = res.data;
  localStorage.setItem("access_token", access_token);
  return res.data;
}

export async function register(email, password) {
  const res = await api.post("/auth/register", { email, password });
  return res.data;
}