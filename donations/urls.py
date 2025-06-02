from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationViewSet, ProjectTotalDonationsView

router = DefaultRouter()
router.register(r'', DonationViewSet, basename='donation')

urlpatterns = [
    path('', include(router.urls)),
    path('total/<int:pk>/', ProjectTotalDonationsView.as_view(), name='project-total-donations'),
]
