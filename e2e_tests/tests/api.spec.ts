import { test, expect } from "@playwright/test";

test.describe("API Health", () => {
  test("health-check", async ({ request }) => {
    const res = await request.get("http://localhost:8000/");
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body).toEqual({ service: "monorepo-api", status: "ok" });
  });
});

test.describe("API Auth", () => {
  test("login-success", async ({ request }) => {
    const res = await request.post("http://localhost:8000/api/token", {
      form: { username: "admin", password: "admin123" },
    });
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body).toHaveProperty("access_token");
    expect(body).toHaveProperty("token_type");
  });

  test("login-failure", async ({ request }) => {
    const res = await request.post("http://localhost:8000/api/token", {
      form: { username: "admin", password: "wrong" },
    });
    expect(res.status()).toBe(401);
    const body = await res.json();
    expect(body.detail).toBe("Invalid credentials");
  });

  test("me-authenticated", async ({ request }) => {
    const res = await request.post("http://localhost:8000/api/token", {
      form: { username: "admin", password: "admin123" },
    });
    const { access_token } = await res.json();

    const meRes = await request.get("http://localhost:8000/api/me", {
      headers: { Authorization: `Bearer ${access_token}` },
    });
    expect(meRes.status()).toBe(200);
    const meBody = await meRes.json();
    expect(meBody).toEqual({ username: "admin", full_name: "Admin User" });
  });

  test("me-unauthenticated", async ({ request }) => {
    const res = await request.get("http://localhost:8000/api/me");
    expect(res.status()).toBe(401);
  });

  test("register-new-user", async ({ request }) => {
    const username = `e2e_${Date.now()}`;
    const res = await request.post("http://localhost:8000/api/register", {
      data: { username, password: "testpass123", full_name: "E2E Tester" },
    });
    expect(res.status()).toBe(200);
    const body = await res.json();
    expect(body).toEqual({ username, full_name: "E2E Tester" });
  });

  test("register-duplicate", async ({ request }) => {
    const res = await request.post("http://localhost:8000/api/register", {
      data: { username: "admin", password: "admin123", full_name: "Admin User" },
    });
    expect(res.status()).toBe(409);
    const body = await res.json();
    expect(body.detail).toBe("Username already exists");
  });
});
