from django.db import models
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import os

# Create your models here.

class Vendor(models.Model):
    VENDOR_TYPES = [
        ('food_supplier', 'Food Supplier'),
        ('logistic_provider', 'Logistic Provider'),
        ('Mixed', 'Both')
    ]

    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
    ]

    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255, unique=True, blank=False, null=False)
    vendor_type = models.CharField(max_length=50, choices=VENDOR_TYPES)
    fleet_size = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name

class Product(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Driver(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Cargo(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey("Mission", on_delete=models.CASCADE)
    total_products_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Cargo-{self.mission.title}'

class CargoItems(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Region(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    region_name = models.CharField(max_length=255, unique=True)

class Contact(models.Model):
    contact_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Truck(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    ]

    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    vehicle_name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return self.vehicle_name

class TrucksForMission(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey("Mission", on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)

class Mission(models.Model):
    MISSION_TYPES = [
        ('specialized_delivery', 'Specialized Delivery'),
        ('regular_scheduled', 'Regular Scheduled'),
        ('emergency', 'Emergency')
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('active', 'Active'),
    ]

    mission_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=MISSION_TYPES)
    number_of_beneficiaries = models.PositiveIntegerField()
    description = models.TextField()
    dept_location = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title

class VendorMission(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

class OperationRegion(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


def validate_document_file(value):
    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError('File size exceeds the 10MB limit.')
    

class DocumentsAndAgreements(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png']),validate_document_file])

