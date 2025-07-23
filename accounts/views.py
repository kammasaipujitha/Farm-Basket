from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, CustomerProfile, FarmerProfile
from .forms import UserRegistrationForm, CustomerProfileForm, FarmerProfileForm, UserProfileForm

def register(request):
    """Main registration page that redirects to specific registration forms"""
    return render(request, 'accounts/register_choice.html')

def customer_register(request):
    """Customer registration view"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = CustomerProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'customer'
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Farm Basket.')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = CustomerProfileForm()
    
    return render(request, 'accounts/customer_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def farmer_register(request):
    """Farmer registration view"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = FarmerProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'farmer'
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            messages.success(request, 'Farmer account created successfully! Your account will be reviewed by our admin team.')
            return redirect('accounts:login')
    else:
        user_form = UserRegistrationForm()
        profile_form = FarmerProfileForm()
    
    return render(request, 'accounts/farmer_register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    """User profile view"""
    if request.user.user_type == 'customer':
        profile = get_object_or_404(CustomerProfile, user=request.user)
    elif request.user.user_type == 'farmer':
        profile = get_object_or_404(FarmerProfile, user=request.user)
    else:
        profile = None
    
    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    """Edit user profile view"""
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        
        if request.user.user_type == 'customer':
            profile_form = CustomerProfileForm(request.POST, instance=request.user.customer_profile)
        elif request.user.user_type == 'farmer':
            profile_form = FarmerProfileForm(request.POST, instance=request.user.farmer_profile)
        else:
            profile_form = None
        
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        
        if request.user.user_type == 'customer':
            profile_form = CustomerProfileForm(instance=request.user.customer_profile)
        elif request.user.user_type == 'farmer':
            profile_form = FarmerProfileForm(instance=request.user.farmer_profile)
        else:
            profile_form = None
    
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
