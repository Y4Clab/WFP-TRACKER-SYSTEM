from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from Accounts.views import *

urlpatterns = [
    path("register/", view=CreateUserView.as_view(), name="create_user"),
    path("update_user/", view=UpdateUserView.as_view(), name="update_user"),
    path("activate/", view=ActivateAccountView.as_view(), name="activate_user"),
    path("change_password/", view=ChangePasswordView.as_view(), name="change_password"),
    path("forgot_password/", view=ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset_password/", view=ResetPasswordView.as_view(), name="reset_password"),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', view=GetAllUsersView.as_view(), name="get_all_users"),
    path('users/me', view=GetUser.as_view(), name="get_user"),
]

router = DefaultRouter()
router.register("role", CreateUserRolesView, basename="role")

urlpatterns += router.urls