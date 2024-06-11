from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from datetime import datetime
from api.models import Client

class MonthlyRateThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        return f'{request.user.id}_{datetime.now().strftime("%Y%m")}'

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return False

        # Assuming client has a price field
        price = client.price
        rate = self.get_monthly_rate(price)

        cache_key = self.get_cache_key(request, view)
        num_requests = cache.get(cache_key, 0)

        if num_requests >= rate:
            return False

        cache.incr(cache_key)
        cache.expire(cache_key, 30 * 24 * 60 * 60)  # 30 days
        return True

    def get_monthly_rate(self, price):
        # Define your logic to calculate the rate based on price
        if price == 10:
            return 100
        elif price == 20:
            return 200
        # Add more conditions as needed
        return 50
    
class OneTimeRateThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        return f'{request.user.id}_one_time'

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            return False

        cache_key = self.get_cache_key(request, view)
        print(cache_key)
        if cache.get(cache_key):
            return False

        cache.set(cache_key, 1, None)  # No expiration time
        return True
    
class BulkRateThrottle(BaseThrottle):
    def get_cache_key(self, request, view):
        return f'{request.user.id}_bulk'

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            return False

        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            return False

        # Assuming client has a price field
        price = client.price
        rate = self.get_bulk_rate(price)

        cache_key = self.get_cache_key(request, view)
        num_requests = cache.get(cache_key, 0)

        if num_requests >= rate:
            return False

        cache.incr(cache_key)
        return True

    def get_bulk_rate(self, price):
        # Define your logic to calculate the rate based on price
        if price == 100:
            return 1000
        elif price == 200:
            return 2000
        # Add more conditions as needed
        return 500
    
class NoThrottle(BaseThrottle):

    def allow_request(self, request, view):
        return True