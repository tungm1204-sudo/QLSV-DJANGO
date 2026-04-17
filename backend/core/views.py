from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": "API is running. See /api/docs/ for endpoints."})
