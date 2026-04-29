import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import apiClient from "../services/apiClient";

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("demo@agentforge.ai");
  const [password, setPassword] = useState("password");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");
    setSubmitting(true);
    try {
      const response = await apiClient.post("/auth/login", { email, password });
      sessionStorage.setItem("agentforge_token", response.data.access_token);
      setMessage("Access granted. Routing you to the lab…");
      setTimeout(() => navigate("/dashboard"), 700);
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Authentication failed. Verify credentials.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="auth-card" aria-labelledby="login-title">
      <div className="auth-card__crest" aria-hidden="true">AF</div>
      <h2 id="login-title">Enter the Lab</h2>
      <p className="auth-tagline">Authenticate to summon your research crew.</p>

      <div style={{ display: "grid", placeItems: "center" }}>
        <span className="demo-creds">Demo access pre-filled</span>
      </div>

      <form className="form-grid" onSubmit={handleLogin}>
        <label>
          Email
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            autoComplete="email"
            required
          />
        </label>
        <label>
          Access Cipher
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            autoComplete="current-password"
            required
          />
        </label>
        <button className="btn-primary" type="submit" disabled={submitting}>
          {submitting ? "Authenticating…" : "Initiate Session"}
        </button>
      </form>

      {message && <div className="banner banner--success">{message}</div>}
      {error && <div className="banner banner--error">{error}</div>}

      <p className="auth-foot">
        New scientist? <Link to="/register">Forge a profile →</Link>
      </p>
    </section>
  );
}

export default LoginPage;
