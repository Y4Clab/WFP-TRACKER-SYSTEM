from rest_framework.routers import DefaultRouter
from .views import *

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
