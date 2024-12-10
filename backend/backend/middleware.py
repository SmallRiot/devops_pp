import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info("Incoming request: %s %s", request.method, request.path)

    def process_response(self, request, response):
        logger.info("Outgoing response: %s %s", request.method, response.status_code)
        return response