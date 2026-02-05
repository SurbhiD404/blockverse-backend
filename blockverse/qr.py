
import qrcode
from io import BytesIO
from django.http import HttpResponse


def registration_qr_view(request):
   
    registration_url = "http://127.0.0.1:3000/register"

    img = qrcode.make(registration_url)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")


