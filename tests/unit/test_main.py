import pytest
from app.main import (
    DeveloperTask,
    ProductivityReport,
    TaskStatus,
    fetch_all_tasks,
    generate_productivity_report,
    MOCK_TASKS,
)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list() -> None:
    tasks = await fetch_all_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_fetch_all_tasks_items_are_developer_tasks() -> None:
    tasks = await fetch_all_tasks()
    for task in tasks:
        assert isinstance(task, DeveloperTask)


@pytest.mark.asyncio
async def test_generate_productivity_report_returns_report() -> None:
    report = await generate_productivity_report()
    assert isinstance(report, ProductivityReport)


@pytest.mark.asyncio
async def test_generate_productivity_report_completed_tasks_counts_complete_status() -> None:
    report = await generate_productivity_report()
    expected_completed = sum(
        1 for task in MOCK_TASKS.values() if task.status == TaskStatus.COMPLETE
    )
    assert report.completed_tasks == expected_completed


@pytest.mark.asyncio
async def test_generate_productivity_report_total_tasks_matches_mock() -> None:
    report = await generate_productivity_report()
    assert report.total_tasks == len(MOCK_TASKS)


@pytest.mark.asyncio
async def test_generate_productivity_report_total_hours_is_sum() -> None:
    report = await generate_productivity_report()
    expected_hours = round(sum(task.hours_spent for task in MOCK_TASKS.values()), 2)
    assert report.total_hours_spent == expected_hours


@pytest.mark.asyncio
async def test_generate_productivity_report_completion_rate_between_zero_and_one() -> None:
    report = await generate_productivity_report()
    assert 0.0 <= report.completion_rate <= 1.0
