import logging
import time

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.path} "
            f"{response.status_code} "
            f"{duration:.2f}s"
        )

        return response

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # response = self.get_response(request) or
        try:
            response = self.get_response(request)
        except Exception:
            logger.exception("Unhandled exception during request")
            raise

        duration = time.time() - start_time

        if duration > 2:
            logger.warning(
                "Slow request: %s %s took %.2fs",
                request.method,
                request.path,
                duration
            )

        logger.info(
            "Method=%s Path=%s Status=%s Duration=%.2f User=%s",
            request.method,
            request.path,
            response.status_code,
            duration,
            getattr(request.user, 'id', None)
        )

        return response

class SimpleLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Request Path:", request.path)

        response = self.get_response(request)

        print("Response Status:", response.status_code)
        return response
