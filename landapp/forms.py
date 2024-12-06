from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Land
from django.core.validators import RegexValidator
from decimal import Decimal

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'phone_number', 'user_type')
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'phone_number', 'user_type')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'user_type')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'user_type')


class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ['location', 'photo', 'size_in_acres', 'price']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'size_in_acres': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }





class PaymentForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,  # Allow up to 15 digits for E.164
        label="Phone Number(254*********)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
        validators=[RegexValidator(regex=r'^\+?[1-9]\d{9,14}$', message="Enter a valid phone number in E.164 format.")]
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Amount (KSH)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'})
    )

