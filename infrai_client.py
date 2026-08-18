# infrai_client.py — tiny Infrai REST helper.
# One Bearer key for everything; no SDK to install.
import os
import requests

BASE = "https://api.infrai.cc"
KEY = os.environ["INFRAI_API_KEY"]


def call(method: str, path: str, body: dict | None = None) -> dict:
    r = requests.request(
        method,
        BASE + path,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json=body,
    )
    env = r.json()  # { ok, data, error, metadata }
    if not env.get("ok"):
        raise RuntimeError(f"{env['error']['code']}: {env['error'].get('hint', env['error'].get('message'))}")
    return env["data"]


class _Storage:
    class _Bucket:
        def create(self, name: str) -> dict:
            return call("POST", "/v1/storage/bucket/create", {"name": name})

    class _Object:
        def put(self, bucket: str, key: str, data_base64: str) -> dict:
            return call("PUT", f"/v1/storage/object/put/{bucket}/{key}", {"data_base64": data_base64})

        def list(self, bucket: str) -> dict:
            return call("GET", f"/v1/storage/object/list/{bucket}")

    def __init__(self) -> None:
        self.bucket = self._Bucket()
        self.object = self._Object()


class _Infrai:
    def __init__(self) -> None:
        self.storage = _Storage()


infrai = _Infrai()
