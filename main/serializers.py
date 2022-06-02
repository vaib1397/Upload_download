from main.models import User, Operational
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        username = data["username"]
        password = data["password"]

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    raise ValidationError("User is deactivated")
            else:
                raise ValidationError("Unable to login with given credentials")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):

        user = User.objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
            password=make_password(validated_data["password"])
        )
        return user


class OperationalSerializer(serializers.ModelSerializer):
    class Meta:

        model = Operational
        fields = '__all__'


# from django.contrib.auth import authenticate, get_user_model
# from djoser.conf import settings
# from djoser.serializers import TokenCreateSerializer

# User = get_user_model()

# class CustomTokenCreateSerializer(TokenCreateSerializer):

#     def validate(self, attrs):
#         password = attrs.get("password")
#         params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
#         self.user = authenticate(
#             request=self.context.get("request"), **params, password=password
#         )
#         if not self.user:
#             self.user = User.objects.filter(**params).first()
#             if self.user and not self.user.check_password(password):
#                 self.fail("invalid_credentials")
#         # We changed only below line
#         if self.user: # and self.user.is_active:
#             return attrs
#         self.fail("invalid_credentials")
