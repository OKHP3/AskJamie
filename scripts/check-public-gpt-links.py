#!/usr/bin/env python3
"""Probe represented public AskJamie and BrandGuard ChatGPT destinations.

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
    "AJ04": "https://chatgpt.com/g/g-691fa3532a588191b5b362f2fc07e8b3-okhp3-brandguardtm-by-askjamietm",
    "BFS01": "https://chatgpt.com/g/g-68e8927c5cd48191863e613f04ee042d-bfs-framing-intelligent-futures",
    "BRG01": "https://chatgpt.com/g/g-694adab7e534819197ebfce0f5862c21-brick-toys-billund-in-1932",
    "BRG02": "https://chatgpt.com/g/g-694ac7b0f8b88191ab788b14898ba340-starbucks",
    "BRG03": "https://chatgpt.com/g/g-694ad15940f88191a87082759ca1dda1-brooks-running",
    "BRG04": "https://chatgpt.com/g/g-694add8864c08191a89b1fcb119e956c-ping",
    "BRG05": "https://chatgpt.com/g/g-694ac90f7dbc81918a6e27ff35b34de6-costco",
    "BRG06": "https://chatgpt.com/g/g-694ac93c34f08191931aa28bd8b3571f-hershey-okhp3-brandguardtm",
    "BRG07": "https://chatgpt.com/g/g-694adbdf17548191beedb2b973071bfa-lvmh",
    "BRG08": "https://chatgpt.com/g/g-694ac9b7d9048191b81085d5b270cb79-dollar-general",
    "BRG09": "https://chatgpt.com/g/g-694adb61d4ec819183d8652bb8d50fe1-coca-cola",
    "BRG10": "https://chatgpt.com/g/g-694acda6b8908191a3872f005dc764ed-discount-tire",
    "BRG11": "https://chatgpt.com/g/g-694acd390b4c81919e17a209752adf49-scheels",
    "BRG12": "https://chatgpt.com/g/g-69544ab093dc8191a1f0d0f901a2ada5-mathews-archery",
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