from django.contrib import admin
from .models import Review, ReviewImage, ReviewHelpful

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at', 'product__category')
    search_fields = ('customer__user__username', 'product__name', 'title', 'comment')
    readonly_fields = ('is_verified_purchase',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('customer', 'product', 'rating', 'title', 'comment')
        }),
        ('Verification', {
            'fields': ('is_verified_purchase',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ('review', 'caption', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('review__customer__user__username', 'review__product__name', 'caption')
    ordering = ('-created_at',)

@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'is_helpful', 'created_at')
    list_filter = ('is_helpful', 'created_at')
    search_fields = ('review__customer__user__username', 'user__username')
    ordering = ('-created_at',)
