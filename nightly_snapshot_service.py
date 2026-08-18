# nightly_snapshot_service.py — application entry point.
import base64
import os
from datetime import date

from infrai_client import infrai
from snapshot_models import (
    CourseDelivery,
    LearnerDeadline,
    EducatorReport,
    NightlySnapshot,
    should_snapshot,
)

BUCKET = "edtech-nightly"


def run_nightly() -> str:
    # Build tonight's domain-shaped records.
    snapshot = NightlySnapshot(
        date=str(date.today()),
        courses=[CourseDelivery("c1", "Video Editing 101", 42, 8)],
        deadlines=[LearnerDeadline("l1", "c1", "2024-12-01", False)],
        reports=[EducatorReport("e1", "c1", 0.73, 3)],
    )
    if not should_snapshot(snapshot):
        return "skip"
    # Create the bucket if this is a fresh account.
    infrai.storage.bucket.create(BUCKET)
    key = f"snapshots/{snapshot.date}.json"
    payload = base64.b64encode(snapshot.to_object_bytes()).decode("ascii")
    infrai.storage.object.put(BUCKET, key, payload)
    return key


if __name__ == "__main__":
    written = run_nightly()
    if written == "skip":
        print("No enrolled learners; snapshot skipped.")
    else:
        print(f"Wrote snapshot to {written}")
        items = infrai.storage.object.list(BUCKET)["items"]
        print(f"Bucket now holds {len(items)} object(s).")
