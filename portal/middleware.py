import time
from .models import Events
from django.contrib.auth.models import User


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = time.monotonic()
        response = self.get_response(request)

        tmp = Events()
        tmp.user = request.user
        tmp.path = request.path
        tmp.delay = time.monotonic() - timestamp
        tmp.save()

        return response