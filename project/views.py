from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, Category, ProjectImage, Tag
from .serializers import ProjectSerializer, CategorySerializer, ProjectImageSerializer, TagSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Project.objects.select_related('owner', 'category') \
            .prefetch_related('images', 'tags')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'upload_image']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_image(self, request, slug=None):
        project = self.get_object()
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = request.FILES['image']
        is_featured = request.data.get('is_featured', False)
        ProjectImage.objects.create(
            project=project,
            image=image,
            is_featured=is_featured
        )
        return Response(
            {'status': 'Image uploaded successfully'},
            status=status.HTTP_201_CREATED
        )


class ProjectImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectImageSerializer

    def get_queryset(self):
        return ProjectImage.objects.filter(project__slug=self.kwargs['project_slug'])

    def perform_create(self, serializer):
        project = Project.objects.get(slug=self.kwargs['project_slug'])
        serializer.save(project=project)
