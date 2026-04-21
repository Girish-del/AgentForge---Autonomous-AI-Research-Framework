import { useState } from "react";

import apiClient from "../services/apiClient";

function LoginPage() {
  const [email, setEmail] = useState("demo@agentforge.ai");
  const [password, setPassword] = useState("password");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    setError("");
    setMessage("");
    try {
      const response = await apiClient.post("/auth/login", { email, password });
      sessionStorage.setItem("agentforge_token", response.data.access_token);
      setMessage("Authenticated. Token saved for API requests.");
    } catch (requestError) {
      setError(requestError?.response?.data?.detail || "Login failed.");
    }
  };

  return (
    <section className="panel">
      <h2>Login</h2>
      <p>Sign in to manage research loops and experiments.</p>
      <form className="form-grid" onSubmit={handleLogin}>
        <label>
          Email
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            required
          />
        </label>
        <label>
          Password
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            required
          />
        </label>
        <button type="submit">Login</button>
      </form>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </section>
  );
}

export default LoginPage;
