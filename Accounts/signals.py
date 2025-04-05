from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from Accounts.models import UsersWithRoles, UserProfile
from food_track.models import Vendor, Contact
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UsersWithRoles)
def create_vendor_contact(sender, instance, created, **kwargs):
    """
    Signal to create a Vendor and Contact record when a user with the vendor role is created
    """
    try:
        if created and instance.user_with_role_role.role_name == "vendor":
            user = instance.user_with_role_user
            
            # Get user profile to access profile_organization
            user_profile = UserProfile.objects.filter(profile_user=user).first()
                
            # Try to find vendor by matching reg_no with profile_organization
            vendor = Vendor.objects.filter(reg_no=user_profile.profile_organization).first()
            
            if not vendor:
                logger.error(f"No vendor found with reg_no matching")
                # Instead of raising exception, we'll log the error and return
                return
            
            # Create contact
            try:
                Contact.objects.create(
                    user=user,
                    vendor=vendor  # Use vendor object, not vendor_id
                )
                logger.info(f"Contact created successfully for user {user.email} with vendor {vendor.name}")
            except Exception as contact_error:
                logger.error(f"Failed to create contact: {str(contact_error)}")
    except Exception as e:
        logger.error(f"Error in create_vendor_contact signal: {str(e)}")