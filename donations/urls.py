from django.urls import path
from .views import CreateDonationView, ProjectTotalDonationsView

urlpatterns = [
    path('create/', CreateDonationView.as_view(), name='create-donation'),
    path('total/<int:pk>/', ProjectTotalDonationsView.as_view(), name='project-total-donations'),
]