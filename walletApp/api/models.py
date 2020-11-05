from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Api(models.Model):
    customer_xid = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=50, default="disabled")
    token = models.CharField(max_length=100)
    is_disabled = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=20,decimal_places=4,default=Decimal('0.0000'))
    enabled_at = models.DateTimeField(null=True, blank=True)
    disabled_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    deposited_at = models.DateTimeField(null=True, blank=True)
    reference_id = models.CharField(max_length=100,null=True, unique=True)
    deposited_by = models.CharField(max_length=100, null=True)
    withdrawn_by = models.CharField(max_length=100, null=True)
    history_json = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.customer_xid