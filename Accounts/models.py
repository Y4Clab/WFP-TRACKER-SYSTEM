from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime,timedelta

class ProfileTypeChoice(models.TextChoices):
    SUPER_ADMIN = "Super Admin"
    ORGANIZATION_ADMIN = "Organization_Admin"

# Create your models here.
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    profile_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, db_index=True)
    profile_phone = models.CharField(default='', max_length=9000, blank=True, null=True)
    profile_user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, db_index=True)
    profile_organization = models.CharField(default='', max_length=9000)
    profile_type = models.CharField(default='Organization_Admin', choices = ProfileTypeChoice.choices, max_length=9000)
    profile_is_active = models.BooleanField(default=True, db_index=True)
    profile_created_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profiles'
        ordering = ['-id']
        verbose_name_plural = "USER PROFILES"

    def __str__(self):
        return f"{self.profile_organization} : {self.profile_user.first_name} {self.profile_user.last_name}"

class AccountActivationRequestUsers(models.Model):
    primary_key = models.AutoField(primary_key=True)
    account_activation_user = models.ForeignKey(User, related_name='password_profile', on_delete=models.CASCADE)
    account_activation_token = models.CharField(max_length=300, editable=False, default=None)
    account_activation_is_used = models.BooleanField(default=False)
    account_activation_is_active = models.BooleanField(default=True)
    # account_activation_expiration_time = models.DateTimeField()
    
    class Meta:
        db_table = 'account_activation_request'
        ordering = ['-primary_key']
        verbose_name_plural = "ACCOUNT ACTIVATION REQUESTS"

    def __str__(self):
        return "{} - {}".format(self.account_activation_user, self.account_activation_token)


class ForgotPasswordRequestUser(models.Model):
    primary_key = models.AutoField(primary_key=True)
    request_user = models.ForeignKey(User, related_name='request_profile', on_delete=models.CASCADE)
    request_token = models.CharField(max_length=300, editable=False, default=None)
    request_is_used = models.BooleanField(default=False)
    request_is_active = models.BooleanField(default=True)
    request_created_date = models.DateTimeField(auto_now_add=True)
    request_expiration_time = models.DateTimeField()
    class Meta:
        db_table = 'users_forgot_password_request'
        ordering = ['-primary_key']
        verbose_name_plural = "FORGOT PASSWORD REQUESTS"

    def __str__(self):
        return f"{self.request_user} - {self.request_token}"

    def has_expired(self):
        # Calculate the time difference between now and request_created_date
        current_time = datetime.now()
        time_difference = current_time - self.request_created_date

        # Check if the time difference is greater than 24 hours (86400 seconds)
        if time_difference.total_seconds() > 86400:
            return True
        
        return False
    

class UserRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    role_name = models.CharField(default='', max_length=9000)
    role_description = models.CharField(default='', max_length=9000)
    role_is_active = models.BooleanField(default=True)
    role_createddate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "USER ROLES"

    def __str__(self):
        return "{}".format(self.role_name)



class UsersWithRoles(models.Model):
    primary_key = models.AutoField(primary_key=True)
    user_with_role_unique_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    user_with_role_role = models.ForeignKey(UserRoles, related_name='user_role_name', on_delete=models.CASCADE)
    user_with_role_user = models.ForeignKey(User, related_name='role_user', on_delete=models.CASCADE)
    user_with_role_createddate = models.DateField(auto_now_add=True)


    class Meta:
        db_table = 'user_with_roles'
        ordering = ['-primary_key']
        verbose_name_plural = "USERS WITH ROLES"