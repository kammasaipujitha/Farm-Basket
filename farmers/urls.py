from django.urls import path
from . import views

app_name = 'farmers'

urlpatterns = [
    path('', views.farmer_list, name='farmer_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:farmer_id>/', views.farmer_profile, name='farmer_profile'),
] 