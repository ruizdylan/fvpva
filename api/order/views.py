from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import login as login_auth
from django.contrib.auth import authenticate, logout
from django.core.exceptions import FieldError
# Create your views here.
from django.db.models import Q
from model_utils import Choices
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from api.order.models import Order, UserWallet
from api.order.serializer import UserWalletSerializer, OrderDataTableSerializer
from api.permissions import IsOauthAuthenticatedSuperAdminAndCustomer, IsOauthAuthenticatedSuperAdmin
from api.users.models import User, EmailVerificationLink, AccessLevel, Role
from api.users.serializer import UserUpdateProfileSerializer, AuthenticateSerializer, UserSerializer, \
    SocialAuthenticateSerializer
from api.views import BaseAPIView
from fapva.utils import parse_email, boolean, query_datatable_by_args_countries, query_datatable_by_args_orders


class OrderAPIView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        """
        In this api, only **Super Admin** and **Local Admin** can login. Other users won't be able to login through this API.
        **Mandatory Fields**
        * email
        * password
        """
        try:
            # data = Order.objects.filter(user_id=request.user.id, is_completed=True).order_by('-created_on')
            data = UserWallet.objects.filter(user_id=request.user.id, order__is_completed=True).order_by("-id")
            serializer = UserWalletSerializer(data, many=True)
            return self.send_response(
                success=True,
                code=f'200',
                status_code=status.HTTP_200_OK,
                payload=serializer.data,
                description="User Updated Successfully",
            )
        except User.DoesNotExist:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exist"
            )
        except FieldError:
            return self.send_response(
                code=f'500',
                description="Cannot resolve keyword given in 'order_by' into field"
            )
        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="User with this email already exists in the system."
                )
            else:
                return self.send_response(
                    code=f'500',
                    description=e
                )

    def put(self, request, pk=None):
        """
        In this api, only **Super Admin** and **Local Admin** can login. Other users won't be able to login through this API.
        **Mandatory Fields**
        * email
        * password
        """
        try:
            message = request.data.get('message', None)
            order_instance = Order.objects.get(id=pk)
            order_instance.message = message
            order_instance.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'message_receiver_{order_instance.user_id}',
                {
                    'type': 'notify_clients',
                    'message': message,
                })
            return self.send_response(
                success=True,
                code=f'200',
                status_code=status.HTTP_200_OK,
                description="Message Updated Successfully",
            )
        except User.DoesNotExist:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User doesn't exist"
            )
        except FieldError:
            return self.send_response(
                code=f'500',
                description="Cannot resolve keyword given in 'order_by' into field"
            )
        except Exception as e:
            if hasattr(e.__cause__, 'pgcode') and e.__cause__.pgcode == '23505':
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="User with this email already exists in the system."
                )
            else:
                return self.send_response(
                    code=f'500',
                    description=e
                )


class OrderDataTableAPIView(BaseAPIView):
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
            query_object = Q(is_completed=True, expire_at__gte=datetime.utcnow())
            # query_object = Q()
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
            property_ = query_datatable_by_args_orders(
                kwargs=request.query_params,
                model=Order,
                query_object=query_object,
                ORDER_COLUMN_CHOICES=ORDER_COLUMN_CHOICES,
                search_function=self.search_countries
            )

            serializer = OrderDataTableSerializer(property_.get('items', []), many=True)

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

        except Order.DoesNotExist as e:
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
            query_object = Q(id__icontains=search_value) | Q(number__icontains=search_value)
            return queryset.filter(query_object)
        except:
            return []
