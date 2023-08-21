import random
from datetime import datetime, timedelta
from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
# Create your models here.
from slugify import slugify

from main.models import Log, Countries
from fapva.utils import parse_email, image_directory_path


# Create your models here.
class Services(Log):
    """ Role model."""
    name = models.CharField(db_column='Name', max_length=255, null=True, blank=True)
    code = models.SlugField(db_column='Code', default=None, null=True, blank=True)
    flag = models.FileField(db_column="Flag", upload_to=image_directory_path, default=None, null=True)
    is_active = models.BooleanField(db_column="IsActive", default=True)
    is_deleted = models.BooleanField(db_column="IsDeleted", default=False)

    class Meta:
        db_table = 'Services'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.code = slugify(self.name)
            super().save()
        except Exception:
            raise


class ServiceNumber(Log):
    country = models.ForeignKey(Countries, db_column='CountryId', related_name='country_service', on_delete=models.CASCADE)
    service = models.ForeignKey(Services, db_column='ServiceId', related_name='number_service', on_delete=models.CASCADE)
    number = models.TextField(db_column="Number", default=None, null=True)
    price = models.FloatField(db_column="Price", default=0, null=True)
    is_paid = models.BooleanField(db_column="IsPaid", default=False)
    is_active = models.BooleanField(db_column="IsActive", default=True)
    is_deleted = models.BooleanField(db_column="IsDeleted", default=False)

    class Meta:
        db_table = 'Services_Number'
