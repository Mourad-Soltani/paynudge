"""
Tests for PayNudge generator
Author: Mourad.Soltani
"""

import pytest
from datetime import date
from paynudge.generator import (
    parse_due_date,
    days_overdue,
    get_tier,
    generate_subject,
    generate_body,
    process_invoices,
)
import tempfile
import csv
from pathlib import Path


def test_parse_due_date():
    assert parse_due_date("2026-11-01") == date(2026, 11, 1)
    assert parse_due_date("01/11/2026") == date(2026, 11, 1)
    with pytest.raises(ValueError):
        parse_due_date("invalid")


def test_days_overdue():
    today = date(2026, 11, 12)
    due = date(2026, 11, 1)
    assert days_overdue(due, today) == 11
    due_future = date(2026, 11, 20)
    assert days_overdue(due_future, today) == -8


def test_get_tier():
    assert get_tier(-5) == "upcoming"
    assert get_tier(3) == "gentle"
    assert get_tier(15) == "firm"
    assert get_tier(30) == "final"


def test_generate_subject():
    subj = generate_subject("gentle", "Acme Corp", "INV-001")
    assert "INV-001" in subj
    assert "Acme Corp" in subj


def test_generate_body():
    body = generate_body("firm", "Acme", "$500", "INV-001", "2026-11-01", 10)
    assert "INV-001" in body
    assert "10 days overdue" in body


def test_process_invoices(tmp_path):
    csv_path = tmp_path / "invoices.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["client", "amount", "invoice_id", "due_date", "email"])
        writer.writerow(["Acme", "$500", "INV-001", "2026-11-01", "billing@acme.com"])
        writer.writerow(["Beta", "$200", "INV-002", "2026-11-20", "pay@beta.com"])

    results = process_invoices(str(csv_path), today=date(2026, 11, 12))
    assert len(results) == 2
    assert results[0]["tier"] == "firm"
    assert results[1]["tier"] == "upcoming"
    assert "error" not in results[0]
