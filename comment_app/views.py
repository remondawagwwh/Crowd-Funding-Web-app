from rest_framework import generics, permissions
from .models import Project, Comment, ReportProject, ReportComment
from .serializers import (
    ProjectSerializer, CommentSerializer, 
    ReportProjectSerializer, ReportCommentSerializer
)



class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReportProjectCreateAPIView(generics.CreateAPIView):
    queryset = ReportProject.objects.all()
    serializer_class = ReportProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReportCommentCreateAPIView(generics.CreateAPIView):
    queryset = ReportComment.objects.all()
    serializer_class = ReportCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
