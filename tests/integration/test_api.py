"""Integration tests for the FastAPI app."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_enhance_happy_path(client: TestClient) -> None:
    response = client.post(
        "/v1/enhance",
        json={"text": "explain transformers", "strategy": "cot_injector"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "enhanced" in data
    assert data["original"] == "explain transformers"
    assert len(data["enhanced"]) > len(data["original"])


def test_enhance_empty_text_returns_422(client: TestClient) -> None:
    response = client.post("/v1/enhance", json={"text": "", "strategy": "cot_injector"})
    assert response.status_code == 422


def test_enhance_all_strategies(client: TestClient) -> None:
    for strategy in ["cot_injector", "structure_formatter", "context_enricher", "composite"]:
        response = client.post(
            "/v1/enhance",
            json={"text": "what is recursion", "strategy": strategy},
        )
        assert response.status_code == 200, f"Failed for strategy: {strategy}"


def test_strategies_list_non_empty(client: TestClient) -> None:
    response = client.get("/v1/strategies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4


def test_strategies_list_has_required_fields(client: TestClient) -> None:
    response = client.get("/v1/strategies")
    for item in response.json():
        assert "id" in item
        assert "description" in item
        assert "name" in item


def test_batch_enhance_three_prompts(client: TestClient) -> None:
    response = client.post(
        "/v1/enhance/batch",
        json={
            "prompts": [
                {"text": "summarise this document", "strategy": "structure_formatter"},
                {"text": "write python code", "strategy": "cot_injector"},
                {"text": "explain DNS", "strategy": "context_enricher"},
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 3


def test_batch_enhance_too_many_prompts(client: TestClient) -> None:
    response = client.post(
        "/v1/enhance/batch",
        json={"prompts": [{"text": f"prompt {i}", "strategy": "cot_injector"} for i in range(21)]},
    )
    assert response.status_code == 422
