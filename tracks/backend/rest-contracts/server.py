#!/usr/bin/env python3
"""Offline, loopback-only REST contracts exercise (Python 3.10+ stdlib).

The in-memory task store is intentionally ephemeral. No auth, storage, uploads,
external APIs, telemetry, or production-grade rate limits are implemented.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from threading import Lock
from urllib.parse import parse_qs, urlsplit

MAX_BODY_BYTES = 8192
MAX_TASKS = 100
MAX_TITLE_LENGTH = 120
DEFAULT_LIMIT = 20
MAX_PAGE_LIMIT = 50


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    done: bool
    version: int

    def payload(self) -> dict:
        return {"id": self.id, "title": self.title, "done": self.done, "version": self.version}

    def etag(self) -> str:
        return f'"task-{self.id}-v{self.version}"'


class Store:
    """One lock guards all transitions; conditional mutations are atomic."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def create(self, title: str, done: bool) -> Task | None:
        with self._lock:
            if len(self._tasks) >= MAX_TASKS:
                return None
            task = Task(self._next_id, title, done, 1)
            self._next_id += 1
            self._tasks[task.id] = task
            return task

    def get(self, task_id: int) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def list(self, offset: int, limit: int, done: bool | None) -> dict:
        with self._lock:
            matching = [
                task for task in self._tasks.values()
                if done is None or task.done == done
            ]
            matching.sort(key=lambda task: task.id)
            return {
                "items": [task.payload() for task in matching[offset:offset + limit]],
                "total": len(matching),
                "offset": offset,
                "limit": limit,
            }

    def change(self, task_id: int, expected: str, changes: dict) -> tuple[str, Task | None]:
        with self._lock:
            old = self._tasks.get(task_id)
            if old is None:
                return "missing", None
            if expected != old.etag():
                return "stale", old
            title = changes.get("title", old.title)
            done = changes.get("done", old.done)
            if title == old.title and done == old.done:
                return "unchanged", old
            updated = Task(old.id, title, done, old.version + 1)
            self._tasks[task_id] = updated
            return "changed", updated

    def delete(self, task_id: int, expected: str) -> str:
        with self._lock:
            old = self._tasks.get(task_id)
            if old is None:
                return "missing"
            if old.etag() != expected:
                return "stale"
            del self._tasks[task_id]
            return "deleted"


