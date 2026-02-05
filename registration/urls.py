from django.urls import path
from .views import  CreatePaymentOrder, VerifyPaymentAndRegister

urlpatterns = [
    # path('register/', RegisterTeamView.as_view()),
    path('create-order/', CreatePaymentOrder.as_view()),
    path('verify-payment/', VerifyPaymentAndRegister.as_view()), #register after payment verification
]
