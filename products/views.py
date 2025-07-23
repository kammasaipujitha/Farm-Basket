from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from .models import Product, Category, MarketPrice
from .forms import ProductForm
from accounts.models import FarmerProfile

def product_list(request, category_id=None):
    """Display list of products with optional category filtering"""
    products = Product.objects.filter(is_available=True).select_related('farmer', 'category')
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    else:
        category = None
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(farmer__farm_name__icontains=search_query)
        )
    
    # Filtering
    product_type = request.GET.get('type', '')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price_per_kg')
    elif sort_by == 'price_high':
        products = products.order_by('-price_per_kg')
    elif sort_by == 'rating':
        products = products.order_by('-average_rating')
    else:
        products = products.order_by('name')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category,
        'search_query': search_query,
        'product_type': product_type,
        'sort_by': sort_by,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    """Display detailed view of a product"""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(pk=pk)[:4]
    
    # Get market prices for this product
    market_prices = MarketPrice.objects.filter(product=product).order_by('-date')[:5]
    
    context = {
        'product': product,
        'related_products': related_products,
        'market_prices': market_prices,
    }
    
    return render(request, 'products/product_detail.html', context)

def product_search(request):
    """Handle product search"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(farmer__farm_name__icontains=query),
            is_available=True
        ).select_related('farmer', 'category')
    else:
        products = Product.objects.none()
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'products/search_results.html', context)

@login_required
def my_products(request):
    """Display farmer's own products"""
    if request.user.user_type != 'farmer':
        messages.error(request, 'Access denied. Only farmers can view their products.')
        return redirect('home')
    
    try:
        farmer_profile = request.user.farmer_profile
        products = Product.objects.filter(farmer=farmer_profile).order_by('-created_at')
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Farmer profile not found.')
        return redirect('home')
    
    context = {
        'products': products,
    }
    
    return render(request, 'products/my_products.html', context)

@login_required
def add_product(request):
    """Add a new product"""
    if request.user.user_type != 'farmer':
        messages.error(request, 'Access denied. Only farmers can add products.')
        return redirect('home')
    
    try:
        farmer_profile = request.user.farmer_profile
        if not farmer_profile.is_approved:
            messages.error(request, 'Your farmer account is not yet approved.')
            return redirect('farmers:dashboard')
    except FarmerProfile.DoesNotExist:
        messages.error(request, 'Farmer profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = farmer_profile
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('products:my_products')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product',
    }
    
    return render(request, 'products/product_form.html', context)

@login_required
def edit_product(request, pk):
    """Edit an existing product"""
    product = get_object_or_404(Product, pk=pk)
    
    # Check if user owns this product
    if request.user.user_type != 'farmer' or product.farmer.user != request.user:
        messages.error(request, 'Access denied. You can only edit your own products.')
        return redirect('products:my_products')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('products:my_products')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': 'Edit Product',
    }
    
    return render(request, 'products/product_form.html', context)

@login_required
def delete_product(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    # Check if user owns this product
    if request.user.user_type != 'farmer' or product.farmer.user != request.user:
        messages.error(request, 'Access denied. You can only delete your own products.')
        return redirect('products:my_products')
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:my_products')
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_confirm_delete.html', context)

def market_prices(request):
    """Display market prices for products"""
    market_prices = MarketPrice.objects.select_related('product', 'product__farmer').order_by('-date', 'product__name')
    
    # Group by product
    products_with_prices = {}
    for price in market_prices:
        if price.product not in products_with_prices:
            products_with_prices[price.product] = []
        products_with_prices[price.product].append(price)
    
    context = {
        'products_with_prices': products_with_prices,
    }
    
    return render(request, 'products/market_prices.html', context)

def live_market_price(request):
    """Display live market prices for vegetables, fruits, and herbs"""
    # Get latest market price for each product, filtered by type
    products = Product.objects.filter(
        product_type__in=['vegetable', 'fruit', 'herb']
    ).select_related('category')
    
    latest_prices = []
    for product in products:
        price = product.market_prices.order_by('-date').first()
        if price:
            latest_prices.append({'product': product, 'price': price})
    
    # Sort by product type and name
    latest_prices.sort(key=lambda x: (x['product'].product_type, x['product'].name))
    
    # Group by product type
    prices_by_type = {
        'vegetable': [],
        'fruit': [],
        'herb': []
    }
    
    for item in latest_prices:
        prices_by_type[item['product'].product_type].append(item)
    
    context = {
        'latest_prices': latest_prices,
        'prices_by_type': prices_by_type,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, 'products/live_market_price.html', context)
