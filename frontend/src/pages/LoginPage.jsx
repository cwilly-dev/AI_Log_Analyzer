import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginJson } from "../api/auth";

export default function LoginPage() {
  const nav = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      await loginJson(username, password);
      nav("/dashboard")
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Login failed. Check credentials.";
      setError(typeof msg === "string" ? msg : "Login failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-root">


      <div className="auth-hero">
        <h1 className="auth-hero-title">AI System Log Analyzer</h1>
      </div>

      <div className="auth-card">


        <h1 className="auth-title">Sign In</h1>
        <p className="auth-subtitle">Access your account</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label className="auth-label">
            Username
            <input
              className="auth-input"
              type="text"
              autoComplete="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>

          <label className="auth-label">
            Password
            <input
              className="auth-input"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </label>

          {error ? <div className="auth-error">{error}</div> : null}

          <button className="auth-button" type="submit" disabled={submitting}>
            {submitting ? "Signing in..." : "Sign In"}
          </button>

          <div className="auth-footer">
            <span>Don&apos;t have an account?</span>
            <button
              type="button"
              className="auth-link"
              onClick={() => nav("/signup")}
            >
              Sign Up
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}