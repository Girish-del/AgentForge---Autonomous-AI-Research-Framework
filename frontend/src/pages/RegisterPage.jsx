import { useState } from "react";
import { Link } from "react-router-dom";

function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <section className="auth-card" aria-labelledby="register-title">
      <div className="auth-card__crest" aria-hidden="true">⚙</div>
      <h2 id="register-title">Forge Your Scientist</h2>
      <p className="auth-tagline">
        Bootstrap a local profile. The dev backend currently honors any login on{" "}
        <code>/api/auth/login</code>.
      </p>

      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Codename
          <input
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Dr. Forge"
            required
          />
        </label>
        <label>
          Comm Channel <span className="label-hint">(email)</span>
          <input
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            type="email"
            required
          />
        </label>
        <label>
          Access Cipher
          <input
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            type="password"
            required
          />
        </label>
        <button className="btn-primary" type="submit">Forge Profile</button>
      </form>

      {submitted && (
        <div className="banner banner--info">
          Profile drafted locally. Use any credentials on the login page; the backend register
          endpoint is on the roadmap.
        </div>
      )}

      <p className="auth-foot">
        Already credentialed? <Link to="/">Enter the Lab →</Link>
      </p>
    </section>
  );
}

export default RegisterPage;
