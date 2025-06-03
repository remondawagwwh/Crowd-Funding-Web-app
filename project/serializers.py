from rest_framework import serializers
from .models import Project, Category, ProjectImage, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'icon']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_at']

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'is_featured', 'uploaded_at']
        read_only_fields = ['uploaded_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'title', 'slug', 'description',
            'goal', 'category', 'tags', 'status', 'start_date',
            'end_date', 'created_at', 'images', 'progress_percentage',
            'is_owner'
        ]
        read_only_fields = ['slug', 'created_at', 'progress_percentage']

    def get_is_owner(self, obj):
        request = self.context.get('request')
        return request.user == obj.owner if request else False

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        project = Project.objects.create(**validated_data)
        project.tags.set(tags_data)
        return project