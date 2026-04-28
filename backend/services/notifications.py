import os
import sendgrid
from sendgrid.helpers.mail import Mail
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
ONE_SIGNAL_APP_ID = os.getenv("ONE_SIGNAL_APP_ID")

sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY) if SENDGRID_API_KEY else None

async def send_email(to_email: str, subject: str, content: str):
    """Send email using SendGrid"""
    if not sg:
        logger.warning("SendGrid not configured")
        return
    
    try:
        message = Mail(
            from_email='noreply@ayfgwarimpa.org',
            to_emails=to_email,
            subject=subject,
            html_content=f'<p>{content}</p>'
        )
        response = sg.send(message)
        logger.info(f"Email sent to {to_email}: {response.status_code}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")

async def send_push_notification(user_ids: List[str], title: str, message: str, data: Dict = None):
    """Send push notification using OneSignal"""
    if not ONE_SIGNAL_APP_ID:
        logger.warning("OneSignal not configured")
        return
    
    # This would integrate with OneSignal API
    logger.info(f"Push notification to {len(user_ids)} users: {title}")
