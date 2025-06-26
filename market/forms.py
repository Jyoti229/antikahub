from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage

# Contact Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

# Register Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your shipping address'}),
        required=True,
        label="Shipping Address"
    )
    city = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=20, required=True)
    payment_method = forms.ChoiceField(
        choices=[('cod', 'Cash on Delivery'), ('upi', 'UPI')],
        widget=forms.Select(attrs={'id': 'id_payment_method'})
    )
    upi_id = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your UPI ID', 'id': 'upi-id'})
    )
    shipping_method = forms.ChoiceField(
        choices=[('standard', 'Standard Shipping'), ('express', 'Express Shipping')],
        widget=forms.Select(attrs={'id': 'id_shipping_method'}),
        required=True
    )
    shipping_charge = forms.DecimalField(
        widget=forms.HiddenInput(),
        required=False,
        initial=60
    )
