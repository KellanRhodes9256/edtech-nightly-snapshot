# snapshot_models.py — typed domain models for the edtech snapshot.
from dataclasses import dataclass, asdict
from typing import List
import base64
import json


@dataclass
class CourseDelivery:
    course_id: str
    title: str
    enrolled_learners: int
    modules_published: int


@dataclass
class LearnerDeadline:
    learner_id: str
    course_id: str
    due_date: str
    submitted: bool


@dataclass
class EducatorReport:
    educator_id: str
    course_id: str
    completion_rate: float
    flagged_learners: int


@dataclass
class NightlySnapshot:
    date: str
    courses: List[CourseDelivery]
    deadlines: List[LearnerDeadline]
    reports: List[EducatorReport]

    def to_object_bytes(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")


def should_snapshot(snapshot: NightlySnapshot) -> bool:
    # Only write a snapshot if at least one course has enrolled learners.
    return any(c.enrolled_learners > 0 for c in snapshot.courses)
