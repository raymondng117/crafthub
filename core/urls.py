from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # URL pattern for product category
    path('<str:category>/', views.product_category, name='product_category'),

    # URL pattern for product details
    path('product/<int:product_id>/', views.product_details, name='product_details'),

    # URL pattern for adding product to cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
