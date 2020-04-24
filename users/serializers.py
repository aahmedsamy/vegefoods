from rest_framework import serializers
from .models import User


class UserLoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=20)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'phone_number', 'birth_date', 'first_name', 'last_name',
                  'phone_number_is_verified', 'email_is_verified']


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['image', 'username', 'email', 'phone_number', 'birth_date', 'first_name', 'last_name', 'password',
                  'password2']

    def validate(self, data):
        """
        Validate if password and password1 are identical.
        """
        errors = dict()
        if data['password'] != data['password2']:
            errors['password1'] = "'password' and 'password1' fields aren't the same!"
        if errors:
            raise serializers.ValidationError(errors)
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image', 'email', 'phone_number', 'birth_date', 'first_name', 'last_name']


class UserVerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    pass


class UserChangePasswordSerializer(serializers.Serializer):
    pass


class UserForgetUsernameSerializer(serializers.Serializer):
    pass


class UserVerifyPhoneNumber(serializers.Serializer):
    pass


class UserVerifyEmail(serializers.Serializer):
    pass
