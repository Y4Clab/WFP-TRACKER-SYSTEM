from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path

router = DefaultRouter()
router.register('vendors', VendorViewSet, basename="vendors")
router.register('products', ProductViewSet, basename="products")
router.register('drivers', DriverViewSet, basename="drivers")
router.register('cargo', CargoViewSet, basename="cargo")
router.register('cargo-items', CargoItemsViewSet, basename="cargo items")
router.register('regions', RegionViewSet, basename="regions")
router.register('contacts', ContactViewSet, basename="contacts")
router.register('trucks', TruckViewSet, basename="trucks")
router.register('trucks-for-mission', TrucksForMissionViewSet, basename="mission trucks")
router.register('missions', MissionViewSet, basename="missions")
router.register('vendor-missions', VendorMissionViewSet, basename="vendor missions")
router.register('operation-regions', OperationRegionViewSet, basename="vendor operating regions")
router.register('documents', DocumentsAndAgreementsViewSet, basename="vendor documents")

urlpatterns = router.urls

# Add custom API endpoint for vendor user data
urlpatterns += [
    # General vendor data views
    path('vendor-user-data/', VendorUserDataView.as_view(), name='vendor-user-data'),
    path('vendor-data/<uuid:vendor_id>/', VendorDataByIdView.as_view(), name='vendor-data-by-id'),
    
    # Vendor-specific resource views
    # Trucks
    path('vendor/trucks/', VendorTruckListCreateView.as_view(), name='vendor-trucks-list-create'),
    path('vendor/trucks/<uuid:truck_id>/', VendorTruckDetailView.as_view(), name='vendor-truck-detail'),
    
    # Contacts
    path('vendor/contacts/', VendorContactListCreateView.as_view(), name='vendor-contacts-list-create'),
    path('vendor/contacts/<uuid:contact_id>/', VendorContactDetailView.as_view(), name='vendor-contact-detail'),
    
    # Missions
    path('vendor/missions/', VendorMissionListView.as_view(), name='vendor-missions-list'),
    path('vendor/missions/<uuid:mission_id>/', VendorMissionDetailView.as_view(), name='vendor-mission-detail'),
    
    # TrucksForMission with cargo items
    path('vendor/trucks-for-mission/', VendorTrucksForMissionListCreateView.as_view(), name='vendor-trucks-for-mission-list-create'),
    path('vendor/trucks-for-mission/<uuid:assignment_id>/', VendorTrucksForMissionDetailView.as_view(), name='vendor-trucks-for-mission-detail'),
    path('vendor/trucks-for-mission/<uuid:assignment_id>/cargo/', VendorTrucksForMissionCargoView.as_view(), name='vendor-trucks-for-mission-cargo'),
    path('vendor/truck-cargo/', VendorTruckCargoListView.as_view(), name='vendor-truck-cargo-list'),
]
