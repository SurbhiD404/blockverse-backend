import razorpay
from django.conf import settings

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def create_order(amount, receipt , notes=None ):
    order_data = {
        "amount": amount,
        "currency": "INR",
        "receipt": receipt,
        "payment_capture": 1,
        "notes": notes or {}
    }
    return client.order.create(data=order_data)

def verify_signature(data):
    try:
          client.utility.verify_payment_signature(data)
          return True
    except Exception:
          return False   
# def verify_signature(data):
    
#     return True
