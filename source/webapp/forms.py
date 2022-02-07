from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Good, Category


class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        exclude = []
        widgets = {
            'detailed_description': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        }

    def clean_description(self):
        if len(self.cleaned_data.get('description')) < 20:
            raise ValidationError(f"The description field must be more than 20 symbols!")
        return self.cleaned_data.get('description')

    def clean_detailed_description(self):
        if len(self.cleaned_data.get('detailed_description')) > 2000:
            raise ValidationError(f"The detailed description field must be less than 2000 symbols!")
        return self.cleaned_data.get('detailed_description')


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Search")


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


# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['username', 'phone', 'address']