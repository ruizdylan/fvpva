import csv
import json
import unicodedata

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from main.models import Countries


def get_slugify_name(text):
    try:
        name_ascii = unicodedata.normalize(
            'NFKD', text).encode('ascii', 'ignore')
        name_ascii = name_ascii.decode("utf-8")
        return name_ascii
    except UnicodeDecodeError:
        pass
    except Exception:
        pass

    return ''


def get_or_create_country(obj):
    """
    Get or create a Country Object
    :param country_data: Country attributes in DICT
    :return: Country Object
    """

    try:
        country = Countries.objects.get(code__iexact=slugify(obj['name']))
        print("Country Already Exists")
    except Countries.DoesNotExist:
        json_dump = {
            "name": obj['name'],
            "code": obj['code'],
            "slug": slugify(obj['name']),
            "flag": obj['flag'],
            "dialling_code": obj['dialling_code'],
            "currency_code": obj['currency']['code'],
            "currency_name": obj['currency']['name'],
            "language_code": obj['language']['code'],
            "language_name": obj['language']['name'],
        }
        country = Countries(
            **json_dump
        )
        print("Country Created Successfully")
        country.save()
    return country


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            file_path = staticfiles_storage.path('countries.json')
            file = open(file_path, encoding="utf8")
            data = json.load(file)
            for obj in data:
                get_or_create_country(obj)
        except Exception as e:
            print(e)
