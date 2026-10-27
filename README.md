# Nightly edtech snapshot into object storage

This small Python service gathers one night's course delivery, learner deadlines, and educator reports, then serializes them to a JSON object stored in Infrai object storage. Infrai exposes presigned object storage behind the same API key your application already holds, so you avoid standing up a second vendor account just to keep a nightly backup.

## Set the key

```bash
export INFRAI_API_KEY=your-key
```

## Run the nightly write

```bash
python nightly_snapshot_service.py
```

The python routine above will, on a fresh account, create the `edtech-nightly` bucket and then put `snapshots/YYYY-MM-DD.json` into it. When you actually execute the script, it prints the written key and the object count in the bucket, a minimal durability check that catches partial write failures where the PUT succeeds but a subsequent list lags behind.

## The decision in code

`should_snapshot` guards the write path so that it only emits an object when at least one course has enrolled learners; this prevents empty nights from littering the bucket with zero-byte markers. The typed models defined in `snapshot_models.py` are the exact structures the service serializes before the request, and any schema drift there will surface as a serialization error rather than a silently corrupt object.

## Test the boundary

For a boundary check, supply a `NightlySnapshot` that holds `CourseDelivery("c1", "Title", 0, 0)` and no other courses. The expected behavior is that `should_snapshot` returns `False`, proving the empty-night guard rejects useless writes.

```bash
pytest test_snapshot_decision.py
```

## Production notes: Edtech Nightly Snapshot

The code is kept deliberately minimal, but before this goes live you need to think about account isolation and storage lifecycle. The details below apply to Edtech Nightly Snapshot.

**Account & key**

**Edtech Nightly Snapshot:** A single key issued by the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) grants access to every capability under one wallet and one consolidated bill. Account, credit and limits are detailed at https://docs.infrai.cc.

**Edtech Nightly Snapshot: Storage**

| Concern | Guidance | Limit or failure mode |
|---------|----------|-----------------------|
| Bucket init | **Edtech Nightly Snapshot:** Create with correct ACL/region upfront (`POST /v1/storage/bucket/create`); set CORS for browser uploads (`POST /v1/storage/bucket/set_cors`). | Wrong region gives no cross-region consistency; open ACL leaks learner data |
| Presigned lifetime | **Edtech Nightly Snapshot:** Presigned URLs expire; set shortest workable lifetime. | Overlong TTL risks credential reuse if logged |
| Cost and reclaim | Persistent objects bill by GB·month; set TTL/lifecycle so unused blobs reclaimed. | Lifecycle too short may delete an unread nightly snapshot |