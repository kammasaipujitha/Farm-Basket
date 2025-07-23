from django.db import models
from accounts.models import User

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('order_confirmation', 'Order Confirmation'),
        ('order_status_update', 'Order Status Update'),
        ('delivery_update', 'Delivery Update'),
        ('payment_confirmation', 'Payment Confirmation'),
        ('farmer_approval', 'Farmer Approval'),
        ('product_update', 'Product Update'),
        ('price_update', 'Price Update'),
        ('general', 'General'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Optional fields for linking to specific objects
    related_object_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'order', 'product'
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.recipient.username}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save()

class EmailNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_notifications')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Email to {self.user.email}: {self.subject}"

class SMSNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_notifications')
    message = models.TextField()
    phone_number = models.CharField(max_length=15)
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"SMS to {self.phone_number}: {self.message[:50]}..."
