# Create your views here.
import datetime
import json

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import transaction
from django.db.models import Q, Sum
from model_utils import Choices
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser

from api.main.serializer import CountriesDataTableSerializer
from api.order.models import Order, UserWallet
from api.order.serializer import OrderDataTableSerializer
from api.permissions import IsOauthAuthenticatedSuperAdmin, IsGETorIsOauthAuthenticatedSuperAdmin, \
    IsOauthAuthenticatedSuperAdminAndCustomer
from api.services.models import ServiceNumber
from api.services.serializer import ServicesNumberHomeSerializer
from api.views import BaseAPIView
from fapva.utils import query_datatable_by_args_countries
from main.models import Countries


class CountriesDataTableAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            query_object = Q(is_deleted=False)
            # city = request.query_params.get('city', "")
            # type = request.query_params.get('type', "")
            query = request.query_params.get('query', '')
            #
            # premium_request = request.query_params.get('premium_request', None)
            # featured_request = request.query_params.get('featured_request', None)
            # if city:
            #     query_object = ()
            # query_object = Q()
            # activated = request.query_params.get('status', '3')
            # if query:
            #     query_object &= Q(status=int(query))
            # else:
            #     query_object &= Q(status__in=[0, 1, 2, 3])
            # elif status == '2':
            #     expired = True
            # if status == '3':
            #     query_object = Q(status__in=[1, 2])
            # elif status == '4':
            #     query_object = Q(is_expired=True, status__in=[1, 2])
            # elif activated == '2':
            #     query_object = Q(status=int(activated)) | Q(is_expired=True, status=1)
            # elif activated == '1':
            #     query_object = Q(is_expired=False, status=int(activated))

            # if type:
            #     query_object &= Q(type=type)
            # if city:
            #     query_object &= Q(city=city)
            # if is_approved:
            #     query_object &= Q(is_approved=boolean(is_approved))
            ORDER_COLUMN_CHOICES = Choices(
                ('0', 'id'),
                ('1', 'type'),
                ('4', 'id'),
                ('6', 'description'),
                ('7', 'price')
            )
            property_ = query_datatable_by_args_countries(
                kwargs=request.query_params,
                model=Countries,
                query_object=query_object,
                ORDER_COLUMN_CHOICES=ORDER_COLUMN_CHOICES,
                search_function=self.search_countries
            )

            serializer = CountriesDataTableSerializer(property_.get('items', []), many=True)

            property_data = {
                'draw': property_.get('draw', 0),
                'recordsTotal': property_.get('total', 0),
                'recordsFiltered': property_.get('count', 0),
                'data': serializer.data,
            }
            description = 'List of jobs'

            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                payload=property_data,
                description=description
            )

        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

    @staticmethod
    def search_countries(queryset, search_value, kwargs):
        """
        search given queryset with given search_value
        :param list queryset: all records of a model
        :param str search_value: value user enter in datatable search
        :param dict kwargs: request param from datatable
        :rtype:list
        """
        try:
            query_object = Q(id__icontains=search_value) | Q(name__icontains=search_value)
            query_object |= Q(slug__icontains=search_value)
            return queryset.filter(query_object)
        except:
            return []


class CountriesStatusUpdateAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            country = Countries.objects.get(id=pk)
            country.is_active = not country.is_active
            country.save()
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                description="Status Changed Successfully"
            )

        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

    @staticmethod
    def search_countries(queryset, search_value, kwargs):
        """
        search given queryset with given search_value
        :param list queryset: all records of a model
        :param str search_value: value user enter in datatable search
        :param dict kwargs: request param from datatable
        :rtype:list
        """
        try:
            query_object = Q(id__icontains=search_value) | Q(name__icontains=search_value)
            query_object |= Q(slug__icontains=search_value)
            return queryset.filter(query_object)
        except:
            return []


class CountriesAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsGETorIsOauthAuthenticatedSuperAdmin,)
    parser_classes = (MultiPartParser,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            country = Countries.objects.filter(is_active=True, is_deleted=False).order_by("name")
            serializer = CountriesDataTableSerializer(country, many=True)
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                payload=serializer.data,
                description="Country Data"
            )

        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )

    def post(self, request, pk=None):
        try:
            serializer = CountriesDataTableSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=serializer.data,
                    description='Country Created Successfully',
                )
            else:
                return self.send_response(
                    success=False,
                    code='422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Country with this name already exists"
                )
            return self.send_response(
                code=f'500',
                description=e
            )

    def put(self, request, pk=None):
        try:
            instance = Countries.objects.get(id=pk)
            serializer = CountriesDataTableSerializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=serializer.data,
                    description='Country Updated Successfully',
                )
            else:
                return self.send_response(
                    success=False,
                    code='422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Country with this name already exists"
                )
            return self.send_response(
                code=f'500',
                description=e
            )


class CountriesDeleteAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            country = Countries.objects.get(id=pk)
            country.is_deleted = True
            country.save()
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                description="Deleted Successfully"
            )

        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )


class PaypalOrderAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def post(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            with transaction.atomic():
                service_data = ServiceNumber.objects.get(id=request.data.get("number_id"))
                url = f"{settings.PAYPAL_URL}v2/checkout/orders"
                payload = json.dumps({
                    "intent": "CAPTURE",
                    "purchase_units": [
                        {
                            "amount": {
                                "currency_code": "USD",
                                "value": f'{service_data.price}'
                            }
                        }
                    ]
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {request.data.get("token")}'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                data = json.loads(response.content.decode("utf-8"))
                Order.objects.create(
                    number_id=service_data.id,
                    number=service_data.number,
                    country_id=service_data.country.id,
                    country_name=service_data.country.name,
                    order_id=data['id'],
                    price=service_data.price,
                    user=request.user,
                )

                return self.send_response(
                    success=True,
                    payload=data,
                    status_code=status.HTTP_200_OK,
                    description="Status Changed Successfully"
                )
        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )


class PaypalOrderCaptureAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def post(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            with transaction.atomic():
                url = f"{settings.PAYPAL_URL}v2/checkout/orders/{pk}/capture"
                payload = json.dumps({})
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {request.data.get("token")}'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                data = json.loads(response.content.decode("utf-8"))
                capture_id = data['purchase_units'][0]['payments']['captures'][0]['id']
                order_instance = Order.objects.get(order_id=pk)
                order_instance.response_json = json.dumps(data)
                order_instance.capture_id = capture_id
                order_instance.payment_channel = "paypal-account"
                order_instance.is_completed = True
                order_instance.expire_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
                order_instance.save()

                UserWallet.objects.create(
                    balance=0,
                    user=request.user,
                    order=order_instance,
                    is_refunded=False,
                    order_placed=True
                )

                # Send notification to WebSocket clients
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'bought_numbers',
                    {
                        'type': 'notify_clients',
                        'message': OrderDataTableSerializer(order_instance).data,
                    })

                return self.send_response(
                    success=True,
                    payload={
                        "order_id": order_instance.id,
                        "expire_at": order_instance.expire_at,
                        "capture_payload": data
                    },
                    status_code=status.HTTP_200_OK,
                    description="Status Changed Successfully"
                )
        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )


class OrderCancelAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            order_instance = Order.objects.get(id=pk)
            if str(order_instance.expire_at) < str(datetime.datetime.utcnow()):
                return self.send_response(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="You order has been expired or used. You can not cancel it now"
                )
            UserWallet.objects.create(
                balance=order_instance.price,
                user=request.user,
                order=order_instance,
                is_refunded=True,
                order_placed=False
            )
            order_instance.is_completed = False
            # order_instance.refunded_reason = request.data.get("refunded_reason", None)
            order_instance.is_refunded = True
            order_instance.save()
            return self.send_response(
                success=True,
                status_code=status.HTTP_200_OK,
                description="Order Canceled Successfully Successfully"
            )
        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )


class OrderWalletPayAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def get(self, request, pk=None):
        """
        :param request:
        :param pk: to get singal instance of property
        :return: response of required properties listings
        """
        try:
            service_data = ServiceNumber.objects.get(id=pk)
            balance = UserWallet.objects.filter(user_id=request.user.id).aggregate(total=Sum("balance"))['total']
            balance = balance if balance else 0
            if balance < service_data.price:
                return self.send_response(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Sorry, you don't have enough credits to buy this service"
                )
            order = Order.objects.create(
                number_id=service_data.id,
                number=service_data.number,
                country_id=service_data.country.id,
                country_name=service_data.country.name,
                price=service_data.price,
                user=request.user,
                is_completed=True,
                payment_channel="wallet"
            )
            UserWallet.objects.create(
                user_id=request.user.id,
                order_id=order.id,
                balance=-abs(service_data.price),
                order_placed=True,
                is_refunded=False
            )
            return self.send_response(
                success=True,
                payload={
                  "order_id": order.id
                },
                status_code=status.HTTP_200_OK,
                description="Order Placed Successfully"
            )
        except Countries.DoesNotExist as e:
            return self.send_response(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description=str(e)
            )
        except Exception as e:
            return self.send_response(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                description=str(e)
            )
