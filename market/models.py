from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# ----------------------------
# Seller Profile
# ----------------------------
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# ----------------------------
# Antique Item listed by Seller
# ----------------------------
class AntiqueItem(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    origin = models.CharField(max_length=100)
    era = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='antiques/')
    listed_on = models.DateTimeField(auto_now_add=True)
    artist = models.ForeignKey('Artist', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# ----------------------------
# Artist Information
# ----------------------------
class Artist(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='artist_photos/', blank=True, null=True)  # <-- Add this line

    def __str__(self):
        return self.name


# ----------------------------
# Products available in the marketplace
# ----------------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()

    def __str__(self):
        return self.name


# ----------------------------
# Shopping cart items
# ----------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(AntiqueItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"


# ----------------------------
# Orders placed by users
# ----------------------------
ORDER_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('SHIPPED', 'Shipped'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    payment_method = models.CharField(max_length=20, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def get_total(self):
        # If your OrderItem model uses related_name='items'
        return sum(item.product.price * item.quantity for item in self.items.all())
        # If you did NOT set related_name, use:
        # return sum(item.product.price * item.quantity for item in self.orderitem_set.all())


# ----------------------------
# Items linked to each order
# ----------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

# ----------------------------
# Contact Messages (e.g., Contact Us form)
# ----------------------------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"


# ----------------------------
# User Profile
# ----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_prime = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Only save if profile exists
        if hasattr(instance, 'profile'):
            instance.profile.save()


# ----------------------------
# Product Reviews
# ----------------------------
class ProductReview(models.Model):
    product = models.ForeignKey(AntiqueItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ----------------------------
# Wishlist for users
# ----------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(AntiqueItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')
