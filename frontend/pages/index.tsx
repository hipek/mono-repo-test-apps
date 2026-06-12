import { useState, type FormEvent } from "react";

type TokenResponse = {
  access_token: string;
  token_type: string;
};

type ErrorResponse = {
  detail: string;
};

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [displayName, setDisplayName] = useState("");

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.set("username", username);
      formData.set("password", password);

      const res = await fetch("/api/token", {
        method: "POST",
        body: formData,
      });

      const data: TokenResponse | ErrorResponse = await res.json();

      if (!res.ok) {
        setError((data as ErrorResponse).detail || "Login failed");
        return;
      }

      const token = (data as TokenResponse).access_token;
      localStorage.setItem("token", token);
      setDisplayName(username);
      setIsLoggedIn(true);
    } catch {
      setError("Network error — is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  if (isLoggedIn) {
    return (
      <div className="container">
        <div className="card">
          <div className="logo">
            <h1>Welcome, {displayName}!</h1>
            <p>You are successfully logged in</p>
          </div>

          <div className="success">Session active — token stored in localStorage</div>

          <button
            className="submit-btn"
            onClick={() => {
              localStorage.removeItem("token");
              setIsLoggedIn(false);
              setDisplayName("");
            }}
          >
            Sign Out
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">
        <div className="logo">
          <h1>Welcome Back</h1>
          <p>Sign in to your account</p>
        </div>

        <form className="form" onSubmit={handleSubmit}>
          {error && <div className="error">{error}</div>}

          <div className="field">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoFocus
            />
          </div>

          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button className="submit-btn" type="submit" disabled={loading}>
            {loading && <span className="spinner" />}
            {loading ? "Signing in…" : "Sign In"}
          </button>
        </form>

        <div className="hint">
          Demo credentials: <code>admin</code> / <code>admin123</code>
        </div>
      </div>
    </div>
  );
}
