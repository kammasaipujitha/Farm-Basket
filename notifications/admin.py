from django.contrib import admin
from .models import Notification, EmailNotification, SMSNotification

class NotificationAdmin(admin.ModelAdmin):
    exclude = ('created_at',)

admin.site.register(Notification, NotificationAdmin)

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'is_sent', 'sent_at', 'created_at')
    list_filter = ('is_sent', 'sent_at', 'created_at')
    search_fields = ('user__username', 'user__email', 'subject')
    readonly_fields = ('sent_at',)
    ordering = ('-created_at',)

@admin.register(SMSNotification)
class SMSNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_sent', 'sent_at', 'created_at')
    list_filter = ('is_sent', 'sent_at', 'created_at')
    search_fields = ('user__username', 'phone_number')
    readonly_fields = ('sent_at',)
    ordering = ('-created_at',)
