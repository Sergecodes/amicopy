from ckeditor.widgets import CKEditorWidget
from django import forms
from django.utils.translation import gettext_lazy as _

from .models.models import Device, Session, Transaction


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['display_name']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'text_content', ]

    # def __init__(self, *args, **kwargs):
	# 	# Do not use kwargs.pop('user', None) due to potential security loophole 
    #     # (the user object must be in the form!)
    #     user = kwargs.pop('user')
    #     super().__init__(*args, **kwargs)

    #     # Update user text content widget 
    #     if user.can_use_rich_text_editor:
    #         text_widget = CKEditorWidget(config_name='listing_description')
    #     else:
    #         text_widget = forms.Textarea(attrs={'rows': 5, 'cols': 40})
            
    #     self.fields['text_content'].widget = text_widget


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['title', 'creator_code']

