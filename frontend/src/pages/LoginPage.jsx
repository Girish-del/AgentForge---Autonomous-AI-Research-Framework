import { useState } from "react";

import apiClient from "../services/apiClient";

function LoginPage() {
  const [email, setEmail] = useState("demo@agentforge.ai");
  const [password, setPassword] = useState("password");
  const [message, setMessage] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();
    const response = await apiClient.post("/auth/login", { email, password });
    setMessage(`Token: ${response.data.access_token}`);
  };

  return (
    <form onSubmit={handleLogin}>
      <h2>Login</h2>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
      <button type="submit">Login</button>
      <div>{message}</div>
    </form>
  );
}

export default LoginPage;
