from django.db import models

# Create your models here.
from fapva.utils import image_directory_path


class Log(models.Model):
    """ Abstract model containing common fields."""
    created_by = models.BigIntegerField(
        db_column='CreatedBy', null=True, blank=True, default=0)
    created_on = models.DateTimeField(db_column='CreatedOn', auto_now_add=True)
    modified_by = models.BigIntegerField(
        db_column='ModifiedBy', default=0, null=True, blank=True)
    modified_on = models.DateTimeField(db_column='ModifiedOn', auto_now=True)

    class Meta:
        abstract = True


class Countries(models.Model):
    name = models.CharField(db_column="Name", blank=True, null=True, max_length=255)
    slug = models.CharField(db_column="Slug", blank=True, null=True, max_length=255)
    code = models.CharField(db_column="Code", blank=True, null=True, max_length=255)
    flag = models.FileField(db_column="Flag", blank=True, null=True, upload_to=image_directory_path)
    dialling_code = models.CharField(db_column="DialingCode", blank=True, null=True, max_length=255)
    currency_code = models.CharField(db_column="CurrencyCode", blank=True, null=True, max_length=255)
    currency_name = models.CharField(db_column="CurrencyName", blank=True, null=True, max_length=255)
    language_code = models.CharField(db_column="LanguageCode", blank=True, null=True, max_length=255)
    language_name = models.CharField(db_column="LanguageName", blank=True, null=True, max_length=255)
    is_active = models.BooleanField(db_column="IsActive", default=False)
    is_deleted = models.BooleanField(db_column="IsDeleted", default=False)

    class Meta:
        db_table = 'Countries'
