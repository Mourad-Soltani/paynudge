"""
PayNudge CLI
Author: Mourad.Soltani
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .generator import process_invoices
from . import __version__


def main():
    parser = argparse.ArgumentParser(
        description="PayNudge - Generate tiered payment reminder emails from invoice CSV. By Mourad.Soltani"
    )
    parser.add_argument("csv_file", help="Path to CSV file with columns: client,amount,invoice_id,due_date,email")
    parser.add_argument("--output", "-o", help="Output file (JSON). Default: stdout")
    parser.add_argument("--today", help="Override today's date (YYYY-MM-DD) for testing")
    parser.add_argument("--version", action="version", version=f"PayNudge {__version__}")
    args = parser.parse_args()

    today = None
    if args.today:
        today = date.fromisoformat(args.today)

    if not Path(args.csv_file).exists():
        print(f"Error: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    results = process_invoices(args.csv_file, today=today)

    output = json.dumps(results, indent=2, default=str)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {len(results)} reminders to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
