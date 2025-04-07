from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from Accounts.models import *
from django.contrib.auth.password_validation import validate_password


class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get the user from the token
        user = self.user
        
        # Get the user's role
        user_with_role = UsersWithRoles.objects.filter(user_with_role_user=user).first()
        if user_with_role:
            role = user_with_role.user_with_role_role
            data.update({'role': role.role_name})
        
        return data


class UserProfileSerializer(serializers.Serializer):
    profile_unique_id = serializers.CharField(required = False, allow_blank = True)
    profile_organization = serializers.CharField(required=False, allow_blank=True)
    profile_firstname = serializers.CharField(required=True)
    profile_lastname = serializers.CharField(required=True)
    profile_email = serializers.EmailField(required=True)
    profile_phone = serializers.CharField(required=True)
    profile_type = serializers.CharField(required=False, allow_blank=True)
    profile_role = serializers.CharField(required=False)
    # password = serializers.CharField(
    #     write_only=True, 
    #     required=True,
    #     validators=[validate_password],  # Uses Django's built-in password validators
    #     style={"input_type": "password"}  # Ensures password field is hidden in forms
    # )

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = ["role_name", "role_description"]

class GetUserProfileSerializer(serializers.Serializer):
    profile_unique_id = serializers.UUIDField()
    profile_organization = serializers.CharField(required=False, allow_blank=True)
    profile_firstname = serializers.CharField(required=True)
    profile_lastname = serializers.CharField(required=True)
    profile_email = serializers.EmailField(required=True)
    profile_phone = serializers.CharField(required=True)
    profile_type = serializers.CharField(required=False, allow_blank=True)
    user_role = UserRolesSerializer()


class AllUsersResponseSerializer(serializers.Serializer):
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_users = serializers.IntegerField()
    users_per_page = serializers.IntegerField()
    data = GetUserProfileSerializer(many = True)


class AccountActivationSerializer(serializers.Serializer):
    request_token = serializers.CharField(required=True)
    # password = serializers.CharField(
    #     write_only=True, 
    #     required=True,
    #     validators=[validate_password],  # Uses Django's built-in password validators
    #     style={"input_type": "password"}  # Ensures password field is hidden in forms
    # )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    request_token = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],  # Uses Django's built-in password validators
        style={"input_type": "password"}  # Ensures password field is hidden in forms
    )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],  # Uses Django's built-in password validators
        style={"input_type": "password"}  # Ensures password field is hidden in forms
        )
    new_password = serializers.CharField(
        write_only=True, 
        required=True,
        validators=[validate_password],  # Uses Django's built-in password validators
        style={"input_type": "password"}  # Ensures password field is hidden in forms
    )

