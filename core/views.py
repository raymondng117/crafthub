from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from user.models import Cart, CartItem
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def product_category(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'products.html', {'products': products, 'category': category})

def product_details(request, product_id):
    # Retrieve the product object based on the product_id
    product = Product.objects.get(pk=product_id)
    return render(request, 'product_details.html', {'product': product})

@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Get the product object
        product = get_object_or_404(Product, pk=product_id)
        
        # Get the quantity from the form
        quantity = int(request.POST.get('quantity', 1))

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the item already exists in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            # If item already exists, update the quantity
            cart_item.quantity += quantity
        else:
            # If item does not exist, create a new cart item with the specified quantity
            cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"{product} has been added to cart.")
        return redirect('core:product_details', product_id=product_id)
    else:
        # If the request method is not POST, return a bad request response
        return HttpResponseBadRequest("Bad Request: Only POST method is allowed for this endpoint.")