import { useState } from "react";

function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
  };

  return (
    <section className="panel">
      <h2>Register</h2>
      <p>Bootstrap a local account profile for this development build.</p>
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Name
          <input value={name} onChange={(event) => setName(event.target.value)} required />
        </label>
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
        <button type="submit">Create Account</button>
      </form>
      <p className="muted">
        Registration endpoint is not implemented yet, but this complete UI is ready for backend wiring.
      </p>
    </section>
  );
}

export default RegisterPage;
