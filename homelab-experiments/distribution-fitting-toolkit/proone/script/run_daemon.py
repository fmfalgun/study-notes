#!/usr/bin/env python3
"""Entry point for the resilient telemetry daemon — run this directly, from any directory.

Usage:
  python3 run_daemon.py                  # default 60s sampling interval
  python3 run_daemon.py --interval 30    # override the interval, in seconds

To survive a closed terminal on ProOne, launch it with your shell's own backgrounding, e.g.:
  nohup python3 run_daemon.py > /dev/null 2>&1 &

Stop it with `kill <pid>` (SIGTERM) or Ctrl+C (SIGINT) — both are handled for a clean shutdown
rather than an abrupt kill mid-write.
"""

import argparse

import sampling_daemon


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--interval", type=float, default=sampling_daemon.DEFAULT_INTERVAL_SECONDS,
        help=f"Sampling interval in seconds (default: {sampling_daemon.DEFAULT_INTERVAL_SECONDS})",
    )
    args = parser.parse_args()
    sampling_daemon.run(args.interval)


if __name__ == "__main__":
    main()
