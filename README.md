# BLOCKVERSE’26 – Event Registration Backend
 This project is the backend system for the college technical event
 BLOCKVERSE’26. It handles event registrations, team management,
 email confirmations, and QR-based registration access.

 ##Features
  - Solo and Duo team registration
  - Unique Team ID for each team
  - Roll number enforced as unique
  - Confirmation email sent to all registered     candidates
  - QR code for direct registration access
  - Admin panel for organizers
  - Razorpay payment verification
  - PostgreSQL production database

 ##Tech Stack
 - Python 3
 - Django
 - Django REST Framework
 - SQLite (development)
 - SendGrid (email service)
 - QRCode + Pillow

 ##Project Setup

 1. Create virtual environment
    python -m venv venv

 2. Activate virtual environment
   venv\Scripts\activate

 3. Install dependencies
    pip install -r requirements.txt

 4. Run migrations
    python manage.py makemigrations
    python manage.py migrate

 5. Start server
    python manage.py runserver


 ## API Endpoints

 1. Create Payment Order
    POST /api/create-payment-order/

   Generates Razorpay order based on team type(solo/duo).

 2. Verify Payment & Register
    POST /api/verify-payment-and-register/
   
   Verifies payment signature and stores registration data.

 3. QR Code
    GET /api/qr/

