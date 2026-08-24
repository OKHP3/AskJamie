#!/usr/bin/env python3
"""Probe the public AJ01-AJ03 ChatGPT destinations without changing site files.

Usage:
    python3 scripts/check-public-gpt-links.py
    python3 scripts/check-public-gpt-links.py --timeout 15
    python3 scripts/check-public-gpt-links.py --timeout 15 --retries 2

The probe is deliberately separate from check-links.py. A failed external
request must be investigated and classified, never used to rewrite HTML.
"""
from __future__ import annotations

import argparse
import socket
import sys
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


PUBLIC_GPTS = {
    "AJ01": "https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00-resume-representative-by-askjamietm",
    "AJ02": "https://chatgpt.com/g/g-691fa5845230819199d4ffb89b13e9ab-professional-portfolio-by-askjamietm",
    "AJ03": "https://chatgpt.com/g/g-691f9a52f5088191b4f552770ffb5886-enterprise-sleuth-by-askjamietm",
}

TRANSIENT_STATUSES = {408, 425, 429} | set(range(500, 600))


@dataclass(frozen=True)
class ProbeResult:
    lens_id: str
    url: str
    classification: str
    status: int | None = None
    final_url: str | None = None
    detail: str = ""


def classify_status(status: int) -> str:
    """Return an actionable class, not just an HTTP label."""
    if 200 <= status < 400:
        return "reachable"
    if status in {401, 403}:
        return "authentication_or_private"
    if status in {404, 410}:
        return "broken_or_unpublished"
    if status in TRANSIENT_STATUSES:
        return "transient_service"
    return "unexpected_response"


def probe(lens_id: str, url: str, timeout: float) -> ProbeResult:
    request = Request(
        url,
        headers={
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "AskJamie-public-gpt-link-check/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            return ProbeResult(
                lens_id,
                url,
                classify_status(status),
                status,
                response.geturl(),
            )
    except HTTPError as error:
        return ProbeResult(
            lens_id,
            url,
            classify_status(error.code),
            error.code,
            error.geturl(),
            error.reason or "",
        )
    except (TimeoutError, socket.timeout, URLError, OSError) as error:
        return ProbeResult(
            lens_id,
            url,
            "transient_network",
            detail=str(getattr(error, "reason", error)),
        )


def probe_with_retries(
    lens_id: str, url: str, timeout: float, retries: int
) -> ProbeResult:
    """Retry only transient outcomes; never retry a destination-status result."""
    result = probe(lens_id, url, timeout)
    for attempt in range(retries):
        if result.classification not in {"transient_network", "transient_service"}:
            break
        time.sleep(min(2**attempt, 5))
        result = probe(lens_id, url, timeout)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument(
        "--retries",
        type=int,
        default=0,
        help="retry transient network/service results this many times",
    )
    args = parser.parse_args()
    if args.retries < 0:
        parser.error("--retries must be non-negative")

    results = [
        probe_with_retries(lens_id, url, args.timeout, args.retries)
        for lens_id, url in PUBLIC_GPTS.items()
    ]
    exit_code = 0
    for result in results:
        status = f"HTTP {result.status}" if result.status is not None else "no HTTP response"
        destination = f" -> {result.final_url}" if result.final_url and result.final_url != result.url else ""
        detail = f" ({result.detail})" if result.detail else ""
        print(
            f"{result.lens_id}: {result.classification}: {status}"
            f" url={result.url}{destination}{detail}"
        )
        if result.classification != "reachable":
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())