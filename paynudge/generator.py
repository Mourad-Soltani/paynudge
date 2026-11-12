"""
PayNudge Generator - Core logic for reminder tiers
Author: Mourad.Soltani
"""

from datetime import datetime, date
from typing import Dict, List, Optional
import csv


def parse_due_date(due_str: str) -> date:
    """Parse due date from common formats."""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(due_str.strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {due_str}")


def days_overdue(due: date, today: Optional[date] = None) -> int:
    """Calculate days overdue. Negative if not yet due."""
    if today is None:
        today = date.today()
    return (today - due).days


def get_tier(days: int) -> str:
    """Determine reminder tier based on days overdue."""
    if days < 0:
        return "upcoming"
    elif days <= 7:
        return "gentle"
    elif days <= 21:
        return "firm"
    else:
        return "final"


def generate_subject(tier: str, client: str, invoice_id: str) -> str:
    """Generate email subject based on tier."""
    subjects = {
        "upcoming": f"Upcoming Invoice {invoice_id} for {client}",
        "gentle": f"Friendly Reminder: Invoice {invoice_id} - {client}",
        "firm": f"Payment Reminder: Invoice {invoice_id} is Overdue - {client}",
        "final": f"Final Notice: Invoice {invoice_id} - Immediate Payment Required - {client}",
    }
    return subjects.get(tier, f"Invoice {invoice_id} Reminder")


def generate_body(tier: str, client: str, amount: str, invoice_id: str, due: str, days: int) -> str:
    """Generate email body based on tier."""
    if tier == "upcoming":
        return f"""Hi {client},

This is a friendly heads-up that invoice {invoice_id} for {amount} is due on {due}.

Please let me know if you have any questions.

Best regards,
[Your Name]"""
    elif tier == "gentle":
        return f"""Hi {client},

I hope you're doing well. This is a gentle reminder that invoice {invoice_id} for {amount} was due on {due} ({abs(days)} days ago).

Could you please confirm when payment will be sent?

Thank you,
[Your Name]"""
    elif tier == "firm":
        return f"""Hi {client},

I'm following up on invoice {invoice_id} for {amount}, which was due on {due} and is now {days} days overdue.

Please arrange payment at your earliest convenience. Let me know if there's any issue.

Best,
[Your Name]"""
    else:  # final
        return f"""Hi {client},

This is a final notice regarding invoice {invoice_id} for {amount}, due on {due} and now {days} days overdue.

Payment is required immediately. Please contact me if there are any problems so we can resolve this promptly.

Regards,
[Your Name]"""


def process_invoices(csv_path: str, today: Optional[date] = None) -> List[Dict]:
    """Process CSV and generate reminders."""
    if today is None:
        today = date.today()
    results = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                client = row.get("client", "").strip()
                amount = row.get("amount", "").strip()
                invoice_id = row.get("invoice_id", "").strip()
                due_str = row.get("due_date", "").strip()
                email = row.get("email", "").strip()
                if not all([client, amount, invoice_id, due_str]):
                    continue
                due = parse_due_date(due_str)
                days = days_overdue(due, today)
                tier = get_tier(days)
                subject = generate_subject(tier, client, invoice_id)
                body = generate_body(tier, client, amount, invoice_id, due_str, days)
                results.append({
                    "client": client,
                    "email": email,
                    "invoice_id": invoice_id,
                    "amount": amount,
                    "due_date": due_str,
                    "days_overdue": days,
                    "tier": tier,
                    "subject": subject,
                    "body": body,
                })
            except Exception as e:
                results.append({"error": str(e), "row": row})
    return results
