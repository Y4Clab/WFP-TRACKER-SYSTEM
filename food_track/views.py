from rest_framework import viewsets, permissions, status, generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import *
from food_track.serializers import *

# Create your views here.


# Base ViewSet to handle separate serializers for create and retrieve
class BaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for handling separate serializers for create/update and retrieve operations.
    Uses pk as the lookup field.
    """
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        create_serializer = self.create_serializer_class(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        instance = create_serializer.save()  # Save using create serializer
        response_serializer = self.get_serializer_class_attr(instance)  # Use get serializer for response
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.create_serializer_class
        return self.get_serializer_class_attr
    
    def get_object(self):
        """
        Override `get_object()` to retrieve instances using `pk`
        """
        queryset = self.get_queryset()
        filter_kwargs = {"pk": self.kwargs["pk"]}  # Look up by pk
        return get_object_or_404(queryset, **filter_kwargs)

    # Helper method to get vendor for the authenticated user
    def get_vendor_for_user(self):
        user = self.request.user
        contact = Contact.objects.filter(user=user).first()
        if not contact:
            return None
        return contact.vendor


class VendorViewSet(BaseViewSet):
    """
    API endpoints for managing Vendor resources.
    
    Vendors are organizations providing transportation services.
    """
    queryset = Vendor.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = VendorCreateSerializer
    get_serializer_class_attr = VendorGetSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class ProductViewSet(BaseViewSet):
    """
    API endpoints for managing Product resources.
    
    Products are items that can be transported as cargo.
    """
    queryset = Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = ProductCreateSerializer
    get_serializer_class_attr = ProductGetSerializer



class DriverViewSet(BaseViewSet):
    """
    API endpoints for managing Driver resources.
    
    Drivers are individuals operating trucks for transportation.
    """
    queryset = Driver.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = DriverCreateSerializer
    get_serializer_class_attr = DriverGetSerializer



class CargoViewSet(BaseViewSet):
    """
    API endpoints for managing Cargo resources.
    
    Cargo represents collections of items to be transported.
    """
    queryset = Cargo.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = CargoCreateSerializer
    get_serializer_class_attr = CargoGetSerializer



class CargoItemsViewSet(BaseViewSet):
    """
    API endpoints for managing CargoItems resources.
    
    CargoItems are individual items within a cargo shipment.
    """
    queryset = CargoItems.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = CargoItemsCreateSerializer
    get_serializer_class_attr = CargoItemsGetSerializer



class RegionViewSet(BaseViewSet):
    """
    API endpoints for managing Region resources.
    
    Regions represent geographical areas for operations.
    """
    queryset = Region.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = RegionCreateSerializer
    get_serializer_class_attr = RegionGetSerializer



class ContactViewSet(BaseViewSet):
    """
    API endpoints for managing Contact resources.
    
    Contacts are individuals associated with vendors.
    """
    queryset = Contact.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = ContactCreateSerializer
    get_serializer_class_attr = ContactGetSerializer



class TruckViewSet(BaseViewSet):
    """
    API endpoints for managing Truck resources.
    
    Trucks are vehicles used for transportation.
    """
    queryset = Truck.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = TruckCreateSerializer
    get_serializer_class_attr = TruckGetSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class TrucksForMissionViewSet(BaseViewSet):
    """
    API endpoints for managing TrucksForMission resources.
    
    TrucksForMission represent assignments of trucks to specific missions.
    """
    queryset = TrucksForMission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = TrucksForMissionCreateSerializer
    get_serializer_class_attr = TrucksForMissionGetSerializer
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



class MissionViewSet(BaseViewSet):
    """
    API endpoints for managing Mission resources.
    
    Missions are transportation tasks from origin to destination.
    """
    queryset = Mission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = MissionCreateSerializer
    get_serializer_class_attr = ComprehensiveMissionSerializer



class VendorMissionViewSet(BaseViewSet):
    """
    API endpoints for managing VendorMission resources.
    
    VendorMissions associate vendors with specific missions.
    """
    queryset = VendorMission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = VendorMissionCreateSerializer
    get_serializer_class_attr = VendorMissionGetSerializer



class OperationRegionViewSet(BaseViewSet):
    """
    API endpoints for managing OperationRegion resources.
    
    OperationRegions define geographical areas where vendors operate.
    """
    queryset = OperationRegion.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = OperationRegionCreateSerializer
    get_serializer_class_attr = OperationRegionGetSerializer



class DocumentsAndAgreementsViewSet(BaseViewSet):
    """
    API endpoints for managing DocumentsAndAgreements resources.
    
    Documents and agreements associated with vendors.
    """
    queryset = DocumentsAndAgreements.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = DocumentsAndAgreementsCreateSerializer
    get_serializer_class_attr = DocumentsAndAgreementsGetSerializer


class VendorUserDataView(APIView):
    """
    View for a vendor user to retrieve all their associated data:
    - Contacts
    - Trucks
    - Missions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get the logged in user
        user = request.user
        
        # Find contact associated with this user
        contact = Contact.objects.filter(user=user).first()
        
        if not contact:
            return Response(
                {"error": "No vendor association found for this user"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get the vendor from the contact
        vendor = contact.vendor
        
        # Get all contacts for this vendor
        vendor_contacts = Contact.objects.filter(vendor=vendor)
        contacts_data = ContactGetSerializer(vendor_contacts, many=True).data
        
        # Get all trucks for this vendor
        vendor_trucks = Truck.objects.filter(vendor=vendor)
        trucks_data = TruckGetSerializer(vendor_trucks, many=True).data
        
        # Get missions through VendorMission
        vendor_missions = VendorMission.objects.filter(vendor=vendor)
        missions = [vm.mission for vm in vendor_missions]
        missions_data = ComprehensiveMissionSerializer(missions, many=True).data
        
        response_data = {
            "vendor": VendorGetSerializer(vendor).data,
            "contacts": contacts_data,
            "trucks": trucks_data,
            "missions": missions_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class VendorDataByIdView(APIView):
    """
    Admin view to retrieve all data for a specific vendor by ID:
    - Contacts
    - Trucks
    - Missions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, vendor_id):
        # Get the vendor by id
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response(
                {"error": f"No vendor found with ID {vendor_id}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get all contacts for this vendor
        vendor_contacts = Contact.objects.filter(vendor=vendor)
        contacts_data = ContactGetSerializer(vendor_contacts, many=True).data
        
        # Get all trucks for this vendor
        vendor_trucks = Truck.objects.filter(vendor=vendor)
        trucks_data = TruckGetSerializer(vendor_trucks, many=True).data
        
        # Get missions through VendorMission
        vendor_missions = VendorMission.objects.filter(vendor=vendor)
        missions = [vm.mission for vm in vendor_missions]
        missions_data = ComprehensiveMissionSerializer(missions, many=True).data
        
        response_data = {
            "vendor": VendorGetSerializer(vendor).data,
            "contacts": contacts_data,
            "trucks": trucks_data,
            "missions": missions_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


# Vendor-specific views
class VendorItemMixin:
    """
    Mixin to filter items by the vendor associated with the authenticated user
    """
    permission_classes = [IsAuthenticated]
    
    def get_vendor(self):
        # Get vendor associated with the authenticated user through contact
        contact = Contact.objects.filter(user=self.request.user).first()
        if not contact:
            return None
        return contact.vendor
    
    def get_queryset(self):
        vendor = self.get_vendor()
        if not vendor:
            return self.model.objects.none()
        return self.model.objects.filter(vendor=vendor)


# Vendor Trucks Views
class VendorTruckListCreateView(VendorItemMixin, generics.ListCreateAPIView):
    """
    View for listing and creating trucks for a vendor.
    
    Only shows trucks belonging to the vendor associated with the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    model = Truck
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TruckCreateSerializer
        return TruckGetSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        vendor = self.get_vendor()
        if not vendor:
            return Response({"error": "User is not associated with any vendor"}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(vendor=vendor)


class VendorTruckDetailView(VendorItemMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting a vendor's truck.
    
    Only works with trucks belonging to the vendor associated with the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    model = Truck
    lookup_field = 'pk'
    lookup_url_kwarg = 'truck_id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TruckCreateSerializer
        return TruckGetSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Vendor Contacts Views
class VendorContactListCreateView(VendorItemMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    """View for listing and creating contacts for a vendor"""
    model = Contact
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ContactCreateSerializer
        return ContactGetSerializer
    
    def perform_create(self, serializer):
        vendor = self.get_vendor()
        if not vendor:
            raise ValidationError("User is not associated with any vendor")
        serializer.save(vendor=vendor)


class VendorContactDetailView(VendorItemMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    """View for retrieving, updating and deleting a vendor's contact"""
    model = Contact
    lookup_field = 'pk'
    lookup_url_kwarg = 'contact_id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ContactCreateSerializer
        return ContactGetSerializer


# Vendor Missions Views
class VendorMissionListView(VendorItemMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    """View for listing missions for a vendor"""
    model = VendorMission
    serializer_class = ComprehensiveMissionSerializer
    
    def get_queryset(self):
        vendor = self.get_vendor()
        if not vendor:
            return Mission.objects.none()
        
        # Get missions through VendorMission
        vendor_missions = VendorMission.objects.filter(vendor=vendor)
        mission_ids = [vm.mission.id for vm in vendor_missions]
        return Mission.objects.filter(id__in=mission_ids)


class VendorMissionDetailView(generics.RetrieveAPIView):
    """View for retrieving a specific mission for a vendor"""
    permission_classes = [IsAuthenticated]
    serializer_class = ComprehensiveMissionSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'mission_id'
    
    def get_queryset(self):
        # Get vendor associated with the authenticated user
        contact = Contact.objects.filter(user=self.request.user).first()
        if not contact:
            return Mission.objects.none()
        
        vendor = contact.vendor
        
        # Get missions through VendorMission
        vendor_missions = VendorMission.objects.filter(vendor=vendor)
        mission_ids = [vm.mission.id for vm in vendor_missions]
        return Mission.objects.filter(id__in=mission_ids)


# Vendor TrucksForMission Views
class VendorTrucksForMissionListCreateView(VendorItemMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    """View for listing and creating truck-mission assignments for a vendor"""
    model = TrucksForMission
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrucksForMissionCreateSerializer
        return TrucksForMissionGetSerializer
    
    def perform_create(self, serializer):
        vendor = self.get_vendor()
        if not vendor:
            return Response({"error": "User is not associated with any vendor"}, status=status.HTTP_404_NOT_FOUND)
            
        # Ensure the truck belongs to the vendor
        truck = serializer.validated_data.get('truck')
        if truck.vendor != vendor:
            return Response({"error": "You can only assign trucks that belong to your vendor"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if the vendor is assigned to this mission
        mission = serializer.validated_data.get('mission')
        vendor_mission = VendorMission.objects.filter(vendor=vendor, mission=mission).exists()
        if not vendor_mission:
            return Response({"error": "This mission is not assigned to your vendor"}, status=status.HTTP_400_BAD_REQUEST)
            
        # If cargo_items_ids are provided, validate they belong to the mission
        cargo_items_ids = serializer.validated_data.get('cargo_items_ids', [])
        if cargo_items_ids:
            # Get cargo for this mission
            mission_cargo = Cargo.objects.filter(mission=mission).first()
            if not mission_cargo:
                return Response(
                    {"error": "No cargo found for this mission"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            # Verify cargo items belong to the mission
            valid_cargo_items = CargoItems.objects.filter(
                unique_id__in=cargo_items_ids,
                cargo=mission_cargo
            )
            
            if len(valid_cargo_items) != len(cargo_items_ids):
                return Response(
                    {"error": "Some cargo items don't exist or don't belong to this mission"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer.save(vendor=vendor)


class VendorTrucksForMissionDetailView(VendorItemMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    """View for retrieving, updating and deleting a vendor's truck-mission assignment"""
    model = TrucksForMission
    lookup_field = 'pk'
    lookup_url_kwarg = 'assignment_id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TrucksForMissionCreateSerializer
        return TrucksForMissionGetSerializer


class VendorTrucksForMissionCargoView(generics.UpdateAPIView):
    """View for assigning cargo items to a truck for a mission"""
    permission_classes = [IsAuthenticated]
    serializer_class = TrucksForMissionGetSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'assignment_id'
    
    def get_queryset(self):
        # Get vendor associated with the authenticated user
        contact = Contact.objects.filter(user=self.request.user).first()
        if not contact:
            return TrucksForMission.objects.none()
        
        return TrucksForMission.objects.filter(vendor=contact.vendor)
    
    def update(self, request, *args, **kwargs):
        trucks_for_mission = self.get_object()
        
        # Get cargo items data from request
        cargo_items = request.data.get('cargo_items', [])
        if not cargo_items:
            return Response(
                {"error": "No cargo items provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the mission is assigned to this vendor
        vendor = trucks_for_mission.vendor
        mission = trucks_for_mission.mission
        vendor_mission = VendorMission.objects.filter(vendor=vendor, mission=mission).exists()
        if not vendor_mission:
            return Response(
                {"error": "This mission is not assigned to your vendor"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Verify cargo items belong to the mission
        mission_cargo = Cargo.objects.filter(mission=trucks_for_mission.mission).first()
        if not mission_cargo:
            return Response(
                {"error": "No cargo found for this mission"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Process each cargo item
        errors = []
        cargo_item_ids = [item.get('cargo_item_id') for item in cargo_items if item.get('cargo_item_id')]
        
        # Remove any cargo items no longer in the list
        TruckCargoItem.objects.filter(truck_mission=trucks_for_mission).exclude(
            cargo_item__unique_id__in=cargo_item_ids
        ).delete()
        
        # Update or create cargo items
        for item_data in cargo_items:
            if not item_data.get('cargo_item_id') or not item_data.get('quantity'):
                errors.append(f"Each cargo item must have cargo_item_id and quantity")
                continue
                
            try:
                cargo_item = CargoItems.objects.get(
                    unique_id=item_data['cargo_item_id'],
                    cargo=mission_cargo
                )
            except CargoItems.DoesNotExist:
                errors.append(f"Cargo item with ID {item_data['cargo_item_id']} not found or doesn't belong to this mission")
                continue
                
            quantity = int(item_data['quantity'])
            
            # Check if quantity is valid
            other_allocations = TruckCargoItem.objects.filter(
                cargo_item=cargo_item
            ).exclude(truck_mission=trucks_for_mission).aggregate(
                models.Sum('transferring_quantity')
            )['transferring_quantity__sum'] or 0
            
            available = cargo_item.quantity - other_allocations
            if quantity > available:
                errors.append(f"Cargo item {cargo_item.product.name} only has {available} units available")
                continue
                
            # Update or create the truck cargo item
            TruckCargoItem.objects.update_or_create(
                truck_mission=trucks_for_mission,
                cargo_item=cargo_item,
                defaults={'transferring_quantity': quantity}
            )
        
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            
        # Return updated truck-mission data
        serializer = self.get_serializer(trucks_for_mission)
        return Response(serializer.data)


class VendorTruckCargoListView(generics.ListAPIView):
    """View for listing all truck cargo assignments for a vendor"""
    permission_classes = [IsAuthenticated]
    serializer_class = TruckCargoAssignmentSerializer
    
    def get_queryset(self):
        # Get vendor associated with the authenticated user
        contact = Contact.objects.filter(user=self.request.user).first()
        if not contact:
            return TrucksForMission.objects.none()
        
        # Get all truck-mission assignments for the vendor
        return TrucksForMission.objects.filter(vendor=contact.vendor)
