#!/usr/bin/env python3

import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from typing import Optional


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Send an email through Gmail SMTP using an App Password."
    )
    parser.add_argument("--to", required=True, help="Recipient email address.")
    parser.add_argument("--subject", required=True, help="Email subject line.")
    parser.add_argument(
        "--body-file",
        default=None,
        help="Path to a UTF-8 plain-text file to use as the message body.",
    )
    parser.add_argument(
        "--html-file",
        default=None,
        help="Optional path to a UTF-8 HTML file to attach as the rich-text body.",
    )
    parser.add_argument(
        "--from-name",
        default="Onyx Analytix Automation",
        help="Display name for the From header.",
    )
    parser.add_argument(
        "--reply-to",
        default=None,
        help="Optional Reply-To address.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved message metadata without sending.",
    )
    return parser


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value.strip()


def sanitize_header_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.replace("\r", " ").replace("\n", " ").strip()
    return cleaned or None


def build_message(
    sender_email: str,
    recipient_email: str,
    subject: str,
    from_name: str,
    reply_to: Optional[str],
    body: str,
    html_body: Optional[str],
) -> EmailMessage:
    msg = EmailMessage()
    safe_sender_email = sanitize_header_value(sender_email)
    safe_recipient_email = sanitize_header_value(recipient_email)
    safe_subject = sanitize_header_value(subject)
    safe_from_name = sanitize_header_value(from_name)
    safe_reply_to = sanitize_header_value(reply_to)

    if not safe_sender_email or not safe_recipient_email or not safe_subject or not safe_from_name:
        raise SystemExit("Email headers contain missing or invalid values after sanitization.")

    msg["From"] = f"{safe_from_name} <{safe_sender_email}>"
    msg["To"] = safe_recipient_email
    msg["Subject"] = safe_subject
    if safe_reply_to:
        msg["Reply-To"] = safe_reply_to
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")
    return msg


def send_message(sender_email: str, app_password: str, msg: EmailMessage) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    sender_email = require_env("GMAIL_SMTP_EMAIL")
    app_password = require_env("GMAIL_APP_PASSWORD")

    if not args.body_file and not args.html_file:
        raise SystemExit("Provide --body-file, --html-file, or both.")

    body_path = Path(args.body_file).expanduser().resolve() if args.body_file else None
    html_path = Path(args.html_file).expanduser().resolve() if args.html_file else None

    if body_path and not body_path.is_file():
        raise SystemExit(f"Body file not found: {body_path}")
    if html_path and not html_path.is_file():
        raise SystemExit(f"HTML file not found: {html_path}")

    body = body_path.read_text(encoding="utf-8") if body_path else "HTML version attached."
    html_body = html_path.read_text(encoding="utf-8") if html_path else None
    msg = build_message(
        sender_email=sender_email,
        recipient_email=args.to,
        subject=args.subject,
        from_name=args.from_name,
        reply_to=args.reply_to,
        body=body,
        html_body=html_body,
    )

    if args.dry_run:
        print(f"From: {msg['From']}")
        print(f"To: {msg['To']}")
        print(f"Subject: {msg['Subject']}")
        if msg.get("Reply-To"):
            print(f"Reply-To: {msg['Reply-To']}")
        if body_path:
            print(f"Body file: {body_path}")
        if html_path:
            print(f"HTML file: {html_path}")
        print("Dry run only. No email sent.")
        return

    send_message(sender_email=sender_email, app_password=app_password, msg=msg)
    print(f"Email sent to {args.to}")


if __name__ == "__main__":
    main()
