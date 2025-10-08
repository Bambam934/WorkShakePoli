import time
from django.core.cache import cache
from django.http import JsonResponse

class IdempotencyMiddleware:
    """
    Rechaza reenvíos del mismo Idempotency-Key en ventana TTL.
    Espera header: Idempotency-Key
    """
    TTL_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ("POST", "PUT", "PATCH"):
            key = request.headers.get("Idempotency-Key")
            if key:
                cache_key = f"idemp:{request.user.id if request.user.is_authenticated else 'anon'}:{key}"
                if cache.get(cache_key):
                    return JsonResponse(
                        {"detail": "Duplicate request (Idempotency-Key)"},
                        status=409
                    )
                cache.set(cache_key, int(time.time()), timeout=self.TTL_SECONDS)
        return self.get_response(request)
