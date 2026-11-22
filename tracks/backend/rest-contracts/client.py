#!/usr/bin/env python3
"""A synthetic, opt-in client walkthrough of the loopback REST contract lab.

Run server.py in another terminal first. This client never calls external hosts.
Default behavior reads /health only; --demo creates and then removes one task.
"""
from __future__ import annotations

import argparse
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ApiError(RuntimeError):
    def __init__(self, status: int, text: str) -> None:
        super().__init__(f"HTTP {status}: {text}")
        self.status = status


def request(base: str, method: str, path: str, payload: dict | None = None,
            etag: str | None = None) -> tuple[int, object | None, dict]:
    headers = {"Accept": "application/json"}
    data = None
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    if etag is not None:
        headers["If-Match"] = etag
    req = Request(base + path, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=4) as response:
            raw = response.read(128 * 1024)
            result = json.loads(raw) if raw else None
            return response.status, result, dict(response.headers.items())
    except HTTPError as error:
        content = error.read(1024)
        raise ApiError(error.code, content.decode("utf-8", errors="replace")[:300]) from error


def demo(base: str) -> None:
    status, task, headers = request(
        base, "POST", "/tasks", {"title": "Synthetic API contract exercise"}
    )
    task_id = task["id"]
    etag = headers["ETag"]
    print(f"Created task #{task_id} (HTTP {status})")
    try:
        _, fetched, current_headers = request(base, "GET", f"/tasks/{task_id}")
        print("Read task version:", fetched["version"])
        if current_headers["ETag"] != etag:
            raise RuntimeError("Unexpected ETag change before first edit")

        try:
            request(base, "PATCH", f"/tasks/{task_id}",
                    {"done": True}, etag='"task-999-v1"')
        except ApiError as exc:
            if exc.status != 412:
                raise
            print("Stale update correctly rejected (HTTP 412)")
        else:
            raise RuntimeError("Stale If-Match was unexpectedly accepted")

        _, updated, new_headers = request(
            base, "PATCH", f"/tasks/{task_id}", {"done": True}, etag=etag
        )
        print("Updated task version:", updated["version"])
        etag = new_headers["ETag"]

        _, listing, _ = request(base, "GET", "/tasks?done=true&limit=10&offset=0")
        print("Completed tasks visible:", listing["total"])
    finally:
        try:
            # Reread the latest version so cleanup does not bypass concurrency.
            _, _, fresh_headers = request(base, "GET", f"/tasks/{task_id}")
            status, _, _ = request(
                base, "DELETE", f"/tasks/{task_id}", etag=fresh_headers["ETag"]
            )
            print(f"Synthetic task cleaned up (HTTP {status})")
        except ApiError as exc:
            if exc.status != 404:
                print("Cleanup unavailable; restart server to clear in-memory state.")
            # No credentials or persistent tasks exist in this demo.


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--demo", action="store_true",
                        help="opt into creating/deleting a synthetic local task")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("port must be between 1024 and 65535")
    base = f"http://127.0.0.1:{args.port}"
    try:
        status, health, _ = request(base, "GET", "/health")
        print(f"Local server: HTTP {status}, storage={health['storage']}")
        if args.demo:
            demo(base)
        else:
            print("No mutations performed. Use --demo for a synthetic CRUD walkthrough.")
    except URLError as error:
        raise SystemExit("Local server unavailable; start server.py first.") from error
    except ApiError as error:
        raise SystemExit(f"Server rejected a request with HTTP {error.status}.") from error


if __name__ == "__main__":
    main()
