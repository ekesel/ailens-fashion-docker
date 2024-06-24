# api/throttles.py

from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from api.models import Billing
from datetime import timedelta
from django.utils import timezone
import threading
import time

CACHE_SYNC_INTERVAL = 10  # seconds

class NoThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return True

class OneTimeRateThrottle(BaseThrottle):
    def __init__(self):
        super().__init__()
        self.billing_cache = {}
        # Start the periodic database sync in a separate thread
        self.start_periodic_db_sync()

    def get_cache_key(self, user_id):
        # Generate a unique cache key for the user's billing data
        return f'billing_data_{user_id}'

    def allow_request(self, request, view):
        if not request.user.is_authenticated:
            self.message = "User is not authenticated."
            return False

        user_id = request.user.id
        cache_key = self.get_cache_key(user_id)

        # Load billing data from cache
        billing_data = cache.get(cache_key)

        if billing_data is None:
            # If not in cache, load from database and store in cache
            billing_data = self.load_billing_from_db(user_id)
            if billing_data is None:
                self.message = "Billing information not found."
                return False
            # Store the loaded billing data in cache with expiration set to user's end date
            expiration_seconds = self.get_seconds_until_end_date(billing_data.end_dt)
            cache.set(cache_key, billing_data, expiration_seconds)

        if not billing_data.is_active:
            self.message = "Billing is not active."
            return False

        # Handle request based on the billing method
        if billing_data.method == 'Per Req':
            return self.handle_per_req(billing_data, cache_key)
        elif billing_data.method == 'Bulk Buy':
            return self.handle_bulk_buy(billing_data, cache_key)
        elif billing_data.method == 'Time':
            return self.handle_time(billing_data, cache_key)

        self.message = "Invalid billing method."
        return False

    def load_billing_from_db(self, user_id):
        try:
            # Load billing data from database for the given user
            billing = Billing.objects.get(client__user_id=user_id, is_active=True)
            return billing
        except Billing.DoesNotExist:
            return None

    def handle_per_req(self, billing_data, cache_key):
        # For "Per Req" method, simply update the request count in cache
        self.update_cache(billing_data, cache_key)
        return True

    def handle_bulk_buy(self, billing_data, cache_key):
        if billing_data.no_of_request_consumed >= billing_data.no_of_req_allowed:
            if billing_data.no_of_request_consumed - billing_data.no_of_req_allowed < billing_data.no_of_exceeded_requests_allowed:
                # If within the exceeded request limit, update the request count in cache
                self.update_cache(billing_data, cache_key)
                return True
            self.message = "Number of allowed requests exceeded, and no extra requests are allowed."
            return False

        # If within the allowed request limit, update the request count in cache
        self.update_cache(billing_data, cache_key)
        return True

    def handle_time(self, billing_data, cache_key):
        if not (billing_data.start_dt <= timezone.now() <= billing_data.end_dt):
            self.message = "Request is outside of the allowed time period."
            return False

        if billing_data.no_of_request_consumed >= billing_data.no_of_req_allowed:
            if billing_data.no_of_request_consumed - billing_data.no_of_req_allowed < billing_data.no_of_exceeded_requests_allowed:
                # If within the exceeded request limit, update the request count in cache
                self.update_cache(billing_data, cache_key)
                return True
            self.message = "Number of allowed requests exceeded, and no extra requests are allowed."
            return False

        # If within the allowed request limit, update the request count in cache
        self.update_cache(billing_data, cache_key)
        return True

    def update_cache(self, billing_data, cache_key):
        # Increment the request count in the billing data
        billing_data.no_of_request_consumed += 1
        # Update the cache with the new billing data and set the expiration to user's end date
        expiration_seconds = self.get_seconds_until_end_date(billing_data.end_dt)
        cache.set(cache_key, billing_data, expiration_seconds)
        # Update the in-memory cache
        self.billing_cache[billing_data.client.user.id] = billing_data

    def get_seconds_until_end_date(self, end_date):
        """
        Calculate the number of seconds from now until the specified end date.
        """
        now = timezone.now()
        # Ensure the end_date is in timezone-aware datetime format
        if not timezone.is_aware(end_date):
            end_date = timezone.make_aware(end_date)

        # Calculate the difference in seconds between end_date and now
        return int((end_date - now).total_seconds())

    def periodic_db_sync(self):
        while True:
            time.sleep(10)  # Wait for 10 seconds
            for user_id, billing_data in self.billing_cache.items():
                billing_data.save()  # Save each billing data object to the database

    def start_periodic_db_sync(self):
        # Start the periodic_db_sync method in a separate daemon thread
        thread = threading.Thread(target=self.periodic_db_sync, daemon=True)
        thread.start()

    def __del__(self):
        # Ensure the final sync to the database when the object is deleted
        self.periodic_db_sync()