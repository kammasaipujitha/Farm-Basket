from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem, Delivery
from products.models import Product
from accounts.models import CustomerProfile
import json

@login_required
def cart_view(request):
    """Display user's shopping cart"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied. Only customers can view cart.')
        return redirect('home')
    
    try:
        customer_profile = request.user.customer_profile
        cart, created = Cart.objects.get_or_create(customer=customer_profile)
        cart_items = cart.items.select_related('product', 'product__farmer').all()
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('home')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'orders/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add a product to cart"""
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.user.user_type != 'customer':
        if is_ajax:
            return JsonResponse({'success': False, 'message': 'Access denied'})
        else:
            messages.error(request, 'Access denied.')
            return HttpResponseRedirect(reverse('products:product_list'))
    
    try:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        customer_profile = request.user.customer_profile
        cart, created = Cart.objects.get_or_create(customer=customer_profile)
        
        # Check if product is already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart',
                'cart_count': cart.item_count
            })
        else:
            messages.success(request, 'Product added to cart!')
            return HttpResponseRedirect(reverse('products:product_list'))
        
    except Exception as e:
        if is_ajax:
            return JsonResponse({'success': False, 'message': str(e)})
        else:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse('products:product_list'))

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove an item from cart"""
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update quantity of a cart item"""
    if request.user.user_type != 'customer':
        return JsonResponse({'success': False, 'message': 'Access denied'})
    
    try:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__customer__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Item removed from cart'})
        
        if quantity > cart_item.product.stock_quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {cart_item.product.stock_quantity} {cart_item.product.unit} available'
            })
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'total_price': cart_item.total_price,
            'cart_total': cart_item.cart.total_amount
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@login_required
def checkout(request):
    """Checkout process"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied. Only customers can checkout.')
        return redirect('home')
    
    try:
        customer_profile = request.user.customer_profile
        cart = get_object_or_404(Cart, customer=customer_profile)
        cart_items = cart.items.select_related('product', 'product__farmer').all()
        
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('orders:cart')
        
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        delivery_instructions = request.POST.get('delivery_instructions', '')
        
        if not delivery_address:
            messages.error(request, 'Please provide a delivery address.')
            return render(request, 'orders/checkout.html', {
                'cart': cart,
                'cart_items': cart_items
            })
        
        # Create order
        with transaction.atomic():
            order = Order.objects.create(
                customer=customer_profile,
                total_amount=cart.total_amount,
                delivery_address=delivery_address,
                delivery_instructions=delivery_instructions
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_per_unit=cart_item.product.price_per_kg,
                    total_price=cart_item.total_price
                )
                
                # Update product stock
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('orders:payment')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'orders/checkout.html', context)

@login_required
def order_history(request):
    """Display user's order history"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied. Only customers can view order history.')
        return redirect('home')
    
    try:
        customer_profile = request.user.customer_profile
        orders = Order.objects.filter(customer=customer_profile).order_by('-created_at')
    except CustomerProfile.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('home')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_history.html', context)

@login_required
def order_detail(request, order_id):
    """Display detailed view of an order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user owns this order
    if request.user.user_type != 'customer' or order.customer.user != request.user:
        messages.error(request, 'Access denied. You can only view your own orders.')
        return redirect('orders:order_history')
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)

@login_required
@require_POST
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user owns this order
    if request.user.user_type != 'customer' or order.customer.user != request.user:
        messages.error(request, 'Access denied. You can only cancel your own orders.')
        return redirect('orders:order_history')
    
    # Check if order can be cancelled
    if order.status not in ['pending', 'confirmed']:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('orders:order_detail', order_id=order.id)
    
    with transaction.atomic():
        # Update order status
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        for order_item in order.items.all():
            order_item.product.stock_quantity += order_item.quantity
            order_item.product.save()
        
        messages.success(request, 'Order cancelled successfully.')
        return redirect('orders:order_detail', order_id=order.id)

@login_required
def payment_view(request):
    # Get the latest unpaid order for this customer
    try:
        customer_profile = request.user.customer_profile
        order = Order.objects.filter(customer=customer_profile, payment_status='pending').order_by('-created_at').first()
    except Exception:
        order = None

    if not order:
        messages.error(request, "No unpaid orders found.")
        return redirect('orders:order_history')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_status = 'paid'
        order.payment_method = payment_method
        order.status = 'confirmed'  # Set status to confirmed after payment
        order.save()
        messages.success(request, "Payment successful!")
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'payment.html', {'order': order})
