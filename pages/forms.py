from django import forms

from .models import NewsletterSubscriber, ProductRating


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
