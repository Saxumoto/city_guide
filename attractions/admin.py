from django.contrib import admin
from .models import Attraction

# Register the Attraction model and customize its display in the admin panel.
@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_open', 'created_at')
    list_filter = ('category', 'is_open')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'