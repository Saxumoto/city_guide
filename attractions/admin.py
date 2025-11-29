from django.contrib import admin
from .models import Attraction, Review

# Register the Attraction model and customize its display in the admin panel.
@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'category', 'contributor', 'is_open', 'created_at')
    list_filter = ('status', 'category', 'is_open')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    
    # Add actions to bulk-approve items
    actions = ['approve_attractions', 'reject_attractions']

    def approve_attractions(self, request, queryset):
        updated_count = queryset.update(status='APPROVED')
        self.message_user(request, f"{updated_count} attractions were successfully marked as Approved.")
    approve_attractions.short_description = "Mark selected attractions as Approved"

    def reject_attractions(self, request, queryset):
        updated_count = queryset.update(status='REJECTED')
        self.message_user(request, f"{updated_count} attractions were marked as Rejected.")
    reject_attractions.short_description = "Mark selected attractions as Rejected"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('attraction', 'user', 'rating', 'created_at')