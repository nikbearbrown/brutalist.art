#!/usr/bin/env python3
"""Open a headed Chromium at the hub so the HUMAN signs in, then save the
session (Playwright storageState) OUTSIDE any reel. The agent never types
credentials; this script only waits for /dashboard or /admin to appear."""
import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

DEFAULT_STATE = Path.home() / '.medhavy-walkthrough' / 'brutalist-session.json'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='https://hub.medhavy.com/sign-in')
    parser.add_argument('--state', type=Path, default=DEFAULT_STATE,
                        help=f'where to save the session (default {DEFAULT_STATE})')
    parser.add_argument('--timeout-s', type=int, default=600)
    args = parser.parse_args()
    args.state.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        page.goto(args.url)
        print('Sign in as the walkthrough account in the window that opened.', flush=True)
        page.wait_for_url(lambda u: '/dashboard' in u or '/admin' in u or '/onboarding' in u,
                          timeout=args.timeout_s * 1000)
        context.storage_state(path=str(args.state))
        browser.close()
    args.state.chmod(0o600)
    print(f'Session saved to {args.state} (mode 600). Keep it out of the reel and out of git.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
