from django.contrib import admin
from .models import (
    Seller, AntiqueItem, Artist,
    Product, CartItem, Order, OrderItem,
    ContactMessage
)

# ----------------------------
# Seller Admin
# ----------------------------
@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact')
    search_fields = ('user__username', 'contact')


# ----------------------------
# Antique Item Admin
# ----------------------------
@admin.register(AntiqueItem)
class AntiqueItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'origin', 'era', 'price', 'listed_on')
    list_filter = ('origin', 'era')
    search_fields = ('name', 'description')


# ----------------------------
# Artist Admin
# ----------------------------
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'birth_year', 'death_year')
    search_fields = ('name', 'country')


# ----------------------------
# Product Admin
# ----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')


# ----------------------------
# Cart Item Admin
# ----------------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_on')
    list_filter = ('added_on',)
    search_fields = ('user__username', 'product__name')


# ----------------------------
# Inline for OrderItem in Order Admin
# ----------------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


# ----------------------------
# Order Admin
# ----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    inlines = [OrderItemInline]


# ----------------------------
# Contact Message Admin
# ----------------------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_on')
    search_fields = ('name', 'email')
    list_filter = ('submitted_on',)
