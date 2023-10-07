from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','photo','date_joined']
    raw_id_fields=['user']
