from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('product/<int:product_id>/', views.review_list, name='product_reviews'),
    path('farmer/<int:farmer_id>/', views.review_list, name='farmer_reviews'),
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('helpful/<int:review_id>/', views.mark_helpful, name='mark_helpful'),
] 