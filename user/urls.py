from django.urls import path
from .views import signup_view, signin_view, signout_view, cart_view, update_cart, delete_item, edit_user_info, checkout_view, purchase_history_view, delete_order_view

app_name = 'user'

urlpatterns = [
    # path is a function used to grab the html template for specific url request
    path('signup/', signup_view, name='signup'),
    path('signin/', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),
    path('cart/',cart_view, name='cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('delete-item/<int:item_id>/', delete_item, name='delete_item'),
    path('edit/', edit_user_info, name='edit_user_info'), 
    path('checkout/', checkout_view, name='checkout'),
     path('purchase-history/', purchase_history_view, name='purchase_history'),
      path('delete-order/<int:order_id>/', delete_order_view, name='delete_order'),
]
