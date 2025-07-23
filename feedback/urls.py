from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('submit/', views.feedback_form, name='feedback_form'),
] 