import pytest
from fastapi import status
from main import app
from httpx import AsyncClient
from httpx import ASGITransport
from schemas import AcademicPerformance


def mock_valid_token():
    return {"Authorization": "Bearer valid_token"}



@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_add_academic_performance(async_client):
    payload = {
        "student_id": 1,
        "faculty_id": 1,
        "course_id": 101,
        "mark": 95
    }

    headers = mock_valid_token()

    response = await async_client.put(
        "/academic_performance/",
        json=payload,
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["student_id"] == payload["student_id"]
    assert data["mark"] == payload["mark"]


@pytest.mark.asyncio
async def test_update_academic_performance(async_client):
    payload = {
        "id": 1,
        "student_id": 1,
        "faculty_id": 1,
        "course_id": 101,
        "mark": 98
    }

    headers = mock_valid_token()

    response = await async_client.patch(
        "/academic_performance/",
        json=payload,
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == payload["id"]
    assert data["mark"] == payload["mark"]


@pytest.mark.asyncio
async def test_delete_academic_performance(async_client):
    academic_performance_id = 1
    headers = mock_valid_token()

    response = await async_client.delete(
        f"/academic_performance/?academic_performance_id={academic_performance_id}",
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == academic_performance_id


@pytest.mark.asyncio
async def test_unauthorized_access(async_client):
    response = await async_client.put(
        "/academic_performance/",
        json={"student_id": 1, "faculty_id": 1, "course_id": 1, "mark": 90}
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN or response.status_code == status.HTTP_400_BAD_REQUEST