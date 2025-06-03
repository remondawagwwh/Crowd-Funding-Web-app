from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, CategoryViewSet, TagViewSet, ProjectImageViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('tags', TagViewSet, basename='tag')
router.register('projects', ProjectViewSet, basename='project')

project_router = DefaultRouter()
project_router.register('images', ProjectImageViewSet, basename='project-image')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<slug:project_slug>/', include(project_router.urls)),
]