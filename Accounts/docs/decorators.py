from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import examples
from Accounts.serializers import (
    UserProfileSerializer, 
    AccountActivationSerializer, 
    ForgotPasswordSerializer,
    GetUserProfileSerializer,
    AllUsersResponseSerializer,
    SetPasswordSerializer,
    ChangePasswordSerializer
)

def login_docs(view_func):
    """Decorator to document login endpoint"""
    return swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        ),
        responses={
            200: openapi.Response(
                description="Successful authentication",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT access token'),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT refresh token'),
                        'role': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'role_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the user role'),
                                'role_description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the user role')
                            }
                        )
                    }
                )
            ),
            401: "Invalid credentials"
        },
        operation_description="Authenticate user and obtain JWT tokens with role information",
        examples={
            'application/json': examples.login_request_example
        }
    )(view_func)

def create_user_docs(view_func):
    """Decorator to document user creation endpoint"""
    return swagger_auto_schema(
        request_body=UserProfileSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Operation success status'),
                        'data': UserProfileSerializer,
                    }
                )
            ),
            400: "Bad request - Email already exists or validation error"
        },
        operation_description="Create a new user account with profile information",
        examples={
            'application/json': examples.create_user_request_example
        }
    )(view_func)

def account_activation_docs(view_func):
    """Decorator to document account activation endpoint"""
    return swagger_auto_schema(
        request_body=AccountActivationSerializer,
        responses={
            202: openapi.Response(
                description="Account activated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'data': openapi.Schema(type=openapi.TYPE_STRING, example="account activated")
                    }
                )
            ),
            400: "Invalid token or failed to activate account"
        },
        operation_description="Activate a user account with the token sent via email",
        examples={
            'application/json': examples.account_activation_request_example
        }
    )(view_func)

def forgot_password_docs(view_func):
    """Decorator to document forgot password endpoint"""
    return swagger_auto_schema(
        request_body=ForgotPasswordSerializer,
        responses={
            200: openapi.Response(
                description="Email with reset instructions sent",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="email sent")
                    }
                )
            ),
            204: "Email not found",
            400: "Operation not successful or need to wait before requesting again"
        },
        operation_description="Start the password reset process by sending a reset email",
        examples={
            'application/json': examples.forgot_password_request_example
        }
    )(view_func)

def reset_password_docs(view_func):
    """Decorator to document reset password endpoint"""
    return swagger_auto_schema(
        request_body=SetPasswordSerializer,
        responses={
            202: "Password reset successful",
            400: "Operation not successful",
            200: "Token is expired"
        },
        operation_description="Reset user password with the token received via email"
    )(view_func)

def change_password_docs(view_func):
    """Decorator to document change password endpoint"""
    return swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={
            202: "Password changed successfully",
            400: "Operation not successful",
            200: "Incorrect password"
        },
        operation_description="Change the password for an authenticated user"
    )(view_func)

def get_all_users_docs(view_func):
    """Decorator to document get all users endpoint"""
    return swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: AllUsersResponseSerializer,
            400: "Invalid page number",
            404: "Page number out of range"
        },
        operation_description="Get a paginated list of all users"
    )(view_func)

def get_user_docs(view_func):
    """Decorator to document get user profile endpoint"""
    return swagger_auto_schema(
        responses={
            200: GetUserProfileSerializer,
            404: "User not found"
        },
        operation_description="Get the profile of the currently authenticated user"
    )(view_func) 