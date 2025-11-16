#!/usr/bin/env python3
"""
Email Campaign Manager
Production-ready email campaign system with configuration-based setup

Usage:
    python3 send_campaign.py [--test-email EMAIL] [--send-all] [--dry-run]

Options:
    --test-email EMAIL  Send a test email to the specified address
    --send-all          Send to all candidates in the CSV file
    --dry-run           Validate configuration without sending emails
"""

import smtplib
import csv
import json
import os
import sys
import time
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Get script directory for relative paths
SCRIPT_DIR = Path(__file__).parent.absolute()

class CampaignManager:
    def __init__(self, config_file='config.json'):
        """Initialize campaign manager with configuration"""
        self.config_path = SCRIPT_DIR / config_file
        self.log_path = None  # Will be set in setup_paths()
        self.load_config()
        self.setup_paths()
        self.smtp = None

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            self.log_message(f"✅ Configuration loaded from {self.config_path}", 'INFO')
        except FileNotFoundError:
            print(f"❌ ERROR: Configuration file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ ERROR: Invalid JSON in configuration file: {e}")
            sys.exit(1)

    def setup_paths(self):
        """Setup all file paths relative to script directory"""
        self.template_path = SCRIPT_DIR / self.config['campaign']['template_file']
        self.candidates_path = SCRIPT_DIR / self.config['campaign']['candidates_file']
        self.sent_emails_path = SCRIPT_DIR / self.config['campaign']['sent_emails_file']
        self.log_path = SCRIPT_DIR / self.config['campaign']['log_file']

        # Ensure directories exist
        self.sent_emails_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_message(self, message, level='INFO'):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"

        # Print to console
        print(log_entry)

        # Write to log file (only if log_path is set)
        if self.log_path:
            try:
                with open(self.log_path, 'a') as f:
                    f.write(log_entry + '\n')
            except Exception as e:
                print(f"⚠️  Warning: Could not write to log file: {e}")

    def validate_config(self):
        """Validate configuration and required files"""
        self.log_message("🔍 Validating configuration...", 'INFO')

        # Check SMTP configuration
        required_smtp_fields = ['server', 'port', 'sender_email', 'sender_password']
        for field in required_smtp_fields:
            if field not in self.config['smtp']:
                self.log_message(f"Missing SMTP field: {field}", 'ERROR')
                return False

        # Check template file exists
        if not self.template_path.exists():
            self.log_message(f"Template file not found: {self.template_path}", 'ERROR')
            return False

        # Check candidates file exists
        if not self.candidates_path.exists():
            self.log_message(f"Candidates file not found: {self.candidates_path}", 'ERROR')
            return False

        self.log_message("✅ Configuration validation passed", 'INFO')
        return True

    def load_email_template(self):
        """Load HTML email template from file"""
        try:
            with open(self.template_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.log_message(f"Failed to load template: {e}", 'ERROR')
            sys.exit(1)

    def personalize_template(self, template, candidate_name, candidate_email):
        """Personalize email template with candidate data and config variables"""
        # Extract first name
        first_name = candidate_name.split()[0] if candidate_name else "Student"

        # Replace all template variables
        personalized = template.replace('{{FIRST_NAME}}', first_name)
        personalized = personalized.replace('{{FULL_NAME}}', candidate_name)
        personalized = personalized.replace('{{EMAIL}}', candidate_email)

        # Replace configuration variables
        for key, value in self.config['template_variables'].items():
            personalized = personalized.replace(f'{{{{{key}}}}}', value)

        return personalized

    def load_candidates(self):
        """Load candidates from CSV file"""
        candidates = []
        try:
            with open(self.candidates_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'Name' in row and 'Email' in row:
                        candidates.append({
                            'name': row['Name'].strip(),
                            'email': row['Email'].strip()
                        })
            return candidates
        except Exception as e:
            self.log_message(f"Failed to load candidates: {e}", 'ERROR')
            sys.exit(1)

    def load_sent_emails(self):
        """Load list of already sent emails"""
        if not self.sent_emails_path.exists():
            return set()

        try:
            with open(self.sent_emails_path, 'r') as f:
                return set(line.strip() for line in f if line.strip())
        except Exception as e:
            self.log_message(f"Warning: Could not load sent emails list: {e}", 'WARNING')
            return set()

    def save_sent_email(self, email):
        """Add email to sent emails tracking file"""
        try:
            with open(self.sent_emails_path, 'a') as f:
                f.write(f"{email}\n")
        except Exception as e:
            self.log_message(f"Warning: Could not save sent email: {e}", 'WARNING')

    def connect_smtp(self):
        """Establish SMTP connection"""
        try:
            smtp_config = self.config['smtp']
            self.log_message(f"🔌 Connecting to {smtp_config['server']}:{smtp_config['port']}...", 'INFO')

            self.smtp = smtplib.SMTP(smtp_config['server'], smtp_config['port'], timeout=10)
            self.smtp.set_debuglevel(0)
            self.smtp.ehlo()

            if smtp_config.get('use_tls', True):
                self.log_message("🔐 Starting TLS encryption...", 'INFO')
                self.smtp.starttls()
                self.smtp.ehlo()

            self.log_message(f"🔑 Logging in as {smtp_config['sender_email']}...", 'INFO')
            self.smtp.login(smtp_config['sender_email'], smtp_config['sender_password'])

            self.log_message("✅ SMTP connection established", 'INFO')
            return True
        except Exception as e:
            self.log_message(f"SMTP connection failed: {e}", 'ERROR')
            return False

    def disconnect_smtp(self):
        """Close SMTP connection"""
        if self.smtp:
            try:
                self.smtp.quit()
            except:
                pass

    def reconnect_smtp(self):
        """Reconnect to SMTP server"""
        self.disconnect_smtp()
        time.sleep(2)
        return self.connect_smtp()

    def send_email(self, candidate):
        """Send email to a single candidate"""
        try:
            smtp_config = self.config['smtp']
            template = self.load_email_template()
            html_content = self.personalize_template(
                template,
                candidate['name'],
                candidate['email']
            )

            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.config['campaign']['subject']
            msg['From'] = f"{smtp_config['sender_name']} <{smtp_config['sender_email']}>"
            msg['To'] = f"{candidate['name']} <{candidate['email']}>"

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            self.smtp.sendmail(smtp_config['sender_email'], candidate['email'], msg.as_string())

            self.log_message(f"✅ Sent to: {candidate['name']} <{candidate['email']}>", 'INFO')
            self.save_sent_email(candidate['email'])

            return True

        except Exception as e:
            self.log_message(f"❌ FAILED to send to {candidate['email']}: {str(e)}", 'ERROR')
            return False

    def run_campaign(self, dry_run=False):
        """Run the email campaign"""
        self.log_message("="*80, 'INFO')
        self.log_message("📧 STARTING EMAIL CAMPAIGN", 'INFO')
        self.log_message("="*80, 'INFO')

        # Validate configuration
        if not self.validate_config():
            self.log_message("❌ Configuration validation failed", 'ERROR')
            return False

        # Load candidates
        all_candidates = self.load_candidates()
        self.log_message(f"✅ Loaded {len(all_candidates)} candidates from CSV", 'INFO')

        # Filter out already sent
        sent_emails = self.load_sent_emails()
        pending_candidates = [c for c in all_candidates if c['email'] not in sent_emails]

        self.log_message(f"📊 Total candidates: {len(all_candidates)}", 'INFO')
        self.log_message(f"✅ Already sent: {len(sent_emails)}", 'INFO')
        self.log_message(f"📤 Pending to send: {len(pending_candidates)}", 'INFO')
        self.log_message("", 'INFO')

        if len(pending_candidates) == 0:
            self.log_message("✅ All candidates have already received emails!", 'INFO')
            return True

        if dry_run:
            self.log_message("🔍 DRY RUN MODE - No emails will be sent", 'INFO')
            self.log_message(f"Would send to: {len(pending_candidates)} candidates", 'INFO')
            return True

        # Connect to SMTP
        if not self.connect_smtp():
            return False

        # Send emails
        sending_config = self.config['sending']
        total_sent = 0
        total_failed = 0
        consecutive_failures = 0

        for i, candidate in enumerate(pending_candidates):
            success = self.send_email(candidate)

            if success:
                total_sent += 1
                consecutive_failures = 0
            else:
                total_failed += 1
                consecutive_failures += 1

                # Reconnect after multiple consecutive failures
                if consecutive_failures >= sending_config['max_consecutive_failures']:
                    self.log_message("🔄 Multiple failures detected - reconnecting...", 'INFO')
                    if self.reconnect_smtp():
                        consecutive_failures = 0
                    else:
                        self.log_message("❌ Reconnection failed - stopping campaign", 'ERROR')
                        break

            # Rate limiting
            if (i + 1) % sending_config['emails_per_batch'] == 0 and (i + 1) < len(pending_candidates):
                self.log_message(f"⏸️  Batch complete ({i + 1}/{len(pending_candidates)}). Waiting {sending_config['delay_between_batches']}s...", 'INFO')

                # Disconnect before long wait
                self.disconnect_smtp()
                time.sleep(sending_config['delay_between_batches'])

                # Reconnect after wait
                if not self.reconnect_smtp():
                    self.log_message("❌ Reconnection failed - stopping campaign", 'ERROR')
                    break
            else:
                time.sleep(sending_config['delay_between_emails'])

        # Disconnect
        self.disconnect_smtp()

        # Summary
        self.log_message("", 'INFO')
        self.log_message("="*80, 'INFO')
        self.log_message("📧 EMAIL CAMPAIGN COMPLETE", 'INFO')
        self.log_message("="*80, 'INFO')
        self.log_message(f"✅ Successfully sent: {total_sent}", 'INFO')
        self.log_message(f"❌ Failed: {total_failed}", 'INFO')
        self.log_message(f"📊 Total processed: {total_sent + total_failed}", 'INFO')
        self.log_message("", 'INFO')
        self.log_message(f"📝 Full log saved to: {self.log_path}", 'INFO')
        self.log_message(f"✅ Sent emails log: {self.sent_emails_path}", 'INFO')

        return total_failed == 0

    def send_test_email(self, test_email):
        """Send a test email to verify setup"""
        self.log_message("="*80, 'INFO')
        self.log_message("🧪 SENDING TEST EMAIL", 'INFO')
        self.log_message("="*80, 'INFO')

        if not self.validate_config():
            return False

        if not self.connect_smtp():
            return False

        # Create test candidate
        test_candidate = {
            'name': 'Test User',
            'email': test_email
        }

        success = self.send_email(test_candidate)
        self.disconnect_smtp()

        if success:
            self.log_message("", 'INFO')
            self.log_message("✅ Test email sent successfully!", 'INFO')
        else:
            self.log_message("", 'INFO')
            self.log_message("❌ Test email failed", 'ERROR')

        return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Email Campaign Manager')
    parser.add_argument('--test-email', help='Send a test email to specified address')
    parser.add_argument('--send-all', action='store_true', help='Send to all candidates')
    parser.add_argument('--dry-run', action='store_true', help='Validate without sending')

    args = parser.parse_args()

    # Initialize campaign manager
    campaign = CampaignManager()

    # Handle commands
    if args.test_email:
        success = campaign.send_test_email(args.test_email)
        sys.exit(0 if success else 1)
    elif args.send_all:
        # Confirmation prompt
        print(f"\n⚠️  You are about to send emails to candidates from {campaign.config['smtp']['sender_email']}.")
        response = input("   Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Campaign cancelled")
            sys.exit(0)

        success = campaign.run_campaign(dry_run=args.dry_run)
        sys.exit(0 if success else 1)
    elif args.dry_run:
        success = campaign.run_campaign(dry_run=True)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
