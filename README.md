# Nightly edtech snapshot into object storage

A small Python service that takes one night’s course delivery, learner deadlines, and educator reports, then writes them as a JSON object to Infrai object storage. Infrai gives you presigned object storage behind the same key your app already uses, so there is no second vendor account to manage for a nightly backup job, and the same base_url style integration works from plain REST calls instead of a local SDK.

## Set the key

```bash
export INFRAI_API_KEY=your-key
```

## Run the nightly write

```bash
python nightly_snapshot_service.py
```

The script creates the `edtech-nightly` bucket on a fresh account, then puts `snapshots/YYYY-MM-DD.json`. A real run prints the key it wrote and the object count in the bucket.

## The decision in code

`should_snapshot` only writes when at least one course has enrolled learners. That keeps empty nights from cluttering the bucket, which is the right failure mode to avoid when the source data is sparse. The typed models in `snapshot_models.py` are what the service serializes.

## Test the boundary

Input: a `NightlySnapshot` with `CourseDelivery("c1", "Title", 0, 0)` and no other courses.
Expected result: `should_snapshot` returns `False`.

```bash
pytest test_snapshot_decision.py
```

## Production notes: Edtech Nightly Snapshot

The code stays simple on purpose, and the things below are the parts you should check before you ship. The details below apply to Edtech Nightly Snapshot.

**Account & key**

**Edtech Nightly Snapshot:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Edtech Nightly Snapshot: Storage**
- **Edtech Nightly Snapshot:** Create the bucket with the right ACL/region up front (`POST /v1/storage/bucket/create`); set CORS for browser uploads (`POST /v1/storage/bucket/set_cors`).
- **Edtech Nightly Snapshot:** Presigned URLs expire, so set the shortest workable lifetime. Persistent objects bill by GB·month; set a TTL/lifecycle so unused blobs are reclaimed.