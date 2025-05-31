from rest_framework.routers import DefaultRouter
from .views import DonationViewSet

router = DefaultRouter()
router.register(r'donations', DonationViewSet)

urlpatterns = router.urls
