from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import NewsletterSubscriber, ProductRating


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "email@example.com"}))


class PasswordResetConfirmForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "email@example.com"}))
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={"placeholder": "123456"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "New password"}))


class NewsletterSubscriberForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        }


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = ["user_name", "score", "comment"]
        widgets = {
            "user_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "score": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Your feedback"}),
        }
