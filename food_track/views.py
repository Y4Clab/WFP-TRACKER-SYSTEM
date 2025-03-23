from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import *
from food_track.serializers import *

# Create your views here.


# Base ViewSet to handle separate serializers for create and retrieve
class BaseViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return self.create_serializer_class
        return self.get_serializer_class_attr
    
    def get_object(self):
        """
        Override `get_object()` to retrieve instances using `unique_id` instead of `id`
        """
        queryset = self.get_queryset()
        filter_kwargs = {"unique_id": self.kwargs["pk"]}  # Look up by unique_id
        return get_object_or_404(queryset, **filter_kwargs)
    
    def create(self, request, *args, **kwargs):
        create_serializer = self.create_serializer_class(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        instance = create_serializer.save()  # Save using create serializer
        response_serializer = self.get_serializer_class_attr(instance)  # Use get serializer for response
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)



class VendorViewSet(BaseViewSet):
    queryset = Vendor.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = VendorCreateSerializer
    get_serializer_class_attr = VendorGetSerializer



class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = ProductCreateSerializer
    get_serializer_class_attr = ProductGetSerializer



class DriverViewSet(BaseViewSet):
    queryset = Driver.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = DriverCreateSerializer
    get_serializer_class_attr = DriverGetSerializer



class CargoViewSet(BaseViewSet):
    queryset = Cargo.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = CargoCreateSerializer
    get_serializer_class_attr = CargoGetSerializer



class CargoItemsViewSet(BaseViewSet):
    queryset = CargoItems.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = CargoItemsCreateSerializer
    get_serializer_class_attr = CargoItemsGetSerializer



class RegionViewSet(BaseViewSet):
    queryset = Region.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = RegionCreateSerializer
    get_serializer_class_attr = RegionGetSerializer



class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = ContactCreateSerializer
    get_serializer_class_attr = ContactGetSerializer



class TruckViewSet(BaseViewSet):
    queryset = Truck.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = TruckCreateSerializer
    get_serializer_class_attr = TruckGetSerializer



class TrucksForMissionViewSet(BaseViewSet):
    queryset = TrucksForMission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = TrucksForMissionCreateSerializer
    get_serializer_class_attr = TrucksForMissionGetSerializer



class MissionViewSet(BaseViewSet):
    queryset = Mission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = MissionCreateSerializer
    get_serializer_class_attr = MissionGetSerializer



class VendorMissionViewSet(BaseViewSet):
    queryset = VendorMission.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = VendorMissionCreateSerializer
    get_serializer_class_attr = VendorMissionGetSerializer



class OperationRegionViewSet(BaseViewSet):
    queryset = OperationRegion.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = OperationRegionCreateSerializer
    get_serializer_class_attr = OperationRegionGetSerializer



class DocumentsAndAgreementsViewSet(BaseViewSet):
    queryset = DocumentsAndAgreements.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    create_serializer_class = DocumentsAndAgreementsCreateSerializer
    get_serializer_class_attr = DocumentsAndAgreementsGetSerializer
