
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Category, Tag, ProjectImage


# إعدادات لعرض الصور في لوحة التحكم
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        return format_html('<img src="{}" width="100" height="auto" />', obj.image.url) if obj.image else "-"

    image_preview.short_description = "Preview"


# فلترة المشاريع في لوحة التحكم
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'status', 'goal', 'start_date', 'end_date', 'progress_bar']
    list_filter = ['status', 'category', 'tags']
    search_fields = ['title', 'description', 'owner__username']
    filter_horizontal = ['tags']
    inlines = [ProjectImageInline]
    readonly_fields = ['created_at', 'updated_at', 'progress_bar']

    # دالة لعرض شريط التقدم
    def progress_bar(self, obj):
        return format_html(
            '<progress value="{}" max="100" style="width:100px"></progress> {}%',
            obj.progress_percentage,
            obj.progress_percentage
        )

    progress_bar.short_description = "Progress"


# تسجيل النماذج
admin.site.register(Project, ProjectAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProjectImage)