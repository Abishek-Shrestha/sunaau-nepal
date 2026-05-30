from django.contrib import admin
from .models import Issue, IssueUpdate, Notification

class IssueUpdateInline(admin.TabularInline):
    model = IssueUpdate
    extra = 1

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'severity', 'status', 'municipality', 'ward_number', 'created_at']
    list_filter = ['status', 'category', 'severity', 'municipality']
    search_fields = ['title', 'description', 'location_name']
    inlines = [IssueUpdateInline]

@admin.register(IssueUpdate)
class IssueUpdateAdmin(admin.ModelAdmin):
    list_display = ['issue', 'updated_by', 'old_status', 'new_status', 'created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'notification_type']
    list_editable = ['is_read']
    
