#!/usr/bin/env python3
"""Entry point for the validation harness — run this directly, from any directory.

Usage: python3 run_validate.py
(Python auto-adds this file's own directory to sys.path, so `distributions` resolves
regardless of your current working directory — no -m module gymnastics needed.)
"""

from distributions import validate

if __name__ == "__main__":
    validate.check_pdf_cdf()
    validate.check_mle_recovery()