def validate_title(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("title must be text")
    title = value.strip()
    if not title or len(title) > MAX_TITLE_LENGTH:
        raise ValueError(f"title must be 1-{MAX_TITLE_LENGTH} characters after trimming")
    if any(ord(char) < 32 or ord(char) == 127 for char in title):
        raise ValueError("title contains unsupported control characters")
    return title


def json_pairs(items: list[tuple]) -> dict:
    data: dict = {}
    for key, value in items:
        if key in data:
            raise ValueError("duplicate JSON property")
        data[key] = value
    return data


def invalid_constant(_: str) -> None:
    raise ValueError("nonfinite JSON number")


def handler_factory(store: Store):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        server_version = "LocalContractLab/1.0"
        sys_version = ""

        def log_message(self, fmt: str, *args) -> None:
            # Avoid writing arbitrary task content, query strings or headers to logs.
            print(f"local-http method={self.command} status={args[1] if len(args) > 1 else '?'}")

        def send_json(self, status: HTTPStatus, payload: dict, *, headers: dict | None = None) -> None:
            body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            if headers:
                for name, value in headers.items():
                    self.send_header(name, value)
            self.end_headers()
            self.wfile.write(body)

        def error(self, status: HTTPStatus, code: str, message: str) -> None:
            self.send_json(status, {"error": {"code": code, "message": message}})

        def send_empty(self, status: HTTPStatus) -> None:
            self.send_response(status)
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

        def local_request(self, mutation: bool = False) -> bool:
            host = self.headers.get("Host", "")
            port = self.server.server_port
            if host not in (f"127.0.0.1:{port}", f"localhost:{port}"):
                self.error(HTTPStatus.FORBIDDEN, "invalid_host", "Use the loopback host and configured port")
                self.close_connection = True
                return False
            if mutation:
                origin = self.headers.get("Origin")
                if origin is not None and origin not in (
                    f"http://127.0.0.1:{port}", f"http://localhost:{port}"
                ):
                    self.error(HTTPStatus.FORBIDDEN, "invalid_origin", "Cross-origin mutation is disabled")
                    self.close_connection = True
                    return False
            return True

        def route(self) -> tuple[str, int | None, dict[str, list[str]] | None]:
            try:
                parsed = urlsplit(self.path)
                if parsed.fragment:
                    return "invalid", None, None
                if parsed.path == "/health":
                    return "health", None, parse_qs(parsed.query, keep_blank_values=True)
                if parsed.path == "/tasks":
                    return "collection", None, parse_qs(
                        parsed.query, keep_blank_values=True, strict_parsing=True
                    )
                parts = parsed.path.split("/")
                if len(parts) == 3 and parts[1] == "tasks" and (
                    parts[2].isascii() and parts[2].isdecimal()
                ):
                    task_id = int(parts[2])
                    if 1 <= task_id <= 2_147_483_647:
                        return "item", task_id, parse_qs(
                            parsed.query, keep_blank_values=True, strict_parsing=True
                        )
            except (ValueError, OverflowError):
                return "invalid", None, None
            return "invalid", None, None

        def require_no_query(self, query: dict[str, list[str]] | None) -> bool:
            if query:
                self.error(HTTPStatus.BAD_REQUEST, "unexpected_query", "This endpoint accepts no query parameters")
                return False
            return True

        def parse_body(self, *, partial: bool) -> dict | None:
            if self.headers.get("Transfer-Encoding") or len(self.headers.get_all("Content-Length", [])) != 1:
                self.error(HTTPStatus.BAD_REQUEST, "content_length", "One explicit Content-Length is required")
                self.close_connection = True
                return None
            media_type = [part.strip().lower() for part in self.headers.get(
                "Content-Type", "").split(";")]
            if (media_type[0] != "application/json"
                    or len(media_type) > 2
                    or (len(media_type) == 2 and media_type[1] != "charset=utf-8")):
                self.error(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "content_type",
                           "Expected application/json with optional UTF-8 charset")
                self.close_connection = True
                return None
            try:
                length = int(self.headers["Content-Length"])
                if length < 2 or length > MAX_BODY_BYTES:
                    raise ValueError("invalid body size")
                raw = self.rfile.read(length)
                if len(raw) != length:
                    raise ValueError("truncated body")
                data = json.loads(
                    raw.decode("utf-8"), object_pairs_hook=json_pairs,
                    parse_constant=invalid_constant,
                )
                if not isinstance(data, dict):
                    raise ValueError("body must be a JSON object")
                allowed = {"title", "done"}
                if not data or any(key not in allowed for key in data):
                    raise ValueError("unknown or missing fields")
                if not partial and "title" not in data:
                    raise ValueError("title is required")
                if "title" in data:
                    data["title"] = validate_title(data["title"])
                if "done" in data and type(data["done"]) is not bool:
                    raise ValueError("done must be a JSON boolean")
                return data
            except (ValueError, UnicodeError, OverflowError):
                self.error(HTTPStatus.BAD_REQUEST, "invalid_json", "Invalid task payload")
                self.close_connection = True
                return None

        def expected_version(self) -> str | None:
            values = self.headers.get_all("If-Match", [])
            if len(values) != 1 or not values[0].strip():
                self.error(HTTPStatus.PRECONDITION_REQUIRED, "precondition_required",
                           "Provide the task ETag in If-Match")
                return None
            expected = values[0].strip()
            if len(expected) > 100 or not expected.startswith('"') or not expected.endswith('"'):
                self.error(HTTPStatus.BAD_REQUEST, "invalid_if_match", "A single strong ETag is required")
                return None
            return expected

        def do_GET(self) -> None:
            if not self.local_request():
                return
            kind, task_id, query = self.route()
            if kind == "health":
                if self.require_no_query(query):
                    self.send_json(HTTPStatus.OK, {"status": "ok", "storage": "in_memory"})
                return
            if kind == "item":
                if not self.require_no_query(query):
                    return
                task = store.get(task_id)
                if task is None:
                    self.error(HTTPStatus.NOT_FOUND, "not_found", "Task not found")
                else:
                    self.send_json(HTTPStatus.OK, task.payload(), headers={"ETag": task.etag()})
                return
            if kind == "collection":
                if set(query) - {"offset", "limit", "done"}:
                    self.error(HTTPStatus.BAD_REQUEST, "unknown_filter", "Unknown query parameter")
                    return
                try:
                    for key in query:
                        if len(query[key]) != 1:
                            raise ValueError("duplicate query parameter")
                    offset = int(query.get("offset", ["0"])[0])
                    limit = int(query.get("limit", [str(DEFAULT_LIMIT)])[0])
                    if not 0 <= offset <= 100_000 or not 1 <= limit <= MAX_PAGE_LIMIT:
                        raise ValueError("pagination out of bounds")
                    filter_value = query.get("done", [None])[0]
                    if filter_value not in ("true", "false", None):
                        raise ValueError("invalid done filter")
                except (ValueError, TypeError):
                    self.error(HTTPStatus.BAD_REQUEST, "invalid_pagination",
                               "Use offset 0..100000, limit 1..50, done true|false")
                    return
                done = None if filter_value is None else filter_value == "true"
                self.send_json(HTTPStatus.OK, store.list(offset, limit, done))
                return
            self.error(HTTPStatus.NOT_FOUND, "not_found", "Endpoint not found")

        def do_POST(self) -> None:
            if not self.local_request(mutation=True):
                return
            kind, _, query = self.route()
            if kind != "collection":
                self.error(HTTPStatus.NOT_FOUND, "not_found", "Endpoint not found")
                self.close_connection = True
                return
            if not self.require_no_query(query):
                self.close_connection = True
                return
            data = self.parse_body(partial=False)
            if data is None:
                return
            task = store.create(data["title"], data.get("done", False))
            if task is None:
                self.error(HTTPStatus.CONFLICT, "capacity", "In-memory task limit reached")
            else:
                self.send_json(HTTPStatus.CREATED, task.payload(),
                               headers={"Location": f"/tasks/{task.id}", "ETag": task.etag()})

        def do_PATCH(self) -> None:
            if not self.local_request(mutation=True):
                return
            kind, task_id, query = self.route()
            if kind != "item":
                self.error(HTTPStatus.NOT_FOUND, "not_found", "Endpoint not found")
                self.close_connection = True
                return
            if not self.require_no_query(query):
                self.close_connection = True
                return
            expected = self.expected_version()
            if expected is None:
                self.close_connection = True
                return
            data = self.parse_body(partial=True)
            if data is None:
                return
            state, task = store.change(task_id, expected, data)
            if state == "missing":
                self.error(HTTPStatus.NOT_FOUND, "not_found", "Task not found")
            elif state == "stale":
                self.error(HTTPStatus.PRECONDITION_FAILED, "stale_etag",
                           "Read the latest task and retry with its new ETag")
            else:
                self.send_json(HTTPStatus.OK, task.payload(), headers={"ETag": task.etag()})

        def do_DELETE(self) -> None:
            if not self.local_request(mutation=True):
                return
            kind, task_id, query = self.route()
            if kind != "item":
                self.error(HTTPStatus.NOT_FOUND, "not_found", "Endpoint not found")
                self.close_connection = True
                return
            if not self.require_no_query(query):
                self.close_connection = True
                return
            expected = self.expected_version()
            if expected is None:
                return
            state = store.delete(task_id, expected)
            if state == "missing":
                self.error(HTTPStatus.NOT_FOUND, "not_found", "Task not found")
            elif state == "stale":
                self.error(HTTPStatus.PRECONDITION_FAILED, "stale_etag",
                           "Read the latest task and retry with its new ETag")
            else:
                self.send_empty(HTTPStatus.NO_CONTENT)

        def do_OPTIONS(self) -> None:
            self.error(HTTPStatus.METHOD_NOT_ALLOWED, "not_allowed",
                       "Browser cross-origin access is not supported")

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765, help="localhost-only TCP port")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("--port must be 1024..65535")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_factory(Store()))
    server.daemon_threads = True
    print(f"REST contracts lab running on http://127.0.0.1:{args.port}", flush=True)
    print("Data is not persisted; Ctrl+C stops the server.", flush=True)
    try:
        server.serve_forever(poll_interval=0.25)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
