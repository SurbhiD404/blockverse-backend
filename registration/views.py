import uuid
import logging
import razorpay

from django.conf import settings
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Team, Player
from .serializers import TeamRegistrationSerializer

from .payment import create_order, verify_signature
from .constants import SOLO_FEE, DUO_FEE
from .email_service import send_registration_email

logger = logging.getLogger(__name__)


class CreatePaymentOrder(APIView):

    def post(self, request):

        team_type = request.data.get("team_type")

        
        if team_type == "solo":
            amount = SOLO_FEE * 100

        elif team_type == "duo":
            amount = DUO_FEE * 100
        else:
            return Response(
                {"error": "Invalid team type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receipt = str(uuid.uuid4())
            order = create_order(amount, receipt,notes={"team_type": team_type})

            return Response({
                "order_id": order["id"],
                "amount": amount,
                "currency": "INR",
                "key": settings.RAZORPAY_KEY_ID
            })

        except Exception as e :
            logger.exception("Payment order creation failed")
            return Response(
                {"error": f"Payment order creation failed: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyPaymentAndRegister(APIView):

    def post(self, request):

        data = request.data
        p2 = None  

        if not all([
            data.get("razorpay_order_id"),
            data.get("razorpay_payment_id"),
            data.get("razorpay_signature")
        ]):
            return Response(
                {"error": "Missing payment fields"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
            
        try:
            verified = verify_signature({
                "razorpay_order_id": data.get("razorpay_order_id"),
                "razorpay_payment_id": data.get("razorpay_payment_id"),
                "razorpay_signature": data.get("razorpay_signature"),
            })

            if not verified:
                logger.warning("Payment verification failed")
                return Response(
                    {"error": "Payment verification failed"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            logger.info("Payment verified successfully")
        except Exception as e: 
            logger.exception("Payment verification error: %s", e)
            return Response(
                {"error": f"Payment verification error: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        serializer = TeamRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        reg = serializer.validated_data
        raw_password = reg['password']  
        # hashed_password = raw_password
        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            payment = client.payment.fetch(data.get("razorpay_payment_id"))
            paid_amount = payment["amount"]  # paise
            
            order=client.order.fetch(data.get("razorpay_order_id"))
            order_team_type=order.get("notes", {}).get("team_type")
            
            if order_team_type not in ["solo", "duo"]:
                logger.warning("Invalid order metadata")
                return Response(
                    {"error": "Invalid payment metadata"},
                    status=status.HTTP_400_BAD_REQUEST
                )


            expected_amount = (
                SOLO_FEE * 100
                if order_team_type == "solo"
                else DUO_FEE * 100
            )

            if paid_amount != expected_amount:
                logger.warning("Payment amount mismatch")
                return Response(
                    {"error": "Payment amount mismatch"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.exception("Payment fetch failed: %s", e)
            return Response(
                {"error": f"Unable to verify payment amount: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )
       
        try:  
            with transaction.atomic():

                team = Team.objects.create(
                    team_id=reg['teamId'],
                    team_type=reg['team_type'],
                    # password=reg['password'],
                    password=raw_password,
                    payment_order_id=data.get("razorpay_order_id"),
                    payment_id=data.get("razorpay_payment_id"),
                    payment_status=True
                )
                logger.info(f"Team registered: {team.team_id}")
                p1 = Player.objects.create(team=team, **reg['player1'])

                if reg['team_type'] == 'duo':
                    p2 = Player.objects.create(team=team, **reg['player2'])

        except IntegrityError:
            logger.warning(f"Duplicate team attempt: {reg['teamId']}")
            return Response(
                {"error": "Team ID already exists or duplicate roll number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception(f"Registration failed: {e}")
            return Response(
                {"error": f"Registration failed due to server error: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
        email_status = "sent"

        try:
            send_registration_email(team, raw_password)
            team.email_sent = True
            team.save(update_fields=["email_sent"])

        except Exception as e:
              email_status = "failed"
              team.email_sent = False
              team.save(update_fields=["email_sent"])
              logger.error("Email failed but registration succeeded: %s", e)
        
        return Response(
            {
                "message": "Payment verified & registration successful",
                "team_id": team.team_id,
                "email_status": email_status
            },
            status=status.HTTP_201_CREATED
        )

