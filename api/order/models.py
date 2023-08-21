import random
from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
# Create your models here.
from slugify import slugify

from api.users.models import User
from main.models import Log
from fapva.utils import parse_email


# Create your models here.
class Order(Log):
    user = models.ForeignKey(User, db_column='UserId', related_name='user_order', on_delete=models.CASCADE)
    order_id = models.CharField(db_column="OrderId", default=None, max_length=255, null=True)
    capture_id = models.CharField(db_column="CaptureId", blank=True, null=True, max_length=255)
    response_json = models.TextField(db_column="ResponseJson", null=True, blank=True)
    payment_channel = models.CharField(db_column="PaymentChannel", null=True, default=None, max_length=255)
    country_id = models.IntegerField(db_column='CountryId', default=0)
    country_name = models.CharField(db_column="CountryName", default=None, null=True, max_length=255)
    number = models.CharField(db_column="Number", default=None, null=True, max_length=255)
    number_id = models.IntegerField(db_column="NumberId", default=None, null=True)
    price = models.FloatField(db_column="Price", default=0)
    is_completed = models.BooleanField(db_column="IsCompleted", default=False)
    expire_at = models.DateTimeField(db_column="ExpireAt", default=None, null=True)
    is_refunded = models.BooleanField(db_column="IsRefunded", default=False)
    refunded_reason = models.CharField(db_column="RefundedReason", default=None, max_length=255, null=True)
    is_number_faulty = models.BooleanField(db_column="IsNumberFaulty", default=False)
    message = models.TextField(db_column="Message", default=None, null=True, blank=True)

    class Meta:
        db_table = 'Order'


class UserWallet(Log):
    user = models.ForeignKey(User, db_column='UserId', related_name='user_wallet', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, db_column='OrderId', related_name='order_wallet', on_delete=models.CASCADE)
    balance = models.FloatField(db_column="Balance", default=0, null=True)
    is_refunded = models.BooleanField(db_column="IsRefunded", default=True)
    order_placed = models.BooleanField(db_column="OrderPlaced", default=None)

    class Meta:
        db_table="UserWallet"
