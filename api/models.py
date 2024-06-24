from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=50, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
    
class Outfit(models.Model):
    image = models.ImageField(upload_to='outfit/')
    added_by = models.ForeignKey(Client, on_delete=models.PROTECT)
    binary_code = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.added_by.name

class Billing(models.Model):
    AVAILABLE_METHODS = [
        ('Time', 'Time'),
        ('Per Req', 'Per Req'),
        ('Bulk Buy', 'Bulk Buy'),
    ]
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    method = models.CharField(max_length=100, choices=AVAILABLE_METHODS)
    start_dt = models.DateTimeField(null=True, blank=True)
    end_dt = models.DateTimeField(null=True, blank=True)
    no_of_req_allowed = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    price_for_exceeded_requests = models.IntegerField(null=True, blank=True)
    no_of_exceeded_requests_allowed = models.IntegerField(null=True, blank=True)
    no_of_request_consumed = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.client.name


class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    billing = models.ForeignKey(Billing, on_delete=models.PROTECT)
    over_spend_charge = models.CharField(max_length=1000, null=True, blank=True)
    billed_amount = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.client.name
