from rest_framework import serializers
from django.contrib.auth import get_user_model

from Accounts.models import UserProfile
from .models import *
import os

User = get_user_model()

# Base serializers without complex relationships
class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'vendor_type', 'fleet_size', 'status']

class VendorGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'quantity']

class ProductGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_name']

class RegionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['title', 'type', 'number_of_beneficiaries', 'description', 'dept_location', 'destination_location', 'start_date', 'end_date', 'status']

class MissionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'

# Dependent serializers
class DriverCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'vendor']

class DriverGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Driver
        fields = '__all__'

class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['mission', 'total_products_quantity']

class CargoGetSerializer(serializers.ModelSerializer):
    mission = serializers.StringRelatedField()

    class Meta:
        model = Cargo
        fields = '__all__'

class CargoItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CargoItems
        fields = ['cargo', 'product', 'quantity']

class CargoItemsGetSerializer(serializers.ModelSerializer):
    cargo = CargoGetSerializer()
    product = ProductGetSerializer()
    remaining_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = CargoItems
        fields = '__all__'

class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['user', 'vendor']

class ContactGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Contact
        fields = '__all__'

class TruckCreateSerializer(serializers.ModelSerializer):
    unique_id = serializers.UUIDField(read_only=True)
    vendor = serializers.UUIDField(read_only=True)
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Truck
        fields = ['id', 'unique_id', 'plate_number', 'year', 'model', 'vehicle_name', 'capacity', 'vendor', 'status']

class TruckGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Truck
        fields = '__all__'

class VendorMissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMission
        fields = ['vendor', 'mission']

class VendorMissionGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()
    mission = MissionGetSerializer()

    class Meta:
        model = VendorMission
        fields = '__all__'

class OperationRegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationRegion
        fields = ['region', 'vendor']

class OperationRegionGetSerializer(serializers.ModelSerializer):
    region = RegionGetSerializer()
    vendor = VendorGetSerializer()

    class Meta:
        model = OperationRegion
        fields = '__all__'

# Truck Cargo Item serializers
class TruckCargoItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckCargoItem
        fields = ['cargo_item', 'transferring_quantity']
        
    def validate(self, data):
        # Ensure cargo item belongs to the mission
        cargo_item = data.get('cargo_item')
        truck_mission = self.context.get('truck_mission')
        transferring_quantity = data.get('transferring_quantity')
        
        if not truck_mission:
            raise serializers.ValidationError("Truck mission context is required")
            
        # Verify cargo item belongs to the mission
        mission_cargo = Cargo.objects.filter(mission=truck_mission.mission).first()
        if not mission_cargo or cargo_item.cargo.id != mission_cargo.id:
            raise serializers.ValidationError({
                "cargo_item": "This cargo item doesn't belong to the mission"
            })
            
        # Check available quantity
        other_allocations = TruckCargoItem.objects.filter(
            cargo_item=cargo_item
        ).exclude(truck_mission=truck_mission).aggregate(
            models.Sum('transferring_quantity')
        )['transferring_quantity__sum'] or 0
        
        available = cargo_item.quantity - other_allocations
        if transferring_quantity > available:
            raise serializers.ValidationError({
                "transferring_quantity": f"Exceeds available quantity. Only {available} units available."
            })
            
        return data

class TruckCargoItemGetSerializer(serializers.ModelSerializer):
    cargo_item = CargoItemsGetSerializer()
    
    class Meta:
        model = TruckCargoItem
        fields = ['unique_id', 'cargo_item', 'transferring_quantity']

