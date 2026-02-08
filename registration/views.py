import uuid
import logging
from django.conf import settings
from django.db import transaction, IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Team, Player
from .serializers import TeamRegistrationSerializer
from .utils import send_registration_email
from .payment import create_order, verify_signature
from .constants import SOLO_FEE, DUO_FEE
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
            order = create_order(amount, receipt)

            return Response({
                "order_id": order["id"],
                "amount": amount,
                "currency": "INR",
                "key": settings.RAZORPAY_KEY_ID
            })

        except Exception as e:
            logger.error(f"Payment order creation failed: {str(e)}")
            return Response(
                {"error": f"Payment order creation failed"},
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
            logger.error(f"Verification error: {str(e)}")
            return Response(
                {"error": f"Payment verification error"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        serializer = TeamRegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        reg = serializer.validated_data

       
        try:
            with transaction.atomic():

                team = Team.objects.create(
                    team_id=reg['teamId'],
                    team_type=reg['team_type'],
                    password=reg['password'],
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
            logger.error(f"Registration failed: {str(e)}")
            return Response(
                {"error": f"Registration failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        
        email_status = "sent"

        try:
            send_registration_email(p1.email, team.team_id, reg['password'])

            if p2:
                send_registration_email(p2.email, team.team_id, reg['password'])

        except Exception as e:
            email_status = "failed"
            logger.error(f"Email sending failed for team {team.team_id}: {str(e)}")
            # print("Email failed:", e)

       
        return Response(
            {
                "message": "Payment verified & registration successful",
                "team_id": team.team_id,
                "email_status": email_status
            },
            status=status.HTTP_201_CREATED
        )

