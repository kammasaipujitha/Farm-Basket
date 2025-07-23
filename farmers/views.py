from django.shortcuts import render, HttpResponse, get_object_or_404
from accounts.models import FarmerProfile

# Create your views here.

def farmer_list(request):
    farmers = FarmerProfile.objects.all()
    return render(request, 'accounts/farmer_list.html', {'farmers': farmers})

def dashboard(request):
    return HttpResponse('Farmer Dashboard Placeholder')

def farmer_profile(request, farmer_id):
    farmer = get_object_or_404(FarmerProfile, id=farmer_id)
    return render(request, 'accounts/farmer_profile.html', {'farmer': farmer})
