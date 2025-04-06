from drf_yasg import openapi

# Authentication schemas
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['username', 'password'],
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
    }
)

login_response = openapi.Response(
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
)

# User Registration schemas
create_user_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['profile_firstname', 'profile_lastname', 'profile_email', 'profile_phone', 'profile_role'],
    properties={
        'profile_firstname': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
        'profile_lastname': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
        'profile_email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
        'profile_phone': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
        'profile_role': openapi.Schema(type=openapi.TYPE_STRING, description='User role name'),
        'profile_organization': openapi.Schema(type=openapi.TYPE_STRING, description='User organization'),
        'profile_type': openapi.Schema(type=openapi.TYPE_STRING, description='User type'),
    }
)

create_user_response = openapi.Response(
    description="User created successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Operation success status'),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'profile_firstname': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_lastname': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_email': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_phone': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_role': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_organization': openapi.Schema(type=openapi.TYPE_STRING),
                    'profile_type': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )
        }
    )
)

# Account Activation schemas
account_activation_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['request_token', 'password'],
    properties={
        'request_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token received via email'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password to set'),
    }
)

account_activation_response = openapi.Response(
    description="Account activated successfully",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            'data': openapi.Schema(type=openapi.TYPE_STRING, example="account activated")
        }
    )
)

account_activation_error = openapi.Response(
    description="Invalid token or failed to activate account",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(type=openapi.TYPE_STRING, example="Invalid token")
        }
    )
)

# Forgot Password schemas
forgot_password_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email'],
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the user'),
    }
)

forgot_password_response = openapi.Response(
    description="Email with reset instructions sent",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
            'message': openapi.Schema(type=openapi.TYPE_STRING, example="email sent")
        }
    )
)

email_not_found_response = openapi.Response(
    description="Email not found",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(type=openapi.TYPE_STRING, example="email not found")
        }
    )
)

wait_before_reset_response = openapi.Response(
    description="Operation not successful or need to wait before requesting again",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            'message': openapi.Schema(type=openapi.TYPE_STRING, example="Please wait 30 minutes to reset password again.")
        }
    )
)

# Get All Users schemas
get_all_users_parameters = [
    openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER)
] 