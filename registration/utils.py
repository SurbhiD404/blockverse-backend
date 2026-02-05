from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_registration_email(email, team_id, password):
    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject="BLOCKVERSE’26 Registration Successful 🎉",
        html_content=f"""
        <h2>BLOCKVERSE’26</h2>
        <p><b>Team ID:</b> {team_id}</p>
        <p><b>Password:</b> {password}</p>
        """
    )
    try:
       SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
    except Exception as e:
        raise e