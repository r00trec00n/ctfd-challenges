#!/usr/bin/env python3
"""Import one or all challenge directories into CTFd."""
from __future__ import annotations

import argparse
import getpass
import json
import mimetypes
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "challenges"


class API:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/") + "/api/v1"
        self.token = token

    def call(self, method: str, path: str, data=None, upload: Path | None = None):
        headers = {"Authorization": "Token " + self.token}
        body = None
        if upload is not None:
            boundary = uuid.uuid4().hex
            parts: list[bytes] = []
            for key, value in (data or {}).items():
                parts.append(
                    f"--{boundary}\r\nContent-Disposition: form-data; name=\"{key}\"\r\n\r\n{value}\r\n".encode()
                )
            mime = mimetypes.guess_type(upload.name)[0] or "application/octet-stream"
            parts.append(
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{upload.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
            )
            parts.extend([upload.read_bytes(), f"\r\n--{boundary}--\r\n".encode()])
            body = b"".join(parts)
            headers["Content-Type"] = "multipart/form-data; boundary=" + boundary
        else:
            headers["Content-Type"] = "application/json"
            if data is not None:
                body = json.dumps(data).encode()
        request = urllib.request.Request(self.base + path, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:300]
            raise RuntimeError(f"{method} {path}: HTTP {exc.code}: {detail}") from None
        if result.get("success") is not True:
            raise RuntimeError(f"{method} {path}: CTFd reported failure")
        return result.get("data")


def discover() -> list[Path]:
    return sorted(p for p in ROOT.glob("*/*") if (p / "challenge.json").is_file())


def load(path: Path) -> dict:
    item = json.loads((path / "challenge.json").read_text())
    item["_path"] = path
    for rel in item.get("files", []):
        candidate = path / rel
        if not candidate.is_file():
            raise RuntimeError(f"{path.name}: missing attachment {candidate}")
    if item.get("type") not in {"standard", "container"}:
        raise RuntimeError(f"{path.name}: unsupported type {item.get('type')!r}")
    return item


def select(args) -> list[dict]:
    items = [load(p) for p in discover()]
    if args.challenge:
        items = [x for x in items if x["_path"].name == args.challenge or x["name"] == args.challenge]
        if not items:
            raise RuntimeError(f"Challenge not found: {args.challenge}")
    elif not args.all:
        raise RuntimeError("Choose --all or --challenge SLUG")
    return items


def create_payload(item: dict) -> dict:
    payload = {
        "name": item["name"],
        "category": item["category"],
        "description": item["description"],
        "value": item["value"],
        "type": item["type"],
        "state": "hidden",
        "max_attempts": 0,
    }
    for key in ("image", "port", "ctype"):
        if key in item:
            payload[key] = item[key]
    if item["type"] == "container":
        payload.update({"command": "", "volumes": "", "initial": item["value"], "minimum": item["value"], "decay": 1, "function": "static"})
    return payload


def import_one(api: API, item: dict, publish: bool) -> None:
    existing = {x["name"]: x for x in api.call("GET", "/challenges")}
    current = existing.get(item["name"])
    if current is None:
        current = api.call("POST", "/challenges", create_payload(item))
    elif current.get("type") != item["type"]:
        raise RuntimeError(f"{item['name']}: existing challenge type differs")
    cid = current["id"]

    flags = api.call("GET", f"/challenges/{cid}/flags")
    if not any(f.get("content") == item["flag"] for f in flags):
        if flags:
            raise RuntimeError(f"{item['name']}: refusing to overwrite an unexpected existing flag")
        api.call("POST", "/flags", {"challenge_id": cid, "type": "static", "content": item["flag"], "data": "case_sensitive"})

    files = api.call("GET", f"/challenges/{cid}/files")
    uploaded = {Path(f.get("location", "").replace("\\", "/")).name for f in files}
    for rel in item.get("files", []):
        attachment = item["_path"] / rel
        if attachment.name not in uploaded:
            api.call("POST", "/files", {"challenge_id": cid, "type": "challenge"}, upload=attachment)

    api.call("PATCH", f"/challenges/{cid}", {"state": "visible" if publish else "hidden"})
    print(f"{item['name']}: {'visible' if publish else 'hidden'} (id={cid})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import CTFd challenge directories")
    parser.add_argument("--url", required=True, help="CTFd base URL")
    parser.add_argument("--all", action="store_true", help="Import every challenge")
    parser.add_argument("--challenge", help="Import one directory slug or exact challenge name")
    parser.add_argument("--publish", action="store_true", help="Make imported challenges visible after import")
    parser.add_argument("--dry-run", action="store_true", help="Validate without contacting CTFd")
    args = parser.parse_args()
    items = select(args)
    print(f"Validated {len(items)} challenge(s): {', '.join(x['name'] for x in items)}")
    if args.dry_run:
        return
    token = getpass.getpass("CTFd API token: ").strip()
    if not token:
        raise SystemExit("An API token is required")
    api = API(args.url, token)
    for item in items:
        import_one(api, item, args.publish)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, urllib.error.URLError) as exc:
        raise SystemExit(str(exc))
