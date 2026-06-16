import json
import os

SCENARIOS_DIR = os.path.join(os.path.dirname(__file__), "..", "scenarios")

SCENARIOS = {
    "auth-login.json": {
        "description": "Login scenarios for the monorepo app",
        "base_url": "http://localhost:3000",
        "scenarios": [
            {
                "id": "valid-login-admin",
                "description": "Login with valid admin credentials",
                "username": "admin",
                "password": "admin123",
                "expected": {"status": "success", "redirect": True},
            },
            {
                "id": "valid-login-user",
                "description": "Login with valid demo user credentials",
                "username": "user",
                "password": "pass123",
                "expected": {"status": "success", "redirect": True},
            },
            {
                "id": "invalid-password",
                "description": "Login with wrong password",
                "username": "admin",
                "password": "wrongpassword",
                "expected": {"status": "error", "message": "Invalid credentials"},
            },
            {
                "id": "invalid-username",
                "description": "Login with non-existent username",
                "username": "nonexistent",
                "password": "somepass",
                "expected": {"status": "error", "message": "Invalid credentials"},
            },
            {
                "id": "empty-username",
                "description": "Login with empty username",
                "username": "",
                "password": "admin123",
                "expected": {"status": "validation_error"},
            },
            {
                "id": "empty-password",
                "description": "Login with empty password",
                "username": "admin",
                "password": "",
                "expected": {"status": "validation_error"},
            },
        ],
    },
    "api-health.json": {
        "description": "API health check and public endpoint scenarios",
        "base_url": "http://localhost:3000",
        "scenarios": [
            {
                "id": "health-check",
                "description": "GET / returns service status",
                "method": "GET",
                "path": "/",
                "expected_status": 200,
                "expected_body": {"service": "monorepo-api", "status": "ok"},
            },
        ],
    },
    "api-auth.json": {
        "description": "API authentication scenarios",
        "base_url": "http://localhost:3000",
        "scenarios": [
            {
                "id": "login-success",
                "description": "POST /api/token with valid credentials returns token",
                "method": "POST",
                "path": "/api/token",
                "body": {"username": "admin", "password": "admin123"},
                "expected_status": 200,
                "expected_fields": ["access_token", "token_type"],
            },
            {
                "id": "login-failure",
                "description": "POST /api/token with invalid credentials returns 401",
                "method": "POST",
                "path": "/api/token",
                "body": {"username": "admin", "password": "wrong"},
                "expected_status": 401,
                "expected_body": {"detail": "Invalid credentials"},
            },
            {
                "id": "me-authenticated",
                "description": "GET /api/me with valid token returns user info",
                "method": "GET",
                "path": "/api/me",
                "requires_auth": True,
                "auth_credentials": {"username": "admin", "password": "admin123"},
                "expected_status": 200,
                "expected_body": {"username": "admin", "full_name": "Admin User"},
            },
            {
                "id": "me-unauthenticated",
                "description": "GET /api/me without token returns 401",
                "method": "GET",
                "path": "/api/me",
                "expected_status": 401,
            },
            {
                "id": "register-new-user",
                "description": "POST /api/register creates a new user",
                "method": "POST",
                "path": "/api/register",
                "body": {"username": "e2etest", "password": "testpass123", "full_name": "E2E Tester"},
                "expected_status": 200,
                "expected_body": {"username": "e2etest", "full_name": "E2E Tester"},
            },
            {
                "id": "register-duplicate",
                "description": "POST /api/register with existing username returns 409",
                "method": "POST",
                "path": "/api/register",
                "body": {"username": "admin", "password": "admin123", "full_name": "Admin User"},
                "expected_status": 409,
                "expected_body": {"detail": "Username already exists"},
            },
            {
                "id": "register-validation",
                "description": "POST /api/register with missing fields returns 422",
                "method": "POST",
                "path": "/api/register",
                "body": {"username": "testonly"},
                "expected_status": 422,
            },
        ],
    },
}

def main():
    os.makedirs(SCENARIOS_DIR, exist_ok=True)

    for filename, data in SCENARIOS.items():
        filepath = os.path.join(SCENARIOS_DIR, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {filepath}")

    summary = {
        "generated_at": "2026-06-16",
        "total_scenario_files": len(SCENARIOS),
        "total_scenarios": sum(len(v["scenarios"]) for v in SCENARIOS.values()),
        "files": list(SCENARIOS.keys()),
    }
    summary_path = os.path.join(SCENARIOS_DIR, "_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Created: {summary_path}")

    total = summary["total_scenarios"]
    print(f"\nDone — {total} scenarios across {len(SCENARIOS)} files generated.")


if __name__ == "__main__":
    main()
