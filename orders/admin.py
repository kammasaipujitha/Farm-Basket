from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Delivery, OrderTracking

# Custom admin actions for order status
@admin.action(description="Mark selected orders as Shipped")
def mark_as_shipped(modeladmin, request, queryset):
    queryset.update(status='processing')

@admin.action(description="Mark selected orders as Out for Delivery")
def mark_as_out_for_delivery(modeladmin, request, queryset):
    queryset.update(status='shipped')

@admin.action(description="Mark selected orders as Delivered")
def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status='delivered')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'item_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('customer__user__username', 'customer__user__email')
    readonly_fields = ('total_amount', 'item_count')
    ordering = ('-created_at',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'total_price', 'added_at')
    list_filter = ('added_at', 'product__category')
    search_fields = ('cart__customer__user__username', 'product__name')
    readonly_fields = ('total_price',)
    ordering = ('-added_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'total_amount', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'customer__user__username', 'customer__user__email')
    readonly_fields = ('order_number', 'total_amount')
    ordering = ('-created_at',)
    actions = [mark_as_shipped, mark_as_out_for_delivery, mark_as_delivered]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'status', 'total_amount')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'delivery_instructions')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_per_unit', 'total_price')
    list_filter = ('product__category', 'product__farmer')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('total_price',)
    ordering = ('-order__created_at',)

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('order', 'delivery_date', 'delivery_time_slot', 'is_delivered', 'delivered_at')
    list_filter = ('delivery_date', 'is_delivered', 'delivered_at')
    search_fields = ('order__order_number', 'order__customer__user__username')
    ordering = ('-delivery_date',)

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'location', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('order__order_number', 'status', 'location')
    ordering = ('-timestamp',)
