# import qrcode
# import base64
# from io import BytesIO

# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings


# def generate_qr_base64(data):
#     """
#     Generate QR image and return base64 string
#     so it can be embedded inside email
#     """
#     qr = qrcode.make(data)

#     buffer = BytesIO()
#     qr.save(buffer, format="PNG")

#     img_str = base64.b64encode(buffer.getvalue()).decode()
#     return img_str


# def send_registration_email(team, raw_password):
#     """
#     Sends HTML email with QR codes
#     for each player in the team
#     """

#     subject = "🎟️ BLOCKVERSE’26 — You're In!"

#     # get players from DB
#     players = team.players.all()

#     text_message = f"""
# BLOCKVERSE’26 Registration Confirmed

# Team ID: {team.team_id}
# Password: {raw_password}

# Keep credentials safe.
# """

#     html_players_section = ""

#     for player in players:
#         qr = generate_qr_base64(player.student_no)

#         html_players_section += f"""
#         <div style="background:#f1f5f9;border-radius:10px;padding:15px;margin:15px 0;">
#             <p><b>Name:</b> {player.name}</p>
#             <p><b>Student No:</b> {player.student_no}</p>
#             <img src="data:image/png;base64,{qr}" width="160"/>
#         </div>
#         """

#     html_message = f"""
# <div style="margin:0;padding:0;background:#0f172a;font-family:Arial,sans-serif;">

#     <div style="max-width:650px;margin:auto;background:#ffffff;border-radius:12px;overflow:hidden;">

#         <div style="background:linear-gradient(135deg,#2563eb,#7c3aed);padding:30px;text-align:center;color:white;">
#             <h1 style="margin:0;font-size:28px;">🚀 BLOCKVERSE’26</h1>
#             <p style="margin:8px 0 0;font-size:16px;">Registration Confirmed</p>
#         </div>

#         <div style="padding:30px;color:#111827;">

#             <h2>Congratulations Team! 🎉</h2>

#             <p>Your registration is confirmed.</p>

#             <div style="background:#e5e7eb;border-radius:10px;padding:15px;margin:20px 0;">
#                 <p><b>Team ID:</b> {team.team_id}</p>
#                 <p><b>Password:</b> {raw_password}</p>
#             </div>

#             <h3>🎫 Player QR Codes</h3>

#             {html_players_section}

#             <p>Scan QR for attendance.</p>

#             <p style="margin-top:20px;">
#                 🔥 Innovate. Build. Dominate.<br>
#                 See you at the arena!
#             </p>

#         </div>

#         <div style="background:#111827;color:#9ca3af;text-align:center;padding:20px;font-size:12px;">
#             BLOCKVERSE’26 Organizing Committee<br>
#             This is an automated confirmation email
#         </div>

#     </div>

# </div>
# """

#     # send to all players
#     recipients = [player.email for player in players]

#     try:
#         email = EmailMultiAlternatives(
#             subject,
#             text_message,
#             settings.DEFAULT_FROM_EMAIL,
#             recipients,
#         )

#         email.attach_alternative(html_message, "text/html")
#         email.send()

#         return True

#     except Exception as e:
#         print("EMAIL ERROR:", e)
#         return False


import logging
import qrcode
from io import BytesIO

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.mime.image import MIMEImage
logger = logging.getLogger(__name__)

def generate_qr_image(data):
    qr = qrcode.make(data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer


def send_registration_email(team, raw_password):

    subject = "🎟️ BLOCKVERSE’26 — You're In!"

    players = team.players.all()

    text_message = f"""
BLOCKVERSE’26 Registration Confirmed

Team ID: {team.team_id}
Password: {raw_password}

Welcome to the arena.
Bring your A-game.
"""

    html_players_section = ""
    qr_images = []

    # generate QR attachments
    for index, player in enumerate(players):
        img_buffer = generate_qr_image(player.student_no)

        cid = f"qr{index}"

        image = MIMEImage(img_buffer.read())
        image.add_header("Content-ID", f"<{cid}>")
        image.add_header("Content-Disposition", "inline")

        qr_images.append(image)

        html_players_section += f"""
        <div style="background:#f8fafc;border-radius:12px;padding:18px;margin:18px 0;border:1px solid #e5e7eb;">
            <p style="margin:0 0 6px;"><b>Name:</b> {player.name}</p>
            <p style="margin:0 0 10px;"><b>Student No:</b> {player.student_no}</p>
            <img src="cid:{cid}" width="150"/>
        </div>
        """

    html_message = f"""
<div style="margin:0;padding:0;background:#0f172a;font-family:Arial,sans-serif;">

    <div style="max-width:680px;margin:auto;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,0.25);">

        <div style="background:linear-gradient(135deg,#2563eb,#7c3aed);padding:40px;text-align:center;color:white;">
            <h1 style="margin:0;font-size:30px;">🚀 BLOCKVERSE’26</h1>
            <p style="margin-top:10px;font-size:16px;opacity:0.9;">
                Official Registration Confirmation
            </p>
        </div>

        <div style="padding:32px;color:#111827;line-height:1.6;">

            <h2 style="margin-top:0;">Congratulations Champions! 🎉</h2>

            <p>
                You are officially registered for <b>BLOCKVERSE’26</b> —
                the battlefield where innovation meets competition.
            </p>

            <p>
                Expect intense challenges, creative problem solving,
                and an unforgettable tech experience.
            </p>

            <div style="background:#e5e7eb;border-radius:12px;padding:18px;margin:22px 0;">
                <p style="margin:0 0 6px;"><b>🎟 Team ID:</b> {team.team_id}</p>
                <p style="margin:0;"><b>🔐 Password:</b> {raw_password}</p>
            </div>

            <h3>🎫 Player QR Codes</h3>

            {html_players_section}

            <p style="font-size:14px;color:#374151;">
                Scan your QR at the entry desk for instant attendance verification.
            </p>

            <h3>📌 Event Checklist</h3>

            <ul style="padding-left:18px;font-size:14px;color:#374151;">
                <li>Carry your college ID card</li>
                <li>Arrive at least 30 minutes early</li>
                <li>Keep your credentials safe</li>
                <li>Stay active in the WhatsApp updates group</li>
                <li>Charge your devices ⚡</li>
                <li>Bring your competitive spirit 🔥</li>
            </ul>

            <p style="margin-top:22px;font-weight:bold;font-size:16px;">
                Innovate. Compete. Dominate.
            </p>

            <p>
                The arena is ready. The future is waiting.<br>
                See you at BLOCKVERSE’26 — bring your best game!
            </p>

        </div>

        <div style="background:#111827;color:#9ca3af;text-align:center;padding:22px;font-size:12px;">
            BLOCKVERSE’26 Organizing Committee<br>
            From BRL Tech Society ❤️<br>
            This is an automated confirmation email
        </div>

    </div>

    <p style="text-align:center;color:#64748b;font-size:12px;margin:18px 0;">
        © BLOCKVERSE’26 • All rights reserved
    </p>

</div>
"""

    recipients = [player.email for player in players]

    try:
        email = EmailMultiAlternatives(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
        )

        email.attach_alternative(html_message, "text/html")

        # attach QR images
        for img in qr_images:
            email.attach(img)

        email.send(fail_silently=True)

        return True

    except Exception as e:
        logger.error("EMAIL ERROR: %s", e)
        return False
