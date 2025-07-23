from django.contrib import admin
from .models import Category, Product, MarketPrice, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'farmer', 'price_per_kg', 'stock_quantity', 'is_organic', 'is_available', 'created_at')
    list_filter = ('category', 'product_type', 'is_organic', 'is_available', 'created_at')
    search_fields = ('name', 'description', 'farmer__farm_name', 'farmer__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('average_rating',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'product_type', 'farmer')
        }),
        ('Pricing & Stock', {
            'fields': ('price_per_kg', 'stock_quantity', 'unit')
        }),
        ('Product Details', {
            'fields': ('is_organic', 'is_available', 'image')
        }),
        ('Statistics', {
            'fields': ('average_rating',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'source', 'date', 'created_at')
    list_filter = ('source', 'date', 'created_at')
    search_fields = ('product__name', 'source')
    ordering = ('-date', '-created_at')
    date_hierarchy = 'date'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'caption', 'is_primary', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'caption')
    ordering = ('-created_at',)
