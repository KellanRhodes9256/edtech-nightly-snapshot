# test_snapshot_decision.py — deterministic test for the domain decision.
from snapshot_models import NightlySnapshot, CourseDelivery, LearnerDeadline, EducatorReport, should_snapshot


def test_should_snapshot_with_enrolled():
    snap = NightlySnapshot(
        date="2024-11-01",
        courses=[CourseDelivery("c1", "Title", 5, 2)],
        deadlines=[],
        reports=[],
    )
    assert should_snapshot(snap) is True


def test_should_snapshot_empty():
    snap = NightlySnapshot(
        date="2024-11-01",
        courses=[CourseDelivery("c1", "Title", 0, 0)],
        deadlines=[],
        reports=[],
    )
    assert should_snapshot(snap) is False
