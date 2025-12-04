import logging
from datetime import datetime
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

        response = self.get_response(request)
        return response
