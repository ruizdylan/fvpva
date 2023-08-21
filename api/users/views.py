from datetime import datetime

from django.contrib.auth import login as login_auth
from django.contrib.auth import authenticate, logout
from django.core.exceptions import FieldError
# Create your views here.
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOauthAuthenticatedSuperAdminAndCustomer, IsOauthAuthenticatedSuperAdmin
from api.users.models import User, EmailVerificationLink, AccessLevel, Role
from api.users.serializer import UserUpdateProfileSerializer, AuthenticateSerializer, UserSerializer, \
    SocialAuthenticateSerializer
from api.views import BaseAPIView
from fapva.utils import parse_email, boolean


class UserProfileUpdateView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def put(self, request, pk=None):
        """
        In this api, only **Super Admin** and **Local Admin** can login. Other users won't be able to login through this API.
        **Mandatory Fields**
        * email
        * password
        """
        try:
            user_data = User.objects.get(id=request.user.id)
            # user = User
            serializer = UserUpdateProfileSerializer(instance=user_data,
                                                     data=request.data)
            if serializer.is_valid():
                serializer.save()
                return self.send_response(
                    success=True,
                    code=f'200',
                    status_code=status.HTTP_200_OK,
                    payload=UserUpdateProfileSerializer(serializer.instance).data,
                    description="User Updated Successfully",
                )
            else:
                return self.send_response(
                    success=True,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors,
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


class UserProfilePasswordView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdminAndCustomer,)

    def put(self, request, pk=None):
        """
        In this api, only **Super Admin** and **Local Admin** can login. Other users won't be able to login through this API.
        **Mandatory Fields**
        * email
        * password
        """
        try:
            user_data = User.objects.get(id=request.user.id)
            if not request.data['new_password']:
                return self.send_response(
                    success=True,
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Password Required",
                )
            else:
                if user_data.check_password(request.data['old_password']):
                    user_data.set_password(request.data['new_password'])
                    user_data.save()
                    # user = User
                    return self.send_response(
                        success=True,
                        code=f'200',
                        status_code=status.HTTP_200_OK,
                        description="Password Updated Successfully",
                    )
                else:
                    return self.send_response(
                        success=True,
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description="Invalid Password",
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


class LoginView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            serializer = AuthenticateSerializer(data=request.data)
            if serializer.is_valid():
                email = parse_email(serializer.data.get('email'))
                password = serializer.data.get('password')
                user = authenticate(request, email=email, password=password)
                if user:
                    if user.is_active:
                        # token, created = Token.objects.create(user=user)
                        oauth_token = self.get_oauth_token(email, password)
                        if 'access_token' in oauth_token:

                            # user_data = {'access_token': oauth_token.get('access_token'),
                            #              'refresh_token': oauth_token.get('refresh_token')}
                            serialized = UserUpdateProfileSerializer(User.objects.get(id=user.id))
                            user_data = serialized.data
                            user_data['access_token'] = oauth_token.get('access_token')
                            user_data['refresh_token'] = oauth_token.get('refresh_token')
                            login_auth(request, user)
                            # user_data['refresh_token'] = oauth_token.get('refresh_token')
                            return self.send_response(success=True,
                                                      code=f'200',
                                                      status_code=status.HTTP_200_OK,
                                                      payload=user_data,
                                                      description='You are logged in!',
                                                      )
                        else:
                            return self.send_response(description='Something went wrong with Oauth token generation.',
                                                      code=f'500')
                    else:
                        description = 'Your account is blocked or deleted.'
                        return self.send_response(success=False,
                                                  code=f'422',
                                                  status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                  payload={},
                                                  description=description)
                else:
                    return self.send_response(
                        success=False,
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        payload={}, description='Email or password is incorrect.'
                    )
            else:
                return self.send_response(
                    success=False,
                    code='422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Exception as e:
            return self.send_response(
                code=f'500',
                description=e
            )


class RegisterView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['role'] = Role.objects.get(code=AccessLevel.CUSTOMER_CODE)
                serializer.save(**validated_data)
                password = request.data.get('password')
                email = parse_email(request.data.get('email'))
                serializer.instance.set_password(password)
                serializer.instance.save()
                user = authenticate(request, email=email, password=password)
                if serializer.instance:
                    if serializer.instance.is_active:
                        oauth_token = self.get_oauth_token(email, password)
                        if 'access_token' in oauth_token:
                            user_data = UserSerializer(serializer.instance).data
                            user_data['access_token'] = oauth_token.get('access_token')
                            user_data['refresh_token'] = oauth_token.get('refresh_token')
                            login_auth(request, user)
                            return self.send_response(success=True,
                                                      code=f'200',
                                                      status_code=status.HTTP_200_OK,
                                                      payload=user_data,
                                                      description='You are logged in!',
                                                      )
                        else:
                            return self.send_response(description='Something went wrong with Oauth token generation.',
                                                      code=f'500')
                    else:
                        description = 'Your account is blocked or deleted.'
                        return self.send_response(success=False,
                                                  code=f'422',
                                                  status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                                  payload={},
                                                  description=description)
                else:
                    return self.send_response(
                        success=False,
                        code=f'422',
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        payload={}, description='Email or password is incorrect.'
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
                    description="User with this email already exists in the system."
                )
            return self.send_response(
                code=f'500',
                description=e
            )


class LogoutView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION", "").replace("Token ", "")
            get_token = Token.objects.filter(pk=token).first()

            if not get_token:
                return self.send_response(code=f'422',
                                          status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                          description="User doesn't logout")
            logout(request)
            get_token.delete()
            return self.send_response(success=True,
                                      code=f'201', status_code=status.HTTP_201_CREATED,
                                      payload={},
                                      description='User logout successfully'
                                      )
        except User.DoesNotExist:
            return self.send_response(code=f'422',
                                      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                      description="User doesn't exists")
        except FieldError:
            return self.send_response(code=f'500',
                                      description="Cannot resolve keyword given in 'order_by' into field")
        except Exception as e:
            return self.send_response(code=f'500',
                                      description=e)


# class VerifyInvitationLink(BaseAPIView):
#     """
#     Verify the Link of the Local Admin
#     """
#     authentication_classes = ()
#     permission_classes = ()
#
#     def post(self, request, pk=None):
#         """
#         In this API, we will validate the **Local Admin** token. Whether it is a valid token, or unexpired.
#         If it is, it will return the user_id using which **Local Admin** will update his/her password
#         """
#         try:
#             verify = EmailVerificationLink.objects.get(token=request.data['token'], code=request.data['code'])
#             if datetime.date(verify.expiry_at) <= datetime.date(datetime.now()):
#                 EmailVerificationLink.add_email_token_link(verify.user)
#                 verify.delete()
#                 return self.send_response(
#                     code=f'422',
#                     status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                     description="The link is expired. New link has been sent to your email"
#                 )
#             else:
#                 return self.send_response(
#                     success=True,
#                     code=f'201',
#                     status_code=status.HTTP_201_CREATED,
#                     payload={"user_id": verify.user_id},
#                     description="Token Verified Successfully"
#                 )
#         except EmailVerificationLink.DoesNotExist:
#             return self.send_response(
#                 code=f'422',
#                 status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 description="Verification token doesn't exists"
#             )
#         except Exception as e:
#             return self.send_response(
#                 code=f'500',
#                 description=e
#             )


class UpdatePassword(BaseAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        """
        In this API, we will validate the **Local Admin** token. Whether it is a valid token, or unexpired.
        If it is, it will return the user_id using which **Local Admin** will update his/her password
        """
        try:
            verify = EmailVerificationLink.objects.get(token=request.data['token'],
                                                       )
            if datetime.date(verify.expiry_at) <= datetime.date(datetime.now()):
                EmailVerificationLink.add_email_token_link(verify.user)
                verify.delete()
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="The link is expired. New link has been sent to your email"
                )
            else:
                verify.user.set_password(request.data["password"])
                verify.user.save(update_fields=["password"])
                verify.delete()
            return self.send_response(
                success=True,
                code=f'201',
                status_code=status.HTTP_201_CREATED,
                description="Password Updated"
            )
        except EmailVerificationLink.DoesNotExist:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Verification token doesn't exists"
            )
        except Exception as e:
            return self.send_response(
                code=f'500',
                description=e
            )


class ForgotPasswordView(BaseAPIView):
    parser_class = ()
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            if request.data['email'] == "" or None:
                return self.send_response(
                    code=f'422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description="Email required"
                )
            else:
                user = User.objects.get(email__exact=parse_email(request.data['email']))
                obj = EmailVerificationLink.add_email_token_link(user)
                # send_email_sendgrid_template(from_email=settings.SUPPORT_MAIL,
                #                              to_email=user.email,
                #                              data={"first_name": user.first_name,
                #                                    "otp": obj.code}
                #                              ,
                #                              template=settings.FORGOT_PASSWORD_TEMPLATE_ID
                #                              )

                return self.send_response(
                    success=True,
                    code=f'201',
                    payload={"key": obj.token,
                             },
                    status_code=status.HTTP_201_CREATED,
                    description="Forgot Password mail sent successfully",
                )
        except User.DoesNotExist:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="User does not exists"
            )
        except Exception as e:
            return self.send_response(
                code=f'500',
                description=e
            )


class UserView(BaseAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsOauthAuthenticatedSuperAdmin,)

    def get(self, request, pk=None):
        try:
            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))
            active = request.query_params.get('active', None)
            q = request.query_params.get('q', None)
            query_set = Q(role__code=AccessLevel.CUSTOMER_CODE)

            if q:
                query_set &= Q(first_name__icontains=q) | \
                             Q(last_name__icontains=q) | \
                             Q(email__icontains=q)
            if active:
                query_set &= Q(is_active=boolean(active))
            if pk:
                query_set &= Q(id=pk)
                query = User.objects.get(query_set)
                serializer = UserSerializer(query)
                count = 1
            else:
                query = User.objects.filter(
                    query_set
                ).order_by('-id')
                serializer = UserSerializer(
                    query[offset:limit + offset],
                    many=True,
                )

                count = query.count()
            return self.send_response(
                success=True,
                code='200',
                status_code=status.HTTP_200_OK,
                payload=serializer.data,
                count=count
            )
        except User.DoesNotExist:
            return self.send_response(
                success=False,
                code='422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='User Does`t Exist'
            )
        except FieldError as e:
            return self.send_response(
                success=False,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                code=f'422',
                description=str(e)
            )

        except Exception as e:
            return self.send_response(
                success=False,
                description=e)


class SocialLoginView(BaseAPIView):
    """
    API View for Login Super Admin and Admin
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, pk=None):
        try:
            serializer = SocialAuthenticateSerializer(data=request.data)
            if serializer.is_valid():
                oauth_token = self.convert_oauth_token(token=serializer.data["token"],
                                                       backend=serializer.data["backend"], request=request)
                if 'access_token' in oauth_token:

                    #
                    user_data = UserSerializer(oauth_token.get("user")).data

                    user_data['access_token'] = oauth_token.get('access_token')
                    return self.send_response(success=True,
                                              code=f'200',
                                              status_code=status.HTTP_200_OK,
                                              payload=user_data,
                                              description=_('You are logged in!'),
                                              )
                elif oauth_token.get("sign_up_required", None):
                    return self.send_response(success=True,
                                              code=f'200',
                                              status_code=status.HTTP_200_OK,
                                              payload={"sign_up_required": True},
                                              )

                else:
                    payload = {}

                    return self.send_response(
                        success=False,
                        code=f'422',
                        payload=payload,
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        description=str(oauth_token)
                    )
            else:
                return self.send_response(
                    success=False,
                    code='422',
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    description=serializer.errors
                )
        except Exception as e:
            return self.send_response(code=f'500',
                                      description=e)
