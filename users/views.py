from rest_framework import (viewsets, status, mixins)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny)

from rest_framework_simplejwt.tokens import RefreshToken

from helpers.permissions import (IsMyProfile, EmailIsNotVerified)
from helpers.numbers import gen_rand_number

from .models import User
from .serializers import (UserLoginSerializer, UserSerializer, UserCreateSerializer, UserUpdateSerializer,
                          UserVerificationCodeSerializer)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'id': str(user.id),
        'email_is_verified': user.email_is_verified(),
        'phone_number_is_verified': user.phone_number_is_verified()
    }


class UserViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    def get_queryset(self):
        queryset = User.objects.filter(is_active=True)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer_class(self):
        if self.action in ['login']:
            return UserLoginSerializer
        elif self.action in ['update', 'create']:
            return UserUpdateSerializer
        elif self.action in ['create']:
            return UserCreateSerializer
        elif self.action in ['verify_email', 'verify_phone_number']:
            return UserVerificationCodeSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        """
        Set actions permissions.
        """
        permission_classes = []
        if self.action in ['login', 'create', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsMyProfile]
        elif self.action in ['send_email_verification_code', 'verify_email']:
            permission_classes = [EmailIsNotVerified]
        return [permission() for permission in permission_classes]

    def auth(self, serializer):
        kwargs = dict()
        if '@' in serializer.data['username_or_email']:
            kwargs['email'] = serializer.data['username_or_email']
        else:
            kwargs['username'] = serializer.data['username_or_email']

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(serializer.data['password']):
                return user
        except User.DoesNotExist:
            return None

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        context = dict()
        if serializer.is_valid():
            user = self.auth(serializer)
            if not user:
                context['detail'] = "Unable to login with provided credentials"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            context = get_tokens_for_user(user)
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)

        if serializer.is_valid():
            data = serializer.data.copy()
            del data['password2']
            user = User.objects.create_user(**data)
            context = get_tokens_for_user(user)
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def send_email_verification_code(self, request):
        user = request.user
        user.email_verification_code = gen_rand_number(6)
        user.save()
        user.email_user("Vegefoods email verification",
                        f"Your email verification code is '{user.email_verification_code}'")
        context = dict()
        context['data'] = "Email verification code sent successfully."
        return Response(context, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        user = request.user
        context = dict()
        if serializer.is_valid():
            code = serializer.data['code']
            print(code, user.email_verification_code)
            if user.email_verification_code == code:
                user.email_verified = True
                user.save()
                context['data'] = "Email verified succesfully."
                return Response(context, status=status.HTTP_200_OK)
            else:
                context['error'] = "Wrong verification code."
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
