import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_returns_200(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_status_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_200(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_returns_list(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_all_tasks_items_have_expected_fields(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    for item in response.json():
        assert "task_id" in item
        assert "title" in item
        assert "status" in item
        assert "hours_spent" in item


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_returns_200(client: AsyncClient) -> None:
    response = await client.get("/report")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_has_expected_fields(client: AsyncClient) -> None:
    response = await client.get("/report")
    data = response.json()
    assert "total_tasks" in data
    assert "completed_tasks" in data
    assert "total_hours_spent" in data
    assert "completion_rate" in data


@pytest.mark.asyncio
@pytest.mark.integration
async def test_get_productivity_report_completed_tasks_not_pending(client: AsyncClient) -> None:
    """Validates the bug fix: completed_tasks counts COMPLETE status, not PENDING."""
    tasks_response = await client.get("/tasks")
    tasks = tasks_response.json()
    expected_completed = sum(1 for t in tasks if t["status"] == "complete")

    report_response = await client.get("/report")
    assert report_response.json()["completed_tasks"] == expected_completed


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_200(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "New integration test task", "status": "pending", "hours_spent": 1.5}
    response = await client.post("/log_task", json=payload)
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_returns_message_dict(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "Return type test", "status": "pending", "hours_spent": 0.0}
    response = await client.post("/log_task", json=payload)
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "logged successfully" in data["message"]


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_invalid_status_returns_422(client: AsyncClient) -> None:
    payload = {"task_id": 0, "title": "Bad status task", "status": "invalid_status", "hours_spent": 0.0}
    response = await client.post("/log_task", json=payload)
    assert response.status_code == 422
