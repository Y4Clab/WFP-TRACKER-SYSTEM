from django.shortcuts import render
from django.utils import timezone
import pytz
from django.contrib.auth.models import User
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from dotenv import dotenv_values
from Accounts.models import *
from Accounts.EmailUtils import CustomEmailBackend
from food_track.models import Vendor, Contact
from Accounts.serializers import *
from datetime import datetime, timedelta
from Accounts.utils import UserUtils

# Create your views here.
config = dotenv_values(".env")

class CreateUserView(APIView):
    http_method_names = ["post"]

    @staticmethod
    @transaction.atomic
    def post(request):
        print(request.data)
        serializer = UserProfileSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user_role = UserRoles.objects.filter(role_name = serializer.validated_data["profile_role"]).first()

        if User.objects.filter(email=serializer.validated_data["profile_email"]).exists():
            return Response({"error": "Email already exists"}, status=400)
    
        user = User.objects.create(
            first_name = serializer.validated_data["profile_firstname"],
            last_name = serializer.validated_data["profile_lastname"],
            email=serializer.validated_data["profile_email"],
            username = serializer.validated_data["profile_email"],
            is_active = False
        )

        # user.set_password(serializer.validated_data["password"])
        # user.save()

        UserProfile.objects.create(
            profile_phone = serializer.validated_data["profile_phone"],
            profile_user = user,
            profile_organization = serializer.validated_data.get("profile_organization", ""),
        )

        UsersWithRoles.objects.create(
            user_with_role_role = user_role,
            user_with_role_user = user
        )
        
        # Contact creation is now handled by the signal

        request_token = UserUtils.get_unique_token()
        AccountActivationRequestUsers.objects.create(
            account_activation_user = user,
            account_activation_token = request_token
        )

        url = config['FRONTEND_DOMAIN'] + f"auth/password-reset/{request_token}"

        body = {
            'receiver_details': user.email,
            'user': user,
            'url': url,
            'subject': "WFP portal Account activation"
        }

        CustomEmailBackend.send_messages(body, '../templates/create_password.html')
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        # # Return validation errors
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class UpdateUserView(APIView):
    http_method_names = ["post"]
    @staticmethod
    @transaction.atomic
    def post(request):
        serializer = UserProfileSerializer(data = request.data).validated_data
        if serializer.is_valid():
            print(serializer)
        try:
            profile = UserProfile.objects.filter(profile_is_active=True, profile_unique_id=serializer["profile_unique_id"]).first()
            if not profile:
                return Response({"error": "User not found"}, status=404)
            
            #update profile information
            if serializer["profile_phone"] is not None:
                profile.profile_phone = serializer["profile_phone"]
            if serializer["profile_type"] is not None:
                profile.profile_type = serializer["profile_type.value"]

            profile.save()

            # Update user information
            user = profile.profile_user
            if serializer["user_firstname"] is not None:
                user.first_name = serializer["user_firstname"]
            if serializer["user_lastname"]:
                user.last_name = serializer["user_lastname"]
            if serializer["user_email"] is not None:
                user.email = serializer["user_email"]
            user.save()

            return Response({"success": True, "data":serializer}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"error": "Failed to update user"}, status=400)


class ActivateAccountView(APIView):
    http_method_names = ["post"]
    @staticmethod
    def post(request):
        serializer = AccountActivationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer = serializer.validated_data
        try:
            requested_token = AccountActivationRequestUsers.objects.filter(account_activation_token = serializer["request_token"], account_activation_is_used = False, account_activation_is_active = True).first()
            if not requested_token:
                return Response({"error": "Invalid token"}, status=400)
            
            #set user as active
            user = requested_token.account_activation_user
            user.is_active = True
            user.set_password(serializer["password"])
            user.save()
            requested_token.account_activation_is_used = True
            requested_token.account_activation_is_active = False
            requested_token.save()
            return Response({"success": True, "data": "account activated"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"error": "Failed to activate account"}, status=400)
        
    
class ForgotPasswordView(APIView):
    http_method_names = ['post']

    @staticmethod
    def post(request):
        serializer = ForgotPasswordSerializer(data = request.data).validated_data
        try:
            user = User.objects.filter(username = serializer["email"]).first()
            if user is None:
                return Response({"error": "email not found"}, status=status.HTTP_204_NO_CONTENT)
            
            request_token = UserUtils.get_unique_token()
            naive_datetime = datetime.now()
            naive_datetime_with_timezone = timezone.make_aware(naive_datetime, timezone.utc)

            expiration_time = naive_datetime_with_timezone + timedelta(minutes=30)
            print(expiration_time)
            password_requests = ForgotPasswordRequestUser.objects.filter(request_user=user, ).first()
            
            if password_requests:
                time_diff = naive_datetime_with_timezone.second - password_requests.request_created_date.second
                time_diff = time_diff/60
                if time_diff<30:
                    return Response({"success": False, "message": "Please wait 30 minutes to reset password again."}, status=status.HTTP_400_BAD_REQUEST)
                
            ForgotPasswordRequestUser.objects.create(
                request_user=user,
                request_token=request_token,
                request_expiration_time=expiration_time  
            )

            # url = config['FRONTEND_DOMAIN'] + f"auth/password-reset/{request_token}"

            # body = {
            #     'receiver_details': user.email,
            #     'user': user,
            #     'url': url,
            #     'subject': "eTour Password Reset"
            # }

            # CustomEmailBackend.send_messages(body, '../htmls/forget_password.html')

            return Response({"success": True, "message": "email sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"success": False, "message":"Operation not successfull"}, status=status.HTTP_400_BAD_REQUEST)
            


class ResetPasswordView(APIView):
    http_method_names = ['post']

    @staticmethod
    def post(request):
        serializer = SetPasswordSerializer(data = request.data).validated_data
        try:
            requested_token = ForgotPasswordRequestUser.objects.filter(request_token = serializer["request_token"]).first()

            current_datetime = datetime.now(pytz.UTC)
            print(current_datetime)
            print(requested_token.request_expiration_time)

            request_token_expired = requested_token.request_expiration_time < current_datetime
            print("request token expired?",request_token_expired)

            if request_token_expired or requested_token is None:
                return Response({"success": False, "message":"token is expired"})
            
            user =requested_token.request_user
            user.set_password(serializer["password"])
            user.save()
            requested_token.request_is_used = True
            requested_token.save()

            return Response({"success": True, "message":"password reset successful"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"success": False, "message":"Operation not successfull"}, status=status.HTTP_400_BAD_REQUEST)
        


class DeleteUsersView(APIView):
    pass


class ChangePasswordView(APIView):
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = ChangePasswordSerializer(data = request.data).validated_data
        try:
            user = User.objects.filter(pk = request.user.id).first()
            if not user.check_password(serializer["old_password"]):
                return Response({"success": False, "data": "Incorrect password"})
            user.set_password(serializer["new_password"])
            user.save()
            
            return Response({"success": True, "message":"password changed successful"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"success": False, "message":"Operation not successfull"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class CreateUserRolesView(viewsets.ModelViewSet):
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer


class GetAllUsersView(APIView):
    # permission_classes = [IsAdminUser]
    @staticmethod
    def get(request):
        users = User.objects.all()
        page_number = request.query_params.get("page", 1)
        page_size = 1

        paginator = Paginator(users, page_size)
        try:
            paginated_users = paginator.page(page_number)
        except PageNotAnInteger:
            return Response(
                {"error": "Invalid page number."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except EmptyPage:
            return Response(
                {"error": "Page number out of range."}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = list(map(lambda x: get_user_data(x.pk), paginated_users))

        response = {
            "total_pages": paginator.num_pages,
            "current_page": paginated_users.number,
            "total_users": paginator.count,
            "users_per_page": page_size,
            "data" : data
        }

        serializer = AllUsersResponseSerializer(data = response)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    

class GetUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
        user = User.objects.filter(pk = request.user.id).first()
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user_data = get_user_data(user.pk)
        serializer = GetUserProfileSerializer(data = user_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



def get_user_data(user_id):
    print(user_id)
    user = User.objects.filter(pk = user_id).first()
    print(user.username)
    user_profile = UserProfile.objects.filter(profile_user_id = user_id).first()
    print(user_profile)
    print("haapaa")
    user_roles = UsersWithRoles.objects.filter(user_with_role_user = user_id).first()

    user_data = {
        "profile_unique_id" : user_profile.profile_unique_id,
        "profile_organization" : user_profile.profile_organization,
        "profile_firstname" : user.first_name,
        "profile_lastname" : user.last_name,
        "profile_email" : user.email,
        "profile_phone" : user_profile.profile_phone,
        "profile_type" : user_profile.profile_type,
        "user_role" : {
            "role_name" : user_roles.user_with_role_role.role_name,
            "role_description" : user_roles.user_with_role_role.role_description,
        }
    }

    return user_data