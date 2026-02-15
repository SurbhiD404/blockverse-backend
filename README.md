BLOCKVERSE’26 — Event Registration Backend

Backend system for BLOCKVERSE’26, a college technical event.
This project handles secure team registration, payment verification, email confirmations, and QR-based access for participants.

It is built using Django and designed to handle real event traffic safely.

## Features

Solo & Duo team registration

Unique Team ID generation

Roll number enforced as unique

Secure password hashing

Razorpay payment verification

Confirmation emails via Gmail SMTP

QR code for direct registration access

Admin dashboard for organizers

Atomic database transactions (no partial saves)

Production-ready PostgreSQL database

Logging for audit & debugging

## How the system works

User selects team type (solo / duo)

Razorpay payment order is created

Payment is verified server-side

Registration data is validated

Team + players are saved atomically

Confirmation email is sent

QR code allows direct access to registration


🛠 Tech Stack

Python 3

Django

Django REST Framework

PostgreSQL (production)

SQLite (development)

Razorpay API

Gmail SMTP

QRCode + Pillow

Render deployment


2. Create virtual environment
python -m venv venv


Activate:

Windows:

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Environment variables

5. Run migrations
python manage.py makemigrations
python manage.py migrate

6. Create admin user
python manage.py createsuperuser

7. Start server
python manage.py runserver


Server runs at:

http://127.0.0.1:8000/


Admin panel:

http://127.0.0.1:8000/admin

🔌 API Endpoints
Create Payment Order
POST /api/create-payment-order/


Creates Razorpay order based on team type.

Verify Payment & Register
POST /api/verify-payment-and-register/


Verifies payment signature and registers team.

QR Registration
GET /api/qr/


Returns QR code for registration access.

## Security Features

Password hashing (Django PBKDF2)

Razorpay signature verification

Atomic database transactions

Unique roll number enforcement

Environment variable secret storage

API logging

## Deployment

The backend is deployed on Render with:

PostgreSQL database

Environment variables

Production WSGI server

HTTPS enabled

To redeploy:

git add .
git commit -m "update"
git push


Render auto-deploys latest commit.

📧 Email System

Emails are sent via Gmail SMTP.

Each registered participant receives:

Team ID

Team password

Registration confirmation

If email fails, registration is still saved and admin can resend.

## Admin Features

Organizers can:

View all teams

Search by Team ID

Filter participants

Track payment status

Monitor email delivery

Admin dashboard:

/admin
## Future Improvements

CSV export for organizers

QR gate verification system

Login dashboard for teams

Email retry queue

Analytics dashboard
