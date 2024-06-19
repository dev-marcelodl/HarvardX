from django import forms
from django.forms import Textarea
from .models import Auction 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import (
    PrependedText, PrependedAppendedText, FormActions)

class AuctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuctionForm, self).__init__(*args, **kwargs) 
        helper = FormHelper()
        helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
        helper.form_method = 'POST'

    class Meta:
        model = Auction
        fields = ['title','description', 'category', 'price', 'image']
        labels = {
            'title': ('Title:'),
            'description': ('Description:'),
            'category': ('Category'),
            'price': ('Price:'),
            'image': ('URL Image:'),
        }
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 20}),
        }