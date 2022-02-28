from django import forms
from webapp.models import Good, Cart, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = []

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["qty"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["goods"]


class GoodDeleteForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ()

    def clean_title(self):
        print(self.instance.title, self.cleaned_data.get("description"))
        if self.instance.title != self.cleaned_data.get("description"):
            print('error')
            raise ValidationError("Description isn't valid")
        return self.cleaned_data.get("description")