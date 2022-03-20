from django.http import HttpResponse
from rest_framework.exceptions import NotAuthenticated

from pets import settings


class CheckApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        X_API_KEY = request.headers.get("X-API-KEY", "")
        if X_API_KEY != settings.API_KEY:
            return HttpResponse('Unauthorized', status=401, headers={"WWW-Authenticate": "Use X-API-KEY"})

        response = self.get_response(request)

        return response
