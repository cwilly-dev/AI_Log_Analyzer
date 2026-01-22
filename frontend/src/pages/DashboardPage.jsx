import React, { useEffect, useMemo, useState } from "react";
import { listMyLogs, createLogRaw, analyzeLog, createAndAnalyzeLogRaw, getLogAnalysis, deleteLog} from "../api/logs";

function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleString();
}

function formatConfidence(confidence) {
    if (confidence == null || confidence === undefined) return "-";
    return `${Math.round(confidence * 100)}%`;
}

function capitalizeString(string) {
    if (!string) return "";
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export default function DashboardPage() {
  const [logs, setLogs] = useState([]);
  const [selectedLogId, setSelectedLogId] = useState(null);

  const [draft, setDraft] = useState("");
  const [loadingList, setLoadingList] = useState(false);
  const [busy, setBusy] = useState(false);

  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");

  const selectedLog = useMemo(
    () => logs.find((l) => l.id === selectedLogId) || null,
    [logs, selectedLogId]
  );

  async function refreshLogs(selectFirst = false) {
    setLoadingList(true);
    setError("");
    try {
      const data = await listMyLogs();
      setLogs(data);

      if (selectFirst && data?.length) {
        setSelectedLogId(data[0].id);
      }
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Failed to load logs.");
    } finally {
      setLoadingList(false);
    }
  }

  useEffect(() => {
    refreshLogs(true);
  }, []);

  async function onCreateLog() {
    setError("");
    setAnalysis(null);
    if (!draft.trim()) {
      setError("Paste a log first.");
      return;
    }

    setBusy(true);
    try {
      const log = await createLogRaw(draft);
      await refreshLogs();
      setSelectedLogId(log.id);
      setDraft("");
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Failed to create log.");
    } finally {
      setBusy(false);
    }
  }

  async function onCreateAndAnalyze() {
    setError("");
    setAnalysis(null);
    if (!draft.trim()) {
      setError("Paste a log first.");
      return;
    }

    setBusy(true);
    try {
      const analysisRes = await createAndAnalyzeLogRaw(draft);
      setAnalysis(analysisRes);
      setDraft("");
      await refreshLogs(true);
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Failed to analyze log.");
    } finally {
      setBusy(false);
    }
  }

  async function onAnalyzeSelected() {
    setError("");
    setAnalysis(null);
    if (!selectedLogId) {
      setError("Select a log first.");
      return;
    }

    setBusy(true);
    try {
      const analysisRes = await analyzeLog(selectedLogId);
      setAnalysis(analysisRes);
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Failed to analyze log.");
    } finally {
      setBusy(false);
    }
  }

  async function onDeleteSelected() {
      if (!selectedLogId) return;

      const confirmed = window.confirm(
        `Delete Log #${selectedLogId}? This cannot be undone.`
      );
      if (!confirmed) return;

      setBusy(true);
      setError("");
      setAnalysis(null);

      try {
        await deleteLog(selectedLogId);

        setLogs((prev) => prev.filter((l) => l.id !== selectedLogId));

        setSelectedLogId(null);
      } catch (err) {
        setError(
          err?.response?.data?.detail ||
          err?.message ||
          "Failed to delete log."
        );
      } finally {
        setBusy(false);
      }
  }

  function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  }

  return (
    <div className="dash-root">
      <div className="dash-topbar">
        <div className="dash-brand">
          <div className="dash-dot" />
          <div>
            <div className="dash-title">AI System Log Analyzer</div>
            <div className="dash-subtitle">Paste logs • analyze • store results</div>
          </div>
        </div>

        <button className="dash-ghost" onClick={logout}>
          Log out
        </button>
      </div>

      <div className="dash-grid">
        {/* LEFT: create */}
        <div className="dash-card">
          <div className="dash-card-header">
            <div className="dash-card-title">New Log</div>
            <div className="dash-card-hint">Paste raw text (multiline supported)</div>
          </div>

          <textarea
            className="dash-textarea"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            placeholder="Paste your system log here..."
          />

          {error ? <div className="auth-error">{error}</div> : null}

          <div className="dash-actions">
            <button className="dash-button" disabled={busy} onClick={onCreateLog}>
              {busy ? "Working..." : "Save Log"}
            </button>
            <button className="dash-button dash-button-secondary" disabled={busy} onClick={onCreateAndAnalyze}>
              {busy ? "Working..." : "Save & Analyze"}
            </button>
          </div>

          <div className="dash-divider" />

          <div className="dash-card-header" style={{ marginTop: 6 }}>
            <div className="dash-card-title">Analyze Selected</div>
            <div className="dash-card-hint">Runs AI analysis on a stored log</div>
          </div>

          <button className="dash-button" disabled={busy || !selectedLogId} onClick={onAnalyzeSelected}>
            {busy ? "Analyzing..." : "Analyze Selected Log"}
          </button>
        </div>

        <div className="dash-card">
          <div className="dash-card-header">
            <div className="dash-card-title">My Logs</div>
            <div className="dash-card-hint">
              {loadingList ? "Loading..." : `${logs.length} total`}
            </div>
          </div>

          <div className="dash-list">
            {logs.map((l) => (
              <button
                key={l.id}
                className={`dash-list-item ${l.id === selectedLogId ? "active" : ""}`}
                onClick={async () => {
                  setSelectedLogId(l.id);
                  setError("");
                  setAnalysis(null);

                  try {
                    const a = await getLogAnalysis(l.id);
                    setAnalysis(a);
                  } catch (err) {
                    const status = err?.response?.status;
                    if (status !== 404) {
                      setError(err?.response?.data?.detail || err?.message || "Failed to load analysis.");
                    }
                  }
                }}
                type="button"
              >
                <div className="dash-list-row">
                  <div className="dash-list-id">Log #{l.id}</div>
                  <div className="dash-list-date">{formatDate(l.created_at)}</div>
                </div>
                <div className="dash-list-preview">
                  {(l.content || "").slice(0, 140)}
                  {(l.content || "").length > 140 ? "…" : ""}
                </div>
              </button>
            ))}

            {!logs.length && !loadingList ? (
              <div className="dash-empty">No logs yet. Paste one on the left to get started.</div>
            ) : null}
          </div>

          {selectedLog ? (
            <>
              <div className="dash-divider" />

              <div className="dash-card-header">
                <div className="dash-card-title">Selected Log</div>
                <div className="dash-card-hint">Full text</div>
              </div>

              <pre className="dash-pre">{selectedLog.content}</pre>
              <div style={{ marginTop: 12, display: "flex", justifyContent: "flex-end" }}>
                  <button type="button" className="dash-button dash-button-danger" disabled={busy || !selectedLogId} onClick={onDeleteSelected}>
                    Delete Log
                  </button>
                </div>
            </>
          ) : null}
        </div>

        <div className="dash-card dash-wide">
          <div className="dash-card-header">
            <div className="dash-card-title">Analysis</div>
            <div className="dash-card-hint">
              {analysis ? "Latest result" : "Run analysis to see results here"}
            </div>
          </div>

          {analysis ? (
            <div className="dash-analysis">
              <div className="dash-pill">
                Risk: <strong>{capitalizeString(analysis.risk_level)}</strong>
              </div>
              <div className="dash-pill">
                Immediate: <strong>{capitalizeString(String(analysis.requires_immediate_attention))}</strong>
              </div>
              <div className="dash-pill">
                Confidence: <strong>{formatConfidence(analysis.confidence)}</strong>
              </div>

              <div className="dash-analysis-grid">
                <div>
                  <div className="dash-k">Summary</div>
                  <div className="dash-v">{analysis.summary}</div>
                </div>
                <div>
                  <div className="dash-k">Root Cause</div>
                  <div className="dash-v">{analysis.root_cause}</div>
                </div>
                <div>
                  <div className="dash-k">Recommended Next Steps</div>
                  <ul className="dash-ul">
                    {(analysis.recommended_next_steps || []).map((s, idx) => (
                      <li key={idx}>{s}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="dash-divider" />

              <div className="dash-k">Raw JSON</div>
              <pre className="dash-pre">{JSON.stringify(analysis, null, 2)}</pre>
            </div>
          ) : (
            <div className="dash-empty">
              No analysis yet. Use <strong>Save & Analyze</strong> or analyze a stored log.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
