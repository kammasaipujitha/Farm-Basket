from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, FarmerProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Farm Basket Info', {
            'fields': ('user_type', 'phone_number', 'address', 'profile_picture', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Farm Basket Info', {
            'fields': ('user_type', 'phone_number', 'address', 'profile_picture', 'is_verified')
        }),
    )

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_delivery_address', 'delivery_instructions')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user__date_joined',)

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'farm_name', 'is_approved', 'years_of_experience', 'approved_by', 'approved_at')
    list_filter = ('is_approved', 'years_of_experience', 'approved_at')
    search_fields = ('user__username', 'farm_name', 'farm_address')
    readonly_fields = ('approved_at',)
    
    actions = ['approve_farmers', 'disapprove_farmers']
    
    def approve_farmers(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(
            is_approved=True,
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f'{updated} farmer(s) approved successfully.')
    approve_farmers.short_description = "Approve selected farmers"
    
    def disapprove_farmers(self, request, queryset):
        updated = queryset.update(
            is_approved=False,
            approved_by=None,
            approved_at=None
        )
        self.message_user(request, f'{updated} farmer(s) disapproved successfully.')
    disapprove_farmers.short_description = "Disapprove selected farmers"