# More complex serializers that depend on multiple other serializers
class TrucksForMissionCreateSerializer(serializers.ModelSerializer):
    unique_id = serializers.UUIDField(read_only=True)
    cargo_items = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        write_only=True,
        help_text="List of cargo items with quantities to assign to this truck"
    )
    
    class Meta:
        model = TrucksForMission
        fields = ['id', 'unique_id', 'mission', 'truck', 'cargo_items']
    
    def validate(self, data):
        """
        Validate that cargo items belong to the mission and quantities are available
        Also check that total items don't exceed truck capacity
        """
        mission = data.get('mission')
        truck = data.get('truck')
        cargo_items = data.get('cargo_items', [])
        
        # Calculate total items to be transported
        total_items = 0
        for item in cargo_items:
            if item.get('quantity'):
                total_items += int(item['quantity'])
        
        # Check if truck has sufficient capacity
        if truck and total_items > truck.capacity:
            raise serializers.ValidationError({
                "cargo_items": f"Total cargo quantity ({total_items}) exceeds truck capacity ({truck.capacity})"
            })
        
        if mission and cargo_items:
            # Verify mission has associated cargo
            mission_cargo = Cargo.objects.filter(mission=mission).first()
            if not mission_cargo:
                raise serializers.ValidationError({
                    "cargo_items": "No cargo found for the specified mission"
                })
            
            # Validate each cargo item
            for item in cargo_items:
                if not item.get('cargo_item_id') or not item.get('quantity'):
                    raise serializers.ValidationError({
                        "cargo_items": "Each cargo item must have cargo_item_id and quantity"
                    })
                
                try:
                    cargo_item = CargoItems.objects.get(
                        unique_id=item['cargo_item_id'],
                        cargo=mission_cargo
                    )
                except CargoItems.DoesNotExist:
                    raise serializers.ValidationError({
                        "cargo_items": f"Cargo item with ID {item['cargo_item_id']} not found or doesn't belong to this mission"
                    })
                
                quantity = int(item['quantity'])
                
                # Check if quantity is valid
                other_allocations = TruckCargoItem.objects.filter(
                    cargo_item=cargo_item
                ).aggregate(
                    models.Sum('transferring_quantity')
                )['transferring_quantity__sum'] or 0
                
                available = cargo_item.quantity - other_allocations
                if quantity > available:
                    raise serializers.ValidationError({
                        "cargo_items": f"Cargo item {cargo_item.product.name} only has {available} units available"
                    })
                
        return data
        
    def create(self, validated_data):
        cargo_items_data = validated_data.pop('cargo_items', [])
        trucks_for_mission = super().create(validated_data)
        
        # Create TruckCargoItem entries for each cargo item
        if cargo_items_data:
            for item in cargo_items_data:
                cargo_item = CargoItems.objects.get(unique_id=item['cargo_item_id'])
                TruckCargoItem.objects.create(
                    truck_mission=trucks_for_mission,
                    cargo_item=cargo_item,
                    transferring_quantity=item['quantity']
                )
        
        return trucks_for_mission

class TrucksForMissionGetSerializer(serializers.ModelSerializer):
    mission = MissionGetSerializer()
    truck = TruckGetSerializer()
    vendor = VendorGetSerializer()
    truck_cargo_items = TruckCargoItemGetSerializer(many=True, read_only=True)

    class Meta:
        model = TrucksForMission
        fields = '__all__'
        
class TruckCargoAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for detailed truck cargo assignment information"""
    mission = MissionGetSerializer()
    truck = TruckGetSerializer()
    cargo_items = serializers.SerializerMethodField()
    capacity_utilization = serializers.SerializerMethodField()
    
    class Meta:
        model = TrucksForMission
        fields = ['unique_id', 'mission', 'truck', 'cargo_items', 'capacity_utilization']
    
    def get_cargo_items(self, obj):
        truck_cargo_items = obj.truck_cargo_items.all()
        items_data = []
        
        for truck_item in truck_cargo_items:
            cargo_item = truck_item.cargo_item
            items_data.append({
                'id': cargo_item.unique_id,
                'product_name': cargo_item.product.name,
                'total_quantity': cargo_item.quantity,
                'transferring_quantity': truck_item.transferring_quantity,
                'cargo_id': cargo_item.cargo.unique_id
            })
            
        return items_data
    
    def get_capacity_utilization(self, obj):
        """Calculate how much of the truck's capacity is being utilized"""
        truck = obj.truck
        total_items = obj.truck_cargo_items.aggregate(
            total=models.Sum('transferring_quantity')
        )['total'] or 0
        
        capacity = truck.capacity
        utilization_percentage = (total_items / capacity * 100) if capacity > 0 else 0
        
        return {
            'total_capacity': capacity,
            'items_assigned': total_items,
            'remaining_capacity': max(0, capacity - total_items),
            'utilization_percentage': round(utilization_percentage, 2)
        }

class DocumentsAndAgreementsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsAndAgreements
        fields = ['vendor', 'document']

        def validate_document(self, value):
            allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png']
            max_size = 10 * 1024 * 1024  # 10MB

            ext = os.path.splitext(value.name)[1].lower()
            if ext not in allowed_extensions:
                raise serializers.ValidationError(f'Invalid file format. Allowed formats: {", ".join(allowed_extensions)}')

            if value.size > max_size:
                raise serializers.ValidationError('File size exceeds the 10MB limit.')

            return value

class DocumentsAndAgreementsGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = DocumentsAndAgreements
        fields = '__all__'

class ComprehensiveMissionSerializer(serializers.ModelSerializer):
    """
    Comprehensive mission serializer that includes all related data:
    - Cargo items
    - Assigned trucks
    - Assigned vendors
    """
    cargo_items = serializers.SerializerMethodField()
    assigned_trucks = serializers.SerializerMethodField()
    assigned_vendors = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = ['unique_id', 'id', 'title', 'type', 'number_of_beneficiaries', 
                 'description', 'dept_location', 'destination_location', 
                 'start_date', 'end_date', 'status','cargo_items', 'assigned_trucks', 
                 'assigned_vendors']
    
    def get_cargo_items(self, mission):
        # Get the cargo associated with this mission
        cargo = Cargo.objects.filter(mission=mission).first()
        if not cargo:
            return []
        
        # Get all cargo items for this cargo
        cargo_items = CargoItems.objects.filter(cargo=cargo)
        return CargoItemsGetSerializer(cargo_items, many=True).data
    
    def get_assigned_trucks(self, mission):
        # Get all truck assignments for this mission
        truck_assignments = TrucksForMission.objects.filter(mission=mission)
        
        # Format the data to include both truck details and cargo assignments
        result = []
        for assignment in truck_assignments:
            # Get truck details
            truck_data = TruckGetSerializer(assignment.truck).data
            
            # Get cargo items assigned to this truck for this mission
            truck_cargo_items = TruckCargoItem.objects.filter(truck_mission=assignment)
            cargo_assignments = []
            
            # Calculate total quantity assigned to this truck
            total_quantity = 0
            
            for truck_cargo in truck_cargo_items:
                cargo_item_data = CargoItemsGetSerializer(truck_cargo.cargo_item).data
                quantity = truck_cargo.transferring_quantity
                total_quantity += quantity
                
                cargo_assignments.append({
                    'cargo_item': cargo_item_data,
                    'quantity': quantity
                })
            
            # Calculate capacity utilization
            capacity = assignment.truck.capacity
            utilization_percentage = (total_quantity / capacity * 100) if capacity > 0 else 0
            
            # Create a complete truck assignment object
            assignment_data = {
                'assignment_id': assignment.unique_id,
                'truck': truck_data,
                'assigned_cargo': cargo_assignments,
                'capacity_data': {
                    'total_capacity': capacity,
                    'items_assigned': total_quantity,
                    'remaining_capacity': max(0, capacity - total_quantity),
                    'utilization_percentage': round(utilization_percentage, 2)
                }
            }
            
            result.append(assignment_data)
            
        return result
    
    def get_assigned_vendors(self, mission):
        # Get all vendor assignments for this mission
        vendor_missions = VendorMission.objects.filter(mission=mission)
        result = []
        
        for vm in vendor_missions:
            vendor_data = VendorGetSerializer(vm.vendor).data
            
            # Get contacts for this vendor
            contacts = Contact.objects.filter(vendor=vm.vendor)
            contact_data = []
            
            for contact in contacts:
                user_data = User.objects.filter(id=contact.user.id, is_active=True).first()
                if user_data:
                    user_profile = UserProfile.objects.filter(profile_user=user_data, profile_is_active=True).first()
                    if user_profile:
                        # Convert UserProfile to a serializable dictionary
                        contact_info = {
                            'id': user_profile.id,
                            'unique_id': str(user_profile.profile_unique_id),
                            'name': f"{user_data.first_name} {user_data.last_name}",
                            'email': user_data.email,
                            'phone': user_profile.profile_phone,
                            'organization': user_profile.profile_organization
                        }
                        contact_data.append(contact_info)
            
            # Create a complete vendor assignment object
            assignment_data = {
                'assignment_id': vm.unique_id,
                'vendor': vendor_data,
                'contacts': contact_data,
                # 'assignment_date': vm.created_at
            }
            
            result.append(assignment_data)
            
        return result
