from django import forms
from products.models import Category

CATEGORY_CHOISES = (
    (category.id, category.title) for category in Category.objects.all()
)


class ProductCreateForms(forms.Form):
    title = forms.CharField(max_length=100, min_length=10)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField()
    rate = forms.FloatField()
    category = forms.ChoiceField(choices=CATEGORY_CHOISES)


class ReviewCreateForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="напишите что нибудь")



