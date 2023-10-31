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
        tmp.remote_addr = request.META['REMOTE_ADDR']
        tmp.request_method = request.META['REQUEST_METHOD']
        tmp.save()

        return response