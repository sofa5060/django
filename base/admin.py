from django.contrib import admin
from .models import ImageUpload  # Ensure the correct model name is imported

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'uploaded_at')
