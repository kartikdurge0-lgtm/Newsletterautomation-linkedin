# Gmail SMTP Setup For Weekly Brief

## 1. Turn on Google 2-Step Verification
App Passwords require 2-Step Verification on the Google account. Google documents that here:
- [Sign in with app passwords](https://support.google.com/accounts/answer/185833)

## 2. Create an App Password
Use the Google Account App Passwords page and create one password dedicated to this automation.

## 3. Create your local env file
Copy [.env.gmail.example](/Users/kartikdurge/Documents/Onyx%20Linkedin/.env.gmail.example) to `.env.gmail` in this folder and fill in:

```bash
GMAIL_SMTP_EMAIL=yourpersonalgmail@gmail.com
GMAIL_APP_PASSWORD=your16digitapppassword
```

Optional:

```bash
REPLY_TO=yourpreferredreplyto@gmail.com
FROM_NAME=Onyx Analytix Automation
RECIPIENT=kartikdurgebharatrath@gmail.com
```

## 4. Dry-run the send
From this folder:

```bash
sh /Users/kartikdurge/Documents/Onyx\ Linkedin/send_latest_brief.sh --dry-run
```

## 5. Send the latest brief
```bash
sh /Users/kartikdurge/Documents/Onyx\ Linkedin/send_latest_brief.sh
```

## 6. Cron example
If you want a local cron job to send the latest generated brief every Monday at 9:35 AM:

```cron
35 9 * * 1 cd /Users/kartikdurge/Documents/Onyx\ Linkedin && /bin/sh /Users/kartikdurge/Documents/Onyx\ Linkedin/send_latest_brief.sh >> /Users/kartikdurge/Documents/Onyx\ Linkedin/send_latest_brief.log 2>&1
```

## 7. Hosted run while laptop is off
If you want the send to run when your laptop is off, use the GitHub Actions workflow at [send-weekly-brief.yml](/Users/kartikdurge/Documents/Onyx%20Linkedin/.github/workflows/send-weekly-brief.yml).

What it does:
- Runs every Monday at 04:05 UTC, which is 09:35 IST on Monday.
- Can also be triggered manually from the GitHub Actions tab.
- Writes a temporary `.env.gmail` file from GitHub repository secrets.
- Sends the latest weekly brief file committed in the repository.

Add these GitHub repository secrets:

```text
GMAIL_SMTP_EMAIL
GMAIL_APP_PASSWORD
RECIPIENT
REPLY_TO
FROM_NAME
```

Notes:
- `GMAIL_SMTP_EMAIL` and `GMAIL_APP_PASSWORD` are required.
- `RECIPIENT`, `REPLY_TO`, and `FROM_NAME` are optional, but recommended.
- This hosted workflow only sends the latest brief file available in the repo.
- It does not yet generate a new research brief remotely by itself. For full laptop-independent generation plus sending, a hosted generation step still needs to be added.

## Files
- [send_gmail_message.py](/Users/kartikdurge/Documents/Onyx%20Linkedin/send_gmail_message.py)
- [send_latest_brief.sh](/Users/kartikdurge/Documents/Onyx%20Linkedin/send_latest_brief.sh)
- [2026-07-05_onyx_analytix_weekly_commercial_pharma_brief.md](/Users/kartikdurge/Documents/Onyx%20Linkedin/2026-07-05_onyx_analytix_weekly_commercial_pharma_brief.md)
- [send-weekly-brief.yml](/Users/kartikdurge/Documents/Onyx%20Linkedin/.github/workflows/send-weekly-brief.yml)
