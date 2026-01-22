import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register, loginJson } from "../api/auth";

export default function SignupPage() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== password2) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setSubmitting(true);
    try {
      await register(email, password);

      await loginJson(email, password);

      setSuccess("Account created! You are now signed in.");
      nav("/dashboard")
//       setTimeout(() => nav("/login"), 600);
    } catch (err) {
      const detail = err?.response?.data?.detail;

      const msg =
        typeof detail === "string"
          ? detail
          : err?.message || "Sign up failed.";

      setError(msg);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-root">
      <div className="auth-bg" />

      <div className="auth-card">

        <h1 className="auth-title">Sign Up</h1>
        <p className="auth-subtitle">Create your account</p>

        <form onSubmit={onSubmit} className="auth-form">
          <label className="auth-label">
            Email (Username)
            <input
              className="auth-input"
              type="email"
              autoComplete="username"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              required
            />
          </label>

          <label className="auth-label">
            Password
            <input
              className="auth-input"
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </label>

          <label className="auth-label">
            Confirm Password
            <input
              className="auth-input"
              type="password"
              autoComplete="new-password"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              placeholder="••••••••"
              required
            />
          </label>

          {error ? <div className="auth-error">{error}</div> : null}
          {success ? <div className="auth-success">{success}</div> : null}

          <button className="auth-button" type="submit" disabled={submitting}>
            {submitting ? "Creating..." : "Create Account"}
          </button>

          <div className="auth-footer">
            <span>Already have an account?</span>
            <button type="button" className="auth-link" onClick={() => nav("/login")}>
              Sign In
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
