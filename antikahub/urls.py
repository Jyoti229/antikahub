from django.urls import path
from market import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('artists/', views.artist_list, name='artist_list'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('contact/', views.contact, name='contact'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register_view, name='register'),  # ✅ Only this line
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('order-history/', views.order_history, name='order_history'),
    path('buy/<int:item_id>/', views.buy_now, name='buy_now'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('about/', views.about, name='about'),
]


# ✅ This must be **outside** the list
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
