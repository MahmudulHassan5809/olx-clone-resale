from django import forms
from django.forms import ModelForm
from products.models import Category, Product


class AdPostForm(ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Images For Ad')

    class Meta:
        model = Product
        exclude = ['owner', 'active', 'created_at', 'slug']

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if len(images) > 4:
            raise forms.ValidationError(
                "You Can Not Upload More Than 4 Images")
        return images

    def clean_city(self):
        return self.cleaned_data.get('city').title()

    def clean_area(self):
        return self.cleaned_data.get('area').title()

    def __init__(self, *args, **kwargs):
        # call the parent init
        super(AdPostForm, self).__init__(*args, **kwargs)
        # change the widget to use checkboxes
        self.fields['category'] = forms.ModelChoiceField(
            queryset=Category.objects.all())
