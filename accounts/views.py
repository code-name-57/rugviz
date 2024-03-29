from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Address, Order, OrderItem, Retailer, Consumer, Cart, CartItem
from catalog.models import Carpet
from .forms import RetailerRegistrationForm, ConsumerRegistrationForm, UserForm, CheckoutForm, AddressForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'cube/account/register.html'

def register_as_retailer(request):
    register_user_uri = "cube/account/register_user.html"
    user = request.user
    if user.is_authenticated:
        try:
            retailer = Retailer.objects.get(user=user)
        except Retailer.DoesNotExist:
            retailer = Retailer()
        form_data_list = [request.POST] if request.POST else list()
        user_form = UserForm(*form_data_list, instance=user)
        registration_form = RetailerRegistrationForm(*form_data_list, instance = retailer)
    else:
        # Signing required
        return redirect('login')
    if request.method == "GET":
        # TODO: A user can either be a consumer or a retailer. Add that check here
        # and provide an option to switch b/w consumers and retailers.
        return render(request, register_user_uri,
                      dict(registration_form=registration_form,
                            user_form=user_form))

    if registration_form.is_valid() and user_form.is_valid():
        user_form.save()
        obj = registration_form.save(commit = False)
        obj.user = user
        obj.save()
        messages.success(request,
            "User registration request sent successfully! Verification would be complete after verification")
        # TODO: create a page to view the user profile
        return redirect('list')

    return render(request, register_user_uri,
                  dict(registration_form=registration_form,
                        user_form=user_form))


def register_as_consumer(request):
    register_user_uri = "cube/account/register_user.html"
    user = request.user
    if user.is_authenticated:
        try:
            consumer = Consumer.objects.get(user=user)
        except Consumer.DoesNotExist:
            consumer = Consumer()
        form_data_list = [request.POST] if request.POST else list()
        user_form = UserForm(*form_data_list, instance=user)
        registration_form = ConsumerRegistrationForm(*form_data_list, instance = consumer)
    else:
        # Signing required
        return redirect('login')
    if request.method == "GET":
        return render(request, register_user_uri,
                      dict(registration_form=registration_form,
                            user_form=user_form))

    if registration_form.is_valid() and user_form.is_valid():
        user_form.save()
        obj = registration_form.save(commit = False)
        obj.user = user
        obj.save()
        messages.success(request,
            "Registered as a consumer! Now you can shop online.")
        return redirect('list')

    return render(request, register_user_uri,
                  dict(registration_form=registration_form,
                        user_form=user_form))

def add_to_cart(request, carpet_id, quantity = 1, redirect_to_cart=True):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()
    carpet = Carpet.objects.get(id = carpet_id)

    try:
        cartItem = CartItem.objects.get(carpet = carpet, cart = cart)
        qty = cartItem.quantity
        cartItem.quantity = qty + quantity
    except CartItem.DoesNotExist:
        cartItem = CartItem(carpet=carpet, cart = cart)
    cartItem.save()
    if redirect_to_cart:
        return redirect("cart")
    else:
        return redirect("carpets", carpet_id=carpet.id)

def deduct_from_cart(request, carpet_id):
    # TODO: Number can be changed directly in the qty, handler that
    # TODO: add same in basic cart page
    # TODO: activate remove link
    return add_to_cart(request, carpet_id, -1)

def remove_from_cart(request, carpet_id):
    try:
        cart = Cart.objects.get(user = request.user)
    except Cart.DoesNotExist:
        cart = Cart(user=request.user)
        cart.save()
    carpet = Carpet.objects.get(id = carpet_id)

    try:
        cartItem = CartItem.objects.get(carpet = carpet, cart = cart)
        cartItem.delete()
    except CartItem.DoesNotExist:
        cartItem = CartItem(carpet=carpet, cart = cart)
    return redirect("cart")

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    checkout_form = CheckoutForm()
    address_form = AddressForm()
    context = {'checkout_form' : checkout_form, 'address_form': address_form }
    user = request.user
    if request.method == "POST":
        form_data_list = [request.POST] if request.POST else list()
        address_form = AddressForm(*form_data_list) # user__address
        checkout_form = CheckoutForm(*form_data_list)
        if address_form.is_valid() and checkout_form.is_valid():
            address = address_form.save()
            order = checkout_form.save(commit = False)
            order.user = user
            order.address = address
            order.save()
            for item in user.cart.cartitem_set.all():
                orderItem = OrderItem(order = order, quantity = item.quantity, unit_price = item.unit_price, carpet_id = item.carpet_id)
                orderItem.save()
    return render(request, "cube/shop/shop-checkout.html", context)

def OrderHistory(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    orders = user.order_set.all()
    context = {'orders' : orders}
    return render(request, "cube/account/account-orders.html", context)