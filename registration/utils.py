# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from django.conf import settings

# def send_registration_email(email, team_id, password):
#     message = Mail(
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to_emails=email,
#         subject="BLOCKVERSE’26 Registration Successful 🎉",
#         html_content=f"""
#         <h2>BLOCKVERSE’26</h2>
#         <p><b>Team ID:</b> {team_id}</p>
#         <p><b>Password:</b> {password}</p>
#         """
#     )
#     try:
#        SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
#     except Exception as e:
#         raise e





from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_registration_email(email, team_id, password):

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=email,
        subject="🎟️ BLOCKVERSE’26 — You're In!",
        html_content=f"""
        <div style="margin:0;padding:0;background:#0f172a;font-family:Arial, sans-serif;">

            <div style="max-width:650px;margin:auto;background:#ffffff;border-radius:12px;overflow:hidden;">

                <div style="background:linear-gradient(135deg,#2563eb,#7c3aed);padding:30px;text-align:center;color:white;">
                    <h1 style="margin:0;font-size:28px;">🚀 BLOCKVERSE’26</h1>
                    <p style="margin:8px 0 0;font-size:16px;">Registration Confirmed</p>
                </div>

                <div style="padding:30px;color:#111827;">

                    <h2>Congratulations Participant! 🎉</h2>

                    <p style="font-size:15px;">
                        Your spot at BLOCKVERSE’26 is secured.
                        Get ready to compete in one of the most electrifying tech events of the year.
                    </p>

                    <div style="background:#f1f5f9;border-radius:10px;padding:20px;margin:20px 0;">
                        <p><b>Team ID:</b> {team_id}</p>
                        <p><b>Password:</b> {password}</p>
                    </div>

                    <h3>📌 Event Checklist</h3>
                    <ul style="padding-left:18px;font-size:14px;">
                        <li>Carry your college ID</li>
                        <li>Arrive 30 minutes early</li>
                        <li>Keep team credentials safe</li>
                        <li>Watch whatsapp group for updates</li>
                    </ul>

                    <p style="font-size:16px;margin-top:20px;">
                        🔥 Innovate. Build. Dominate.<br>
                        See you at the arena!
                    </p>

                </div>

                <div style="background:#111827;color:#9ca3af;text-align:center;padding:20px;font-size:12px;">
                    BLOCKVERSE’26 Organizing Committee<br>
                    From BRL TEAM ❤️<br>
                    This is an automated confirmation email
                </div>

            </div>

            <p style="text-align:center;color:#64748b;font-size:12px;margin:20px 0;">
                © BLOCKVERSE’26 • All rights reserved
            </p>

        </div>
        """
    )
    try:
     SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
    except Exception as e:
        raise e