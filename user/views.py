from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cart, CartItem, UserAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserAddressForm, UserForm
from django.views.decorators.csrf import csrf_exempt

# When a user visits the signup page (/user/signup/), the view renders a form using the UserCreationForm provided by Django's authentication system.
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:signin')
    else:
        form = UserCreationForm()

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'signup.html', {'form': form})

@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index:landingpage')  # Remove {'user': user}
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'signin.html', {'form': form})

@csrf_exempt
def signout_view (request):
    logout(request)
    return redirect('index:landingpage')

@csrf_exempt
@login_required
def edit_user_info(request):
    # Get the current user's instance
    user = request.user
    # Check if the user has a related UserAddress instance
    user_address = user.useraddress_set.first()
    
    # If user_address is None, create a new UserAddress instance
    if user_address is None:
        user_address = UserAddress(user=user)

    if request.method == 'POST':
        # Populate the forms with POST data and instance
        user_form = UserForm(request.POST, instance=user)
        address_form = UserAddressForm(request.POST, instance=user_address)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()
            # Add success message
            messages.success(request, 'Information has been updated.')
            # Redirect to a success page or back to the edit page
            return redirect('user:edit_user_info')
        else:
            # Add error message
            messages.error(request, 'Information can not be updated now. Please try again later.')
    else:
        # Populate the forms with instance data
        user_form = UserForm(instance=user)
        address_form = UserAddressForm(instance=user_address)
        
    for field in user_form.fields.values():
        field.widget.attrs.update({'class': 'form-control col-3 text-start'})
      
    for field in address_form.fields.values():
        field.widget.attrs.update({'class': 'form-control col-3 text-start'})  

    return render(request, 'user_info.html', {'user_form': user_form, 'address_form': address_form})

@csrf_exempt
@login_required
def cart_view(request):
    # Retrieve the current user's cart
    user_cart = Cart.objects.filter(user=request.user).first()
    user_addresses = UserAddress.objects.filter(user=request.user)

    # Initialize cart_item_data and total_prices
    cart_item_data = []
    total_prices = 0

    if user_cart:
        # Retrieve cart items for the user's cart
        cart_items = CartItem.objects.filter(cart=user_cart)

        for cart_item in cart_items:
            # Access the product information using foreign key relationship
            product = cart_item.product

            # Calculate the total price for the cart item
            total_price = cart_item.quantity * product.price
            total_prices += total_price
            # Create a dictionary to store cart item and product information
            cart_item_info = {
                'id': cart_item.id,
                'quantity': cart_item.quantity,
                'product_name': product.name,
                'product_price': product.price,
                'total_price': total_price,
                # Add more product fields as needed
            }
            cart_item_data.append(cart_item_info)

    if request.method == 'POST':
        # Handle updating quantity for cart items
        for cart_item_info in cart_item_data:
            cart_item_id = cart_item_info['id']
            quantity_key = f'quantity_{cart_item_id}'
            if quantity_key in request.POST:
                new_quantity = int(request.POST[quantity_key])
                if new_quantity > 0:
                    cart_item = CartItem.objects.get(pk=cart_item_id)
                    cart_item.quantity = new_quantity
                    cart_item.save()
                else:
                    # Remove item from cart if quantity is zero
                    CartItem.objects.filter(pk=cart_item_id).delete()
                    return redirect('user:cart')

    # Render the template with the cart item data
    return render(request, 'cart.html', {'cart_items': cart_item_data, 'total_prices': total_prices, 'addresses': user_addresses})

@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        # Handle updating quantity for cart items
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                cart_item_id = int(key.replace('quantity_', ''))
                new_quantity = int(value)
                if new_quantity > 0:
                    cart_item = CartItem.objects.get(pk=cart_item_id)
                    cart_item.quantity = new_quantity
                    cart_item.save()
                else:
                    # Remove item from cart if quantity is zero
                    CartItem.objects.filter(pk=cart_item_id).delete()
        messages.success(request, "Cart updated successfully.")
    return redirect('user:cart')

@csrf_exempt
def delete_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"{product_name} removed from cart.")
    return redirect('user:cart')

@csrf_exempt
@login_required
def checkout_view(request):
    if request.method == 'POST':
        user_cart = Cart.objects.filter(user=request.user).first()
        user_addresses = UserAddress.objects.filter(user=request.user)

        if not user_cart or not user_cart.items.exists():
            messages.error(request, "Your cart is empty. Please add items to proceed with checkout.")
            return redirect('user:cart')

        if not user_addresses.exists():
            messages.error(request, "You must have at least one address set up to proceed with checkout.")
            return redirect('user:edit_user_info')

        selected_address_id = request.POST.get('address')
        if not selected_address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect('user:cart')

        # Create the Order with the selected address
        selected_address = UserAddress.objects.get(id=selected_address_id)
        order = Order.objects.create(user=request.user, address=selected_address)

        # Create OrderItems
        cart_items = CartItem.objects.filter(cart=user_cart)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the cart after creating the order
        user_cart.delete()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('user:cart')

    return redirect('user:cart')

@csrf_exempt
@login_required
def purchase_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    order_data = []
    order_number = 0
    
    for order in orders:
        order_number += 1
        total_quantity = sum(item.quantity for item in order.items.all())
        total_price = sum(item.price * item.quantity for item in order.items.all())
        order_data.append({
            'order': order,
            'total_quantity': total_quantity,
            'total_price': total_price,
            'order_number' : order_number,
        })
    return render(request, 'purchase_history.html', {'order_data': order_data})

@csrf_exempt
@login_required
def delete_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect('user:purchase_history')