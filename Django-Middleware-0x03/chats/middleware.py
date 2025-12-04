import logging
from datetime import datetime, time
import time as time_module   # <--- FIX: rename module to avoid clash

from django.http import HttpResponseForbidden, HttpResponse
from django.utils.deprecation import MiddlewareMixin


# Configure logger
logger = logging.getLogger("requests_logger")


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        path = request.get_full_path()

        logger.info(f"{datetime.now()} - User: {user} - Path: {path}")

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Allowed: 06:00 → 21:00
        self.start_time = time(6, 0)
        self.end_time = time(21, 0)

    def __call__(self, request):
        current_time = datetime.now().time()

        if request.path.startswith("/api/v1/chats/"):
            if not (self.start_time <= current_time <= self.end_time):
                return HttpResponseForbidden(
                    "Access to the messaging system is restricted outside 6 AM - 9 PM."
                )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Tracks messages per IP:
        self.message_log = {}

        # Rate limit
        self.limit = 5       # 5 messages
        self.window = 60     # in 60 seconds

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/v1/chats/"):

            ip = self.get_ip(request)
            now = time_module.time()  # <--- FIX: use renamed module

            # Initialize tracking for new IP
            if ip not in self.message_log:
                self.message_log[ip] = []

            # Keep only timestamps in the last minute
            self.message_log[ip] = [
                ts for ts in self.message_log[ip] if now - ts < self.window
            ]

            # Limit reached?
            if len(self.message_log[ip]) >= self.limit:
                return HttpResponse(
                    "Rate limit exceeded. You can only send 5 messages per minute.",
                    status=429,
                )

            # Accept this message
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")
