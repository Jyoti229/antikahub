from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.db.models import Avg

from .models import Seller, AntiqueItem, Artist, Product, CartItem, Order, ProductReview, Wishlist
from .forms import RegisterForm, ContactForm, CheckoutForm


# ======================== Register ========================
def register_view(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            print("Username:", username)
            print("Password:", password)
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return render(request, 'login.html', {'username': username}) 
    return render(request, 'register.html', {'form': RegisterForm()})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


# ======================== Home ========================
def home(request):
    return render(request, 'home.html')


# ======================== Product Views ========================
def product_list(request, pk=None):
    products = AntiqueItem.objects.all()
    return render(request, 'product_list.html', {'products': products})

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']

def product_detail(request, product_id):
    product = get_object_or_404(AntiqueItem, id=product_id)
    filter_by = request.GET.get('filter', 'latest')
    reviews_qs = product.reviews.all()
    if filter_by == 'highest':
        reviews = reviews_qs.order_by('-rating', '-created_at')
    elif filter_by == 'lowest':
        reviews = reviews_qs.order_by('rating', '-created_at')
    else:  # latest
        reviews = reviews_qs.order_by('-created_at')
    avg_rating = reviews_qs.aggregate(Avg('rating'))['rating__avg']
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'filter_by': filter_by,
    })


# ======================== Artist Views ========================
def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'artist_list.html', {'artists': artists})

def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    return render(request, 'artist_detail.html', {'artist': artist})


# ======================== Contact View ========================
def contact(request):
    message_sent = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # or handle the message as you wish
            message_sent = True
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'message_sent': message_sent})


# ======================== Cart and Order ========================

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(AntiqueItem, pk=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def checkout(request):
    shipping_charge = 0
    total = 0
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            shipping_method = form.cleaned_data['shipping_method']
            payment_method = form.cleaned_data['payment_method']
            upi_id = form.cleaned_data['upi_id']
            is_prime = hasattr(request.user, 'profile') and request.user.profile.is_prime
            if shipping_method == 'standard':
                shipping_charge = 0 if is_prime else 60
            elif shipping_method == 'express':
                shipping_charge = 0 if is_prime else 150

            if payment_method == 'upi' and not upi_id:
                form.add_error('upi_id', 'Please enter your UPI ID.')
            else:
                cart_items = CartItem.objects.filter(user=request.user)
                total = sum(item.product.price * item.quantity for item in cart_items) + shipping_charge

                order = Order.objects.create(
                    user=request.user,
                    shipping_address=form.cleaned_data['shipping_address'],
                    city=form.cleaned_data['city'],
                    phone=form.cleaned_data['phone'],
                    payment_method=form.cleaned_data['payment_method'],
                    upi_id=form.cleaned_data.get('upi_id', ''),
                    shipping_charge=shipping_charge,
                    # ... other fields ...
                )

                return render(request, 'thank.html', {
                    'shipping_charge': shipping_charge,
                    'total': total,
                    'payment_method': payment_method,
                    'upi_id': upi_id
                })
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


# ======================== Authentication ========================
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


# ======================== Other Views ========================
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def buy_now(request, item_id):
    item = get_object_or_404(AntiqueItem, id=item_id)
    if request.method == 'POST':
        # Place order logic here
        order = Order.objects.create(user=request.user)
        # Add item to order, adjust as per your Order/OrderItem model
        # Example:
        # OrderItem.objects.create(order=order, product=item, quantity=1)
        return redirect('checkout')
    return render(request, 'buy_now.html', {'item': item})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(AntiqueItem, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    item.delete()
    return redirect('wishlist')

@login_required
def add_review(request, product_id):
    product = get_object_or_404(AntiqueItem, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        from .models import ProductReview
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
    return redirect('product_detail', product_id=product.id)

def about(request):
    return render(request, 'about.html')
