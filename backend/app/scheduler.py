import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date
from app.database import SessionLocal
from app.models import FollowUp


GMAIL_SENDER = os.getenv("GMAIL_SENDER", "")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://your-app.vercel.app")


def send_email(to_address: str, subject: str, html_body: str):
    """Send an HTML email via Gmail SMTP. Silently skips if credentials not set."""
    if not GMAIL_SENDER or not GMAIL_PASSWORD:
        print("⚠️  Email not configured — set GMAIL_SENDER and GMAIL_PASSWORD in .env")
        return
    if not to_address:
        print("⚠️  No recipient email address — skipping")
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = GMAIL_SENDER
        msg["To"] = to_address
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_SENDER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_SENDER, to_address, msg.as_string())

        print(f"✅ Reminder email sent to {to_address}")

    except Exception as e:
        print(f"❌ Failed to send email to {to_address}: {e}")


def build_email_html(due_followups) -> str:
    """Build a clean HTML email listing all due follow-ups."""
    rows = ""
    for f in due_followups:
        app = f.application
        days_overdue = (date.today() - f.followup_date).days
        overdue_text = (
            f'<span style="color:#f87171">({days_overdue}d overdue)</span>'
            if days_overdue > 0 else
            '<span style="color:#fbbf24">Due today</span>'
        )
        rows += f"""
        <tr style="border-bottom:1px solid #252a3a;">
          <td style="padding:12px 16px;font-weight:700;color:#e2e8f0">{app.company}</td>
          <td style="padding:12px 16px;color:#94a3b8">{app.role}</td>
          <td style="padding:12px 16px;color:#94a3b8;font-family:monospace">{f.followup_date}</td>
          <td style="padding:12px 16px">{overdue_text}</td>
        </tr>"""

    count = len(due_followups)
    return f"""
    <div style="font-family:'Segoe UI',sans-serif;background:#0d0f14;padding:32px;border-radius:12px;max-width:600px;margin:0 auto">
      <div style="margin-bottom:24px">
        <div style="font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,#1ab3d4,#3dd68c);-webkit-background-clip:text;-webkit-text-fill-color:transparent">APPLYT</div>
        <div style="font-size:0.85rem;color:#64748b;margin-top:4px">Follow-up Reminders</div>
      </div>

      <div style="background:#1a1e2a;border:1px solid #252a3a;border-radius:10px;padding:20px;margin-bottom:20px">
        <div style="font-size:1rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">
          ⏰ You have <span style="color:#fbbf24">{count} follow-up{'s' if count > 1 else ''}</span> due
        </div>
        <div style="font-size:0.82rem;color:#64748b">Don't let these opportunities slip away!</div>
      </div>

      <table style="width:100%;border-collapse:collapse;background:#1a1e2a;border:1px solid #252a3a;border-radius:10px;overflow:hidden">
        <thead>
          <tr style="background:#1f2433">
            <th style="padding:10px 16px;text-align:left;font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Company</th>
            <th style="padding:10px 16px;text-align:left;font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Role</th>
            <th style="padding:10px 16px;text-align:left;font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Due Date</th>
            <th style="padding:10px 16px;text-align:left;font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Status</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>

      <div style="margin-top:24px;text-align:center">
        <a href="{FRONTEND_URL}" style="background:#4f8ef7;color:#fff;text-decoration:none;padding:10px 24px;border-radius:8px;font-weight:700;font-size:0.85rem">
          Open Applyt →
        </a>
      </div>

      <div style="margin-top:24px;font-size:0.72rem;color:#64748b;text-align:center">
        Sent by APPLYT • {date.today().strftime('%B %d, %Y')}
      </div>
    </div>"""


def followup_checker():
    """
    Check for due follow-ups grouped by user and send each user their own reminder email.

    Uses Firebase Auth email as the recipient — only users who signed up with Google
    (which provides an email) will receive emails. Phone-only users are skipped.
    """
    db = SessionLocal()
    today = date.today()

    try:
        due_followups = (
            db.query(FollowUp)
            .filter(
                FollowUp.followup_date <= today,
                FollowUp.sent == False  
            )
            .all()
        )

        if not due_followups:
            print(f"✅ No follow-ups due today ({today})")
            return

        for f in due_followups:
            _ = f.application

        by_user: dict[str, list] = {}
        for f in due_followups:
            uid = f.application.user_id
            by_user.setdefault(uid, []).append(f)

        print(f"⏰ {len(due_followups)} follow-up(s) due across {len(by_user)} user(s)")

        try:
            from firebase_admin import auth as firebase_auth
            for uid, followups in by_user.items():
                try:
                    user_record = firebase_auth.get_user(uid)
                    recipient   = user_record.email  
                except Exception:
                    recipient = None

                if not recipient:
                    print(f"⚠️  No email for uid={uid} — skipping reminder")
                    continue

                subject = (
                    f"⏰ APPLYT: {len(followups)} follow-up reminder"
                    f"{'s' if len(followups) > 1 else ''} due today"
                )
                html = build_email_html(followups)
                send_email(recipient, subject, html)

        except Exception as e:
            print(f"❌ Firebase lookup failed: {e}")

    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler. Called from main.py on startup."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(followup_checker, "cron", hour=8, minute=0)
    scheduler.add_job(followup_checker, "date", run_date=None)
    scheduler.start()
    print("🕐 Follow-up scheduler started (runs daily at 08:00)")
    return scheduler
