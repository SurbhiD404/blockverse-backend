from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "service": "BLOCKVERSE’26 Backend API",
        "status": "running",
        "version": "1.0",
        "message": "Welcome to BlockVerse registration backend 🚀"
    })
