from django.contrib import admin
from .models import Contact, Deal, Activity

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "email", "phone", "status", "created_at"]
    list_filter = ["status", "source"]
    search_fields = ["name", "company", "email"]

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ["title", "company", "value", "stage", "probability", "created_at"]
    list_filter = ["stage"]
    search_fields = ["title", "company"]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["subject", "related_to", "activity_type", "scheduled", "done", "created_at"]
    list_filter = ["activity_type"]
    search_fields = ["subject", "related_to"]
