#!/usr/bin/env python3
"""Replay a recorded browser journey headless.

A journey is a JSON step script (see ../../docs/journeys.md). This runner is a
replay tool, not a test suite: it re-checks something that was already verified
once, and it never invents or repairs locators on its own.

Exit codes
  0  every step passed
  1  an assertion failed (candidate product defect)
  2  every locator for a step failed (hand to a human or a healing agent)
  3  blocked by the mutation guard
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

PASS, ASSERT_FAIL, LOCATOR_EXHAUSTED, BLOCKED = 0, 1, 2, 3
ENV_REF = re.compile(r"\$\{ENV:([A-Za-z0-9_]+)(?::([^}]*))?\}")


class LocatorExhausted(Exception):
    pass


class AssertionFailed(Exception):
    pass


def expand(value: str) -> str:
    """Replace ${ENV:NAME} or ${ENV:NAME:default} so secrets never live in the journey file."""
    def sub(m):
        name, default = m.group(1), m.group(2)
        found = os.environ.get(name, default)
        if found is None:
            raise SystemExit(f"environment variable {name} is required by the journey")
        return found
    return ENV_REF.sub(sub, value)


def resolve(page, locators, timeout_ms):
    """Try each locator in order. Returns (element, index_used)."""
    for index, loc in enumerate(locators):
        try:
            el = page.locator(loc).first
            el.wait_for(state="visible", timeout=timeout_ms)
            return el, index
        except PWTimeout:
            continue
    raise LocatorExhausted(f"none of {locators} became visible within {timeout_ms} ms each")


def run_step(page, step, timeout_ms):
    action = step["action"]
    if action == "goto":
        page.goto(expand(step["url"]))
        return None
    if action == "expect_url_contains":
        needle = expand(step["value"])
        if needle not in page.url:
            raise AssertionFailed(f"url {page.url!r} does not contain {needle!r}")
        return None

    el, used = resolve(page, step["locators"], timeout_ms)
    if action == "fill":
        el.fill(expand(step["value"]))
    elif action == "click":
        el.click()
    elif action == "expect_text":
        want, got = expand(step["value"]), (el.inner_text() or "").strip()
        if want not in got:
            raise AssertionFailed(f"expected {want!r} in {got!r}")
    elif action == "expect_visible":
        pass  # resolve() already proved visibility
    else:
        raise SystemExit(f"unknown action {action!r}")
    return used


def guard(journey, allow_mutation):
    """Read-only by default: a journey that changes shared state needs an explicit flag."""
    mutating = journey.get("readOnly") is not True or any(s.get("mutates") for s in journey["steps"])
    if mutating and not allow_mutation:
        print(f"BLOCKED: '{journey['name']}' is not readOnly. Re-run with --allow-mutation "
              "only after agreeing to that write on this environment.", file=sys.stderr)
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("journey", type=Path)
    ap.add_argument("--allow-mutation", action="store_true")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--timeout-ms", type=int, default=4000)
    ap.add_argument("--report", type=Path, help="write a JSON report of every step")
    args = ap.parse_args()

    journey = json.loads(args.journey.read_text(encoding="utf-8"))
    if not guard(journey, args.allow_mutation):
        return BLOCKED

    results, code = [], PASS
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_context(viewport={"width": 1280, "height": 720}).new_page()
        for n, step in enumerate(journey["steps"], 1):
            label = step.get("note") or step["action"]
            started = time.time()
            try:
                used = run_step(page, step, args.timeout_ms)
                status = "pass"
                # A fallback locator that worked means the primary went stale: flag it.
                if used:
                    status = f"pass (fallback locator #{used} used, primary is stale)"
            except AssertionFailed as e:
                status, code = f"ASSERTION FAILED: {e}", ASSERT_FAIL
            except LocatorExhausted as e:
                status, code = f"LOCATOR-EXHAUSTED: {e}", LOCATOR_EXHAUSTED
            results.append({"step": n, "what": label, "status": status,
                            "seconds": round(time.time() - started, 2)})
            print(f"{n:>2}. {label:<42} {status}")
            if code != PASS:
                break
        browser.close()

    if args.report:
        args.report.write_text(json.dumps({"journey": journey["name"], "exitCode": code,
                                           "steps": results}, indent=2), encoding="utf-8")
    print("RESULT:", {PASS: "PASS", ASSERT_FAIL: "ASSERTION FAILED", LOCATOR_EXHAUSTED: "LOCATOR-EXHAUSTED"}[code])
    return code


if __name__ == "__main__":
    sys.exit(main())
