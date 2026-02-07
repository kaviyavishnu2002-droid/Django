from rest_framework.throttling import BaseThrottle
from rest_framework.throttling import UserRateThrottle
import time
from rest_framework.response import Response

class CustomIPThrottle(BaseThrottle):
    cache = {}

    def allow_request(self, request, view):
        ip = request.META.get('REMOTE_ADDR')
        now = time.time()
        if ip not in self.cache:
            self.cache[ip] = [now]
            return True
        self.cache[ip] = [t for t in self.cache[ip] if now - t < 60]
        if len(self.cache[ip]) >= 5:
            return False
        self.cache[ip].append(now)
        return True

    def wait(self):
        return 60

class BurstUserThrottle(UserRateThrottle):
    rate = '3/minute'

    def throttle_failure(self):
        return Response(
            {"error": "Too many requests. Try again later."},
            status=429
        )

class RoleBasedThrottle(UserRateThrottle):
    def get_rate(self):
        user = self.request.user

        if user.is_authenticated:
            if user.groups.filter(name='Premium').exists():
                return '10/minute'
            return '6/minute'
        return '3/minute'
