from drf_yasg import openapi

# Login examples
login_request_example = {
    "username": "user@example.com",
    "password": "secure_password123"
}

login_response_example = {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "role": {
        "role_name": "Admin",
        "role_description": "System Administrator"
    }
}

# User registration examples
create_user_request_example = {
    "profile_firstname": "John",
    "profile_lastname": "Doe",
    "profile_email": "john.doe@example.com",
    "profile_phone": "+1-555-123-4567",
    "profile_role": "Admin",
    "profile_organization": "WFP",
    "profile_type": "Organization_Admin"
}

create_user_response_example = {
    "success": True,
    "data": {
        "profile_firstname": "John",
        "profile_lastname": "Doe",
        "profile_email": "john.doe@example.com",
        "profile_phone": "+1-555-123-4567",
        "profile_role": "Admin",
        "profile_organization": "WFP",
        "profile_type": "Organization_Admin"
    }
}

# Account activation examples
account_activation_request_example = {
    "request_token": "abc123def456",
    "password": "new_secure_password123"
}

account_activation_response_example = {
    "success": True,
    "data": "account activated"
}

account_activation_error_example = {
    "error": "Invalid token"
}

# Forgot password examples
forgot_password_request_example = {
    "email": "user@example.com"
}

forgot_password_response_example = {
    "success": True,
    "message": "email sent"
}

email_not_found_example = {
    "error": "email not found"
}

wait_before_reset_example = {
    "success": False,
    "message": "Please wait 30 minutes to reset password again."
}

# Get all users example
get_all_users_response_example = {
    "total_pages": 10,
    "current_page": 1,
    "total_users": 100,
    "users_per_page": 10,
    "data": [
        {
            "profile_unique_id": "123e4567-e89b-12d3-a456-426614174000",
            "profile_organization": "WFP",
            "profile_firstname": "John",
            "profile_lastname": "Doe",
            "profile_email": "john.doe@example.com",
            "profile_phone": "+1-555-123-4567",
            "profile_type": "Organization_Admin",
            "user_role": {
                "role_name": "Admin",
                "role_description": "System Administrator"
            }
        }
    ]
} 