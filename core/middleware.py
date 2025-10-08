# core/middleware.py
import uuid
from django.utils.deprecation import MiddlewareMixin

TRACE_HEADER = "HTTP_X_TRACE_ID"

class TraceIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.trace_id = request.META.get(TRACE_HEADER) or str(uuid.uuid4())
