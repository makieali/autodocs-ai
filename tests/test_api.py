"""Tests for the FastAPI server."""

from __future__ import annotations

import pytest

from autodocs_ai import __version__


@pytest.fixture
def client():
    """Create a test client for the API."""
    from fastapi.testclient import TestClient
    from autodocs_ai.api.app import app
    return TestClient(app)


class TestHealthEndpoints:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["version"] == __version__

    def test_list_templates(self, client):
        response = client.get("/templates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        names = [t["name"] for t in data]
        assert "resume" in names
        assert "invoice" in names
        assert "proposal" in names

    def test_list_providers(self, client):
        response = client.get("/providers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        names = [p["name"] for p in data]
        assert "openai" in names
        assert "anthropic" in names
        assert "ollama" in names


class TestGenerateEndpoint:
    def test_generate_requires_body(self, client):
        response = client.post("/generate")
        assert response.status_code == 422  # Validation error

    def test_generate_requires_prompt(self, client):
        response = client.post("/generate", json={})
        assert response.status_code == 422

    def test_generate_with_invalid_provider_fails(self, client):
        response = client.post("/generate", json={
            "prompt": "test",
            "provider": "nonexistent",
        })
        # Should fail with 500 or 400 since provider doesn't exist
        assert response.status_code in (400, 500)


class TestAPIKeyAuth:
    def test_no_auth_when_key_not_configured(self, client):
        """Without AUTODOCS_API_KEY set, endpoints should be accessible."""
        response = client.get("/templates")
        assert response.status_code == 200
