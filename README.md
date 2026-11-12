# PayNudge

Minimal CLI tool that generates tiered payment reminder emails for freelancers from a simple CSV of invoices.

**Author: Mourad.Soltani**

## Why
Freelancers lose money chasing late payments. This tool turns your invoice list into ready-to-send reminder emails with appropriate tone based on how overdue each invoice is.

## Features
- Reads CSV (client, amount, invoice_id, due_date, email)
- Calculates days overdue
- Generates 4 tiers: upcoming / gentle / firm / final
- Outputs JSON with subject + body for each
- Zero external dependencies beyond Python stdlib
- Health tests included

## Quick Start
```bash
cd paynudge
python -m paynudge.cli examples/sample_invoices.csv --today 2026-11-12
```

Or install editable:
```bash
pip install -e .
paynudge examples/sample_invoices.csv
```

## CSV Format
```
client,amount,invoice_id,due_date,email
Acme Corp,$1500,INV-2026-042,2026-11-01,accounts@acme.com
```

Supported date formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY

## Output
JSON array of reminder objects ready to copy into your email client.

## Tests
```bash
pip install pytest
pytest tests/ -v
```

## License
MIT - Mourad.Soltani
