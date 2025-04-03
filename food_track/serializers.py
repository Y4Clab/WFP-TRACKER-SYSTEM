from rest_framework import serializers
from .models import *

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'reg_no', 'vendor_type', 'fleet_size', 'description', 'status']

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

    class Meta:
        model = CargoItems
        fields = '__all__'



class RegionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_name']

class RegionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'



class ContactCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address', 'city', 'country', 'vendor']

class ContactGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Contact
        fields = '__all__'



class TruckCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = ['vehicle_name', 'vendor', 'status']

class TruckGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Truck
        fields = '__all__'



class TrucksForMissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrucksForMission
        fields = ['mission', 'truck']

class TrucksForMissionGetSerializer(serializers.ModelSerializer):
    mission = serializers.StringRelatedField()
    truck = TruckGetSerializer()

    class Meta:
        model = TrucksForMission
        fields = '__all__'



class MissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['title', 'type', 'number_of_beneficiaries', 'description', 'dept_location', 'destination_location', 'start_date', 'end_date', 'status']

class MissionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = '__all__'



class VendorMissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorMission
        fields = ['vendor', 'mission']

class VendorMissionGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()
    mission = MissionGetSerializer()
    # driver = DriverGetSerializer()

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
