from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point, LineString
import os
import datetime
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

    def save(self, *args, **kwargs):
        # Auto-generate reg_no if not provided
        if not self.reg_no:
            # Get current date and time
            now = datetime.datetime.now()
            # Format: VEN-YYYYMMDD-RandomUUID first 8 chars
            uuid_part = str(uuid.uuid4()).split('-')[0]
            date_part = now.strftime('%Y%m%d')
            self.reg_no = f"VEN-{date_part}-{uuid_part}"
        super().save(*args, **kwargs)

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
    
    @property
    def remaining_quantity(self):
        """Calculate remaining quantity after allocations to trucks"""
        assigned = TruckCargoItem.objects.filter(cargo_item=self).aggregate(
            models.Sum('transferring_quantity')
        )['transferring_quantity__sum'] or 0
        return self.quantity - assigned
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Region(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    region_name = models.CharField(max_length=255, unique=True)

class Contact(models.Model):
    contact_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class Truck(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
    ]

    plate_number = models.CharField(max_length=255, unique=True, blank=True, null=True)
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    vehicle_name = models.CharField(max_length=255)
    year = models.IntegerField()
    model = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return self.vehicle_name

class TrucksForMission(models.Model):
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey("Mission", on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.truck.vehicle_name} for {self.mission.title}"

class TruckCargoItem(models.Model):
    """
    Intermediate model to track the quantity of each cargo item assigned to a truck
    """
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    truck_mission = models.ForeignKey(TrucksForMission, on_delete=models.CASCADE, related_name="truck_cargo_items")
    cargo_item = models.ForeignKey(CargoItems, on_delete=models.CASCADE, related_name="truck_allocations")
    transferring_quantity = models.PositiveIntegerField(
        help_text="Quantity of this cargo item being transferred by this truck"
    )
    
    class Meta:
        unique_together = ('truck_mission', 'cargo_item')
        
    def clean(self):
        """Validate that transferring quantity doesn't exceed available quantity"""
        if self.cargo_item and self.transferring_quantity:
            # Get total allocated to other trucks
            other_allocations = TruckCargoItem.objects.filter(
                cargo_item=self.cargo_item
            ).exclude(id=self.id).aggregate(
                models.Sum('transferring_quantity')
            )['transferring_quantity__sum'] or 0
            
            available = self.cargo_item.quantity - other_allocations
            if self.transferring_quantity > available:
                raise ValidationError({
                    'transferring_quantity': f'Exceeds available quantity. Only {available} units available.'
                })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.truck_mission} - {self.cargo_item.product.name} ({self.transferring_quantity})"

class Mission(models.Model):
    MISSION_TYPES = [
        ('specialized', 'Specialized Delivery'),
        ('regular', 'Regular Scheduled'),
        ('emergency', 'Emergency')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Active', 'Active'),
    ]

    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=MISSION_TYPES)
    # extra = models.CharField(max_length=255, null=True, blank=True)
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

class Route(models.Model):
    TRAVEL_MODES = [
        ('driving', 'Driving'),
        ('walking', 'Walking'),
        ('bicycling', 'Bicycling'),
        ('transit', 'Transit'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('active', 'Active'),
    ]
    
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='routes')
    
    # Text representation of locations (human-readable addresses)
    origin = models.CharField(max_length=255, help_text="Text representation of the origin address")
    destination = models.CharField(max_length=255, help_text="Text representation of the destination address")
    
    # Spatial data fields
    origin_point = gis_models.PointField(null=True, help_text="Geographic coordinates of the origin")
    destination_point = gis_models.PointField(null=True, help_text="Geographic coordinates of the destination")
    path = gis_models.LineStringField(null=True, blank=True, help_text="Full path geometry of the route")
    
    # Waypoints as GeoJSON-compatible field
    waypoints = gis_models.MultiPointField(null=True, blank=True, help_text="Collection of waypoint locations")
    
    # Route preferences
    travel_mode = models.CharField(max_length=20, choices=TRAVEL_MODES, default='driving')
    avoid_tolls = models.BooleanField(default=False)
    avoid_highways = models.BooleanField(default=False)
    optimized_waypoints = models.BooleanField(default=True)
    
    # Additional route data from API
    route_data = models.JSONField(blank=True, null=True, help_text="Additional data from Google Maps API")
    distance_meters = models.PositiveIntegerField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(blank=True, null=True)
    
    # Status and timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Route for {self.mission.title}: {self.origin} to {self.destination}"
    
    @property
    def origin_latitude(self):
        """Return the latitude of the origin point"""
        if self.origin_point:
            return self.origin_point.y
        return None
    
    @property
    def origin_longitude(self):
        """Return the longitude of the origin point"""
        if self.origin_point:
            return self.origin_point.x
        return None
    
    @property
    def destination_latitude(self):
        """Return the latitude of the destination point"""
        if self.destination_point:
            return self.destination_point.y
        return None
    
    @property
    def destination_longitude(self):
        """Return the longitude of the destination point"""
        if self.destination_point:
            return self.destination_point.x
        return None

