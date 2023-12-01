from django import forms
from catalog.models import Product, Blog, Version, Contact


class ProductForm(forms.ModelForm):
    """Форма для товара."""
    class Meta:
        model = Product
        exclude = ('creator',)

    def clean_title(self):
        """Валидация названия товара."""
        danger_list = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
            'бесплатно', 'обман', 'полиция', 'радар'
        ]
        cleaned_data = self.cleaned_data['title']

        for danger in danger_list:
            if danger in cleaned_data.lower():
                raise forms.ValidationError(f'Слово "{danger}" не может использоваться.')

        return cleaned_data

    def clean_description(self):
        """Валидация описания товара."""
        danger_list = [
            'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
            'бесплатно', 'обман', 'полиция', 'радар'
        ]
        cleaned_data = self.cleaned_data['description']

        for danger in danger_list:
            if danger in cleaned_data.lower():
                raise forms.ValidationError(f'Слово "{danger}" не может использоваться.')

        return cleaned_data


class VersionForm(forms.ModelForm):
    """Форма для версий."""
    class Meta:
        model = Version
        fields = '__all__'


class ContactForm(forms.ModelForm):
    """Форма обратной связи."""
    class Meta:
        model = Contact
        fields = '__all__'


class ModeratorForm(forms.ModelForm):
    """Форма для модератора."""
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)


class BlogForm(forms.ModelForm):
    """Форма для блоговых записей."""
    class Meta:
        model = Blog
        exclude = ('slug', 'view_count', 'creator',)
