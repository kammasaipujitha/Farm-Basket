from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('search/', views.product_search, name='product_search'),
    path('my-products/', views.my_products, name='my_products'),
    path('add/', views.add_product, name='add_product'),
    path('<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('market-prices/', views.live_market_price, name='live_market_price'),
] 