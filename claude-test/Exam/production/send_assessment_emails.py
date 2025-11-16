#!/usr/bin/env python3
"""
Production-Ready Automated Email Sender for Technical Assessment
Sends personalized HTML emails to all candidates
"""

import csv
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sys

# ==================== CONFIGURATION ====================

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'vinodyellagonda@paragroup.com'  # CHANGE THIS to your Gmail
SENDER_PASSWORD = ''  # SET THIS - Use App Password (see instructions below)
SENDER_NAME = 'Vinod Yellagonda - Semantic Data Services'

# Assessment Details
EXAM_URL = 'https://semanticservices.netlify.app'
COURSE_NAME = 'Python & SQL Technical Assessment'
START_DATE = 'November 05, 2025 at 9:00 AM EST'
END_DATE = 'November 07, 2025 at 11:59 PM EST'
ORGANIZATION = 'Semantic Data Services'
YOUR_NAME = 'Vinod Yellagonda'
YOUR_TITLE = 'Team Member'
CONTACT_EMAIL = 'careers@semanticdataservices.com'

# File Paths
CANDIDATES_CSV = 'candidates.csv'
LOG_FILE = 'email_sending_log.txt'
SENT_EMAILS_LOG = 'sent_emails.txt'

# Rate Limiting (to avoid Gmail limits)
EMAILS_PER_BATCH = 10
DELAY_BETWEEN_EMAILS = 2  # seconds
DELAY_BETWEEN_BATCHES = 60  # seconds (1 minute)

# ==================== HTML EMAIL TEMPLATE ====================

def get_email_html(candidate_name):
    """Generate personalized HTML email for candidate"""

    # Extract first name from full name
    first_name = candidate_name.split()[0] if candidate_name else "Student"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical Assessment Invitation</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 700px; margin: 0 auto; padding: 20px; background-color: #f4f4f4;">

    <!-- Header -->
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
        <h1 style="margin: 0; font-size: 28px;">📝 Technical Assessment Invitation</h1>
        <p style="margin: 10px 0 0 0; font-size: 16px;">Your evaluation is ready to begin</p>
    </div>

    <!-- Main Content -->
    <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

        <p style="font-size: 16px;">Dear <strong>{first_name}</strong>,</p>

        <p>Thank you for applying for an internship position at <strong>{ORGANIZATION}</strong>. As the next step in our selection process, you are required to complete a comprehensive technical assessment.</p>

        <!-- Assessment Details Box -->
        <div style="background: #f8f9fa; border-left: 4px solid #667eea; padding: 20px; margin: 25px 0; border-radius: 5px;">
            <h2 style="margin-top: 0; color: #667eea; font-size: 20px;">📝 Assessment Details</h2>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; font-weight: bold; width: 180px;">Assessment Type:</td>
                    <td style="padding: 8px 0;">Technical Skills Evaluation</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold;">Topics Covered:</td>
                    <td style="padding: 8px 0;">Python Programming & SQL Database</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold;">Duration:</td>
                    <td style="padding: 8px 0; color: #e74c3c;"><strong>90 Minutes</strong></td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold;">Question Types:</td>
                    <td style="padding: 8px 0;">MCQs & Coding Challenges</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold;">Available From:</td>
                    <td style="padding: 8px 0;">{START_DATE}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; font-weight: bold;">Deadline:</td>
                    <td style="padding: 8px 0; color: #e74c3c;"><strong>{END_DATE}</strong></td>
                </tr>
            </table>
        </div>

        <!-- CTA Button -->
        <div style="text-align: center; margin: 30px 0;">
            <a href="{EXAM_URL}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-size: 18px; font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                🚀 Start Assessment Now
            </a>
        </div>

        <!-- Login Credentials -->
        <div style="background: #fff3cd; border: 2px solid #ffc107; padding: 15px; margin: 25px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #856404;">🔐 Your Login Credentials</h3>
            <p style="margin: 5px 0;"><strong>Email:</strong> Use your registered email address</p>
            <p style="margin: 5px 0;"><strong>Password:</strong> Will be provided in the login page</p>
            <p style="margin: 10px 0 0 0; font-size: 14px; color: #856404;">⚠️ If you encounter any login issues, contact us immediately at {CONTACT_EMAIL}</p>
        </div>

        <!-- Technical Requirements -->
        <div style="margin: 25px 0;">
            <h2 style="color: #667eea; font-size: 20px;">💻 Technical Requirements</h2>
            <ul style="padding-left: 20px;">
                <li style="margin: 8px 0;">✅ <strong>Stable Internet Connection</strong> (minimum 2 Mbps)</li>
                <li style="margin: 8px 0;">✅ <strong>Modern Web Browser</strong> (Chrome, Firefox, Edge, Safari - latest version)</li>
                <li style="margin: 8px 0;">✅ <strong>Working Webcam</strong> (camera monitoring enabled)</li>
                <li style="margin: 8px 0;">✅ <strong>Quiet Environment</strong> (minimize distractions)</li>
                <li style="margin: 8px 0;">✅ <strong>Fully Charged Device</strong> or power supply</li>
            </ul>
        </div>

        <!-- Security Guidelines -->
        <div style="background: #f8d7da; border: 2px solid #dc3545; padding: 15px; margin: 25px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #721c24;">⚠️ Important Security Guidelines</h3>
            <ul style="padding-left: 20px; margin: 10px 0;">
                <li style="margin: 8px 0;">🔴 <strong>Camera Monitoring:</strong> Recording throughout the exam</li>
                <li style="margin: 8px 0;">🔴 <strong>Browser Monitoring:</strong> Tab switching is tracked</li>
                <li style="margin: 8px 0;">🔴 <strong>DevTools Detection:</strong> F12/Developer Tools prohibited</li>
                <li style="margin: 8px 0;">🔴 <strong>Time Limit:</strong> Strictly 90 minutes - no extensions</li>
                <li style="margin: 8px 0;">🔴 <strong>Single Attempt:</strong> ONE attempt only</li>
            </ul>
            <p style="margin: 10px 0 0 0; color: #721c24; font-weight: bold;">Any violation may result in automatic disqualification.</p>
        </div>

        <!-- How to Start -->
        <div style="margin: 25px 0;">
            <h2 style="color: #667eea; font-size: 20px;">🚀 How to Start</h2>
            <ol style="padding-left: 20px;">
                <li style="margin: 10px 0;">Click the "Start Assessment Now" button above</li>
                <li style="margin: 10px 0;">Enter your registered email address</li>
                <li style="margin: 10px 0;">Complete the login process</li>
                <li style="margin: 10px 0;">Allow camera permissions when prompted</li>
                <li style="margin: 10px 0;">Read all instructions carefully</li>
                <li style="margin: 10px 0;">Click "Start Examination" when ready</li>
                <li style="margin: 10px 0;">Answer all questions to the best of your ability</li>
                <li style="margin: 10px 0;">Click "Submit Exam" when finished</li>
            </ol>
        </div>

        <!-- Tips for Success -->
        <div style="background: #d1ecf1; border-left: 4px solid #17a2b8; padding: 15px; margin: 25px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #0c5460;">💡 Tips for Success</h3>
            <ul style="padding-left: 20px; margin: 10px 0;">
                <li style="margin: 8px 0;">Complete the assessment in one sitting (90 minutes)</li>
                <li style="margin: 8px 0;">Test your internet connection beforehand</li>
                <li style="margin: 8px 0;">Choose a quiet, well-lit environment</li>
                <li style="margin: 8px 0;">Read each question carefully</li>
                <li style="margin: 8px 0;">Manage your time wisely across all questions</li>
                <li style="margin: 8px 0;">Submit at least 5 minutes before the deadline</li>
            </ul>
        </div>

        <!-- Support -->
        <div style="background: #e7f3ff; border-left: 4px solid #2196F3; padding: 15px; margin: 25px 0; border-radius: 5px;">
            <h3 style="margin-top: 0; color: #0d47a1;">🆘 Need Help?</h3>
            <p style="margin: 5px 0;"><strong>📧 Email:</strong> {CONTACT_EMAIL}</p>
            <p style="margin: 10px 0 0 0;">Contact us BEFORE your deadline if you experience technical difficulties.</p>
        </div>

        <!-- Closing -->
        <p style="margin-top: 30px;">We wish you the very best in your assessment. This is your opportunity to demonstrate the skills and knowledge you've acquired. Approach it with confidence!</p>

        <p style="margin-top: 20px;">
            <strong>Best regards,</strong><br>
            {YOUR_NAME}<br>
            {YOUR_TITLE}<br>
            {ORGANIZATION}<br>
            {CONTACT_EMAIL}
        </p>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

        <p style="font-size: 13px; color: #666; text-align: center;">
            <em>P.S. Don't forget to check your spam/junk folder if you don't see the confirmation email after submission.</em>
        </p>

    </div>

    <!-- Footer -->
    <div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
        <p>This is an automated message regarding your internship application.</p>
        <p>&copy; 2025 {ORGANIZATION}. All rights reserved.</p>
    </div>

</body>
</html>"""

    return html


def get_email_subject():
    """Generate email subject line"""
    return f"Action Required: Complete Your Technical Assessment - {ORGANIZATION}"


def log_message(message, level='INFO'):
    """Log messages to console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"

    print(log_entry)

    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '\n')


def load_candidates():
    """Load candidates from CSV file"""
    candidates = []

    try:
        with open(CANDIDATES_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append({
                    'name': row['Name'].strip(),
                    'email': row['Email'].strip().lower()
                })

        log_message(f"✅ Loaded {len(candidates)} candidates from {CANDIDATES_CSV}")
        return candidates

    except FileNotFoundError:
        log_message(f"❌ ERROR: {CANDIDATES_CSV} not found!", 'ERROR')
        sys.exit(1)
    except Exception as e:
        log_message(f"❌ ERROR loading candidates: {str(e)}", 'ERROR')
        sys.exit(1)


def load_already_sent():
    """Load list of emails that have already been sent"""
    if not os.path.exists(SENT_EMAILS_LOG):
        return set()

    with open(SENT_EMAILS_LOG, 'r') as f:
        return set(line.strip().lower() for line in f)


def mark_as_sent(email):
    """Mark email as sent"""
    with open(SENT_EMAILS_LOG, 'a') as f:
        f.write(email.lower() + '\n')


def send_email(candidate, smtp_connection):
    """Send email to a single candidate"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
        msg['To'] = candidate['email']
        msg['Subject'] = get_email_subject()

        # Attach HTML content
        html_content = get_email_html(candidate['name'])
        msg.attach(MIMEText(html_content, 'html'))

        # Send email
        smtp_connection.send_message(msg)

        log_message(f"✅ Sent to: {candidate['name']} <{candidate['email']}>")
        mark_as_sent(candidate['email'])

        return True

    except Exception as e:
        log_message(f"❌ FAILED to send to {candidate['email']}: {str(e)}", 'ERROR')
        return False


def send_all_emails():
    """Main function to send emails to all candidates"""

    log_message("=" * 80)
    log_message("📧 STARTING AUTOMATED EMAIL CAMPAIGN")
    log_message("=" * 80)

    # Check if sender password is set
    if not SENDER_PASSWORD:
        log_message("❌ ERROR: SENDER_PASSWORD not set in configuration!", 'ERROR')
        log_message("Please set your Gmail App Password in the script configuration.", 'ERROR')
        log_message("See instructions at the top of this script.", 'ERROR')
        sys.exit(1)

    # Load candidates
    candidates = load_candidates()
    already_sent = load_already_sent()

    # Filter out already sent
    pending_candidates = [c for c in candidates if c['email'] not in already_sent]

    if not pending_candidates:
        log_message("✅ All emails have already been sent!")
        return

    log_message(f"📊 Total candidates: {len(candidates)}")
    log_message(f"✅ Already sent: {len(already_sent)}")
    log_message(f"📤 Pending to send: {len(pending_candidates)}")
    log_message("")

    # Connect to SMTP server
    try:
        log_message(f"🔌 Connecting to {SMTP_SERVER}...")
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        log_message("✅ SMTP connection established")
        log_message("")
    except Exception as e:
        log_message(f"❌ SMTP connection failed: {str(e)}", 'ERROR')
        log_message("Check your email/password and internet connection.", 'ERROR')
        sys.exit(1)

    # Send emails in batches
    total_sent = 0
    total_failed = 0

    for i, candidate in enumerate(pending_candidates):
        # Send email
        success = send_email(candidate, smtp)

        if success:
            total_sent += 1
        else:
            total_failed += 1

        # Rate limiting
        if (i + 1) % EMAILS_PER_BATCH == 0 and (i + 1) < len(pending_candidates):
            log_message(f"⏸️  Batch complete ({i + 1}/{len(pending_candidates)}). Waiting {DELAY_BETWEEN_BATCHES}s before next batch...")
            time.sleep(DELAY_BETWEEN_BATCHES)
        else:
            time.sleep(DELAY_BETWEEN_EMAILS)

    # Close SMTP connection
    smtp.quit()
    log_message("")
    log_message("=" * 80)
    log_message("📧 EMAIL CAMPAIGN COMPLETE")
    log_message("=" * 80)
    log_message(f"✅ Successfully sent: {total_sent}")
    log_message(f"❌ Failed: {total_failed}")
    log_message(f"📊 Total processed: {len(pending_candidates)}")
    log_message("")
    log_message(f"📝 Full log saved to: {LOG_FILE}")
    log_message(f"✅ Sent emails log: {SENT_EMAILS_LOG}")


def send_test_email():
    """Send a test email to yourself first"""
    log_message("=" * 80)
    log_message("🧪 SENDING TEST EMAIL TO YOURSELF")
    log_message("=" * 80)

    if not SENDER_PASSWORD:
        log_message("❌ ERROR: SENDER_PASSWORD not set!", 'ERROR')
        sys.exit(1)

    try:
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send test email
        test_candidate = {
            'name': 'Test Candidate',
            'email': SENDER_EMAIL  # Send to yourself
        }

        send_email(test_candidate, smtp)
        smtp.quit()

        log_message("")
        log_message("✅ Test email sent successfully!")
        log_message(f"Check your inbox at: {SENDER_EMAIL}")
        log_message("")
        log_message("If the email looks good, run: python3 send_assessment_emails.py --send-all")

    except Exception as e:
        log_message(f"❌ Test email failed: {str(e)}", 'ERROR')
        sys.exit(1)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send assessment emails to candidates')
    parser.add_argument('--test', action='store_true', help='Send test email to yourself')
    parser.add_argument('--send-all', action='store_true', help='Send emails to all candidates')
    parser.add_argument('--config-check', action='store_true', help='Check configuration')

    args = parser.parse_args()

    if args.config_check:
        print("\n" + "=" * 80)
        print("📋 CONFIGURATION CHECK")
        print("=" * 80)
        print(f"SMTP Server:      {SMTP_SERVER}:{SMTP_PORT}")
        print(f"Sender Email:     {SENDER_EMAIL}")
        print(f"Password Set:     {'✅ Yes' if SENDER_PASSWORD else '❌ No - REQUIRED!'}")
        print(f"Exam URL:         {EXAM_URL}")
        print(f"Start Date:       {START_DATE}")
        print(f"End Date:         {END_DATE}")
        print(f"Organization:     {ORGANIZATION}")
        print(f"Contact Email:    {CONTACT_EMAIL}")
        print(f"Candidates File:  {CANDIDATES_CSV} {'✅ Found' if os.path.exists(CANDIDATES_CSV) else '❌ Not Found'}")
        print("=" * 80 + "\n")

        if os.path.exists(CANDIDATES_CSV):
            candidates = load_candidates()
            print(f"Total candidates to email: {len(candidates)}\n")

    elif args.test:
        send_test_email()

    elif args.send_all:
        confirm = input("\n⚠️  You are about to send emails to 55 candidates. Continue? (yes/no): ")
        if confirm.lower() == 'yes':
            send_all_emails()
        else:
            print("Cancelled.")

    else:
        parser.print_help()
        print("\n" + "=" * 80)
        print("🚀 QUICK START GUIDE")
        print("=" * 80)
        print("1. Set SENDER_PASSWORD in the script (Gmail App Password)")
        print("2. Run configuration check:")
        print("   python3 send_assessment_emails.py --config-check")
        print("")
        print("3. Send test email to yourself:")
        print("   python3 send_assessment_emails.py --test")
        print("")
        print("4. If test looks good, send to all candidates:")
        print("   python3 send_assessment_emails.py --send-all")
        print("=" * 80 + "\n")
