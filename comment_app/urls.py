from django.urls import path
from .views import (
    ProjectListCreateAPIView, CommentListCreateAPIView, 
    ReportProjectCreateAPIView, ReportCommentCreateAPIView
)

urlpatterns = [
    path('projects/', ProjectListCreateAPIView.as_view(), name='projects-list-create'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comments-list-create'),
    path('reports/project/', ReportProjectCreateAPIView.as_view(), name='report-project-create'),
    path('reports/comment/', ReportCommentCreateAPIView.as_view(), name='report-comment-create'),
]
