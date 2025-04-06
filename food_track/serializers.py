from rest_framework import serializers
from .models import *
import os

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
        fields = ['id', 'unique_id', 'vehicle_name', 'vendor', 'status']

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
        """
        mission = data.get('mission')
        cargo_items = data.get('cargo_items', [])
        
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
    
    class Meta:
        model = TrucksForMission
        fields = ['unique_id', 'mission', 'truck', 'cargo_items']
    
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
