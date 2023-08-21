import io
import json
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import boto3
import requests
from PIL import Image
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Case, When


def parse_email(obj):
    return obj.replace(" ", "").lower()


def get_epoch_time(to_string=False):
    """
    return epoch time
    :param to_string: Boolean, True means convert to String
    :return:
    """
    seconds = int(time.time())
    if to_string:
        return str(seconds)
    return seconds


def slugify_name(string_):
    """
    Convert given string into slugify
    :param string_: String
    :return: String
    """
    if string_:
        slugify_str = '_'.join(string_.split(' '))
        return slugify_str
    return string_


def slugify_name_hyphne(string_):
    """
    Convert given string into slugify
    :param string_: String
    :return: String
    """
    if string_:
        slugify_str = '-'.join(string_.split(' '))
        return slugify_str.lower()
    return string_


def boolean(value):
    """Parse the string ``"true"`` or ``"false"`` as a boolean (case
    insensitive). Also accepts ``"1"`` and ``"0"`` as ``True``/``False``
    (respectively). If the input is from the request JSON body, the type is
    already a native python boolean, and will be passed through without
    further parsing.
    """
    if isinstance(value, bool):
        return value

    if value is None:
        raise ValueError("boolean type must be non-null")
    value = str(value).lower()
    if value in ('true', 'yes', '1', 1):
        return True
    if value in ('false', 'no', '0', 0, ''):
        return False
    raise ValueError("Invalid literal for boolean(): {0}".format(value))


def image_directory_path(instance, filename):
    """
    file will be uploaded to MEDIA_ROOT path
    :param instance: Image Object
    :param filename:  Filename
    :return:
    """
    epoch_time = get_epoch_time(to_string=True)
    slugify_filename = slugify_name(filename)
    file_name = f'{epoch_time}_{slugify_filename}'
    return file_name


def query_datatable_by_args_countries(kwargs, model, query_object, ORDER_COLUMN_CHOICES, search_function):
    """
    :param dict kwargs: request param from datatable
    :param obj model: on which you want to perform action
    :param obj query_object: contains the query to filter database
    :param choices ORDER_COLUMN_CHOICES: all columns on datatable
    :param function search_function: customize function to perform search
    :rtype: dict
    """

    try:

        # start_date = kwargs.get('start_date')
        # try:
        #     start_date = datetime.strptime(str(start_date), '%Y-%m-%dT%H:%M')
        # except:
        #     start_date = datetime.strptime(str(start_date), '%Y/%m/%d %H:%M')
        #
        # # start_date = start_date - timedelta(hours=5)
        # end_date = kwargs.get('end_date')
        #
        # try:
        #     end_date = datetime.strptime(str(end_date), '%Y-%m-%dT%H:%M')
        # except:
        #     end_date = datetime.strptime(str(end_date), '%Y/%m/%d %H:%M')
        # end_date = end_date - timedelta(hours=5)
        # print(start_date)
        # print(end_date)
        # type = int(kwargs.get('status'))

        draw = int(kwargs.get('draw', 0))
        #  start
        start = int(kwargs.get('start', 0))
        #  length (limit)
        length = int(kwargs.get('length', 0))
        # data search
        search_value = kwargs.get('search[value]')
        order_column = kwargs.get('order[0][column]', 0)
        order = kwargs.get('order[0][dir]', None)

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # for asc we want latest record first
        if order == 'asc':
            order_column = f'-{order_column}'

        # if type ==
        queryset = model.objects.filter(query_object)
        # Set record total
        total = queryset.count()

        # this is value that uer type in search box or user select from deopdown
        if search_value:
            queryset = search_function(queryset, search_value, kwargs)
        try:
            count = queryset.count()
        except:
            count = 0

        try:
            queryset = queryset.order_by('-is_active')[start:start + length]
        except:
            queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
    except Exception as e:
        return {
            'exception': e,
            'items': [],
            'count': 0,
            'total': 0,
            'draw': 0
        }


def query_datatable_by_args_orders(kwargs, model, query_object, ORDER_COLUMN_CHOICES, search_function):
    """
    :param dict kwargs: request param from datatable
    :param obj model: on which you want to perform action
    :param obj query_object: contains the query to filter database
    :param choices ORDER_COLUMN_CHOICES: all columns on datatable
    :param function search_function: customize function to perform search
    :rtype: dict
    """

    try:

        # start_date = kwargs.get('start_date')
        # try:
        #     start_date = datetime.strptime(str(start_date), '%Y-%m-%dT%H:%M')
        # except:
        #     start_date = datetime.strptime(str(start_date), '%Y/%m/%d %H:%M')
        #
        # # start_date = start_date - timedelta(hours=5)
        # end_date = kwargs.get('end_date')
        #
        # try:
        #     end_date = datetime.strptime(str(end_date), '%Y-%m-%dT%H:%M')
        # except:
        #     end_date = datetime.strptime(str(end_date), '%Y/%m/%d %H:%M')
        # end_date = end_date - timedelta(hours=5)
        # print(start_date)
        # print(end_date)
        # type = int(kwargs.get('status'))

        draw = int(kwargs.get('draw', 0))
        #  start
        start = int(kwargs.get('start', 0))
        #  length (limit)
        length = int(kwargs.get('length', 0))
        # data search
        search_value = kwargs.get('search[value]')
        order_column = kwargs.get('order[0][column]', 0)
        order = kwargs.get('order[0][dir]', None)

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # for asc we want latest record first
        if order == 'asc':
            order_column = f'-{order_column}'

        # if type ==
        queryset = model.objects.filter(query_object)
        # Set record total
        total = queryset.count()

        # this is value that uer type in search box or user select from deopdown
        if search_value:
            queryset = search_function(queryset, search_value, kwargs)
        try:
            count = queryset.count()
        except:
            count = 0

        try:
            queryset = queryset.order_by('-expire_at')[start:start + length]
        except:
            queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
    except Exception as e:
        return {
            'exception': e,
            'items': [],
            'count': 0,
            'total': 0,
            'draw': 0
        }


def paypal_generate_access_token():
    try:
        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_SECRET_ID
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': 'client_credentials'
        }
        r = requests.post(f"{settings.PAYPAL_URL}v1/oauth2/token", body, headers,
                          auth=(client_id, client_secret))
        if r.status_code == 200:
            return json.loads(r.content.decode("utf-8"))['access_token']
        return None
    except:
        return None


def paypal_generate_client_access_token(token):
    try:
        url = f"{settings.PAYPAL_URL}v1/identity/generate-token"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        response = requests.request("POST", url, headers=headers)
        print(response.text)
        if response.status_code == 200:
            return json.loads(response.content.decode("utf-8"))['client_token']
        return None
    except Exception as e:
        return None