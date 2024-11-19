from logging import exception
from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import *

YES_NO = (
    ('Y', 'Yes'),
    ('N', 'No')
)


SALES_REPORT_TYPE = (
    ('DT', 'Date Wise'),
    ('PR', 'Product Wise'),
    ('CS', 'Customer Wise'),
    ('BR', 'Branch Wise'),
    ('IN', 'Invoice Wise')
)


class DateInput(forms.DateInput):
    input_type = 'date'


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class SMS_Application_Settings_Form(forms.ModelForm):
    # branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    # product_id = ChoiceFieldNoValidation(label="Product Name", required=True)

    def __init__(self, *args, **kwargs):
        super(SMS_Application_Settings_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = SMS_Application_Settings
        fields = ['messaging_auth_url', 'messaging_url', 'messaging_username',
                  'messaging_password', 'total_message_limit', 'is_messaging_on', 'total_message_sent', 'senderid', 'api_key', 'is_headers_require', 'messaging_error']

        # widgets = {
        #     'comments': Textarea(attrs={'rows': 2, 'cols': 60, }),
        #     'expence_date': DateInput(),
        # }

        labels = {
            "messaging_auth_url": _("Message auth url"),
            "messaging_url": _("Message Url"),
            "messaging_username": _("UserName"),
            "messaging_password": _("Messaging Password"),
            "total_message_limit": _("Total Message Limit"),
            "is_messaging_on": _("Is Message on"),
            "total_message_sent": _("Total Message Sent"),
            "senderid": _("Sender Id"),
            "api_key": _("API Key"),
            "is_headers_require": _("Is Headers Require"),
            "messaging_error": _("Message Error"),
        }
        
        
class sms_template_Form(forms.ModelForm):
  
    class Meta:
        model = sms_template
        fields = ['template_type', 'template_text', 'message_type',
                  'message_label', 'minimum_tran_amount', 'is_messaging_enable']

        widgets = {
            'template_text': Textarea(attrs={'rows': 2, 'cols': 60, }),
        }

        labels = {
            "template_type": _("Template Type"),
            "template_text": _("Template Text "),
            "message_type": _("Message Type"),
            "message_label": _("Message Label"),
            "minimum_tran_amount": _("Minimum Transaction Amount"),
            "is_messaging_enable": _("Message Enable"),
        }
        

class SMS_Que_Form(forms.ModelForm):
    sms_balance = forms.CharField(
        label='SMS Balance', initial="", required=False)

    def __init__(self, *args, **kwargs):
        super(SMS_Que_Form, self).__init__(*args, **kwargs)
        self.fields['sms_balance'].widget.attrs['readonly'] = True
        self.fields['sms_balance'].required = False

    class Meta:
        model = sms_que
        fields = ['mobile_number', 'text_message']

        widgets = {
            'text_message': Textarea(attrs={'rows': 3, 'cols': 60, }),
        }

        labels = {
            "mobile_number": _("Send To (Mobile No)"),
            "text_message": _("Message Body ")
        }

class SMS_Sent_Form(forms.ModelForm):
    sms_balance = forms.CharField(
        label='SMS Balance', initial="", required=False)
    from_date = forms.DateField(
        label="From Date", widget=DateInput(), required=True)
    upto_date = forms.DateField(
        label="Upto Date", widget=DateInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(SMS_Sent_Form, self).__init__(*args, **kwargs)
        self.fields['sms_balance'].widget.attrs['readonly'] = True
        self.fields['sms_balance'].required = False

    class Meta:
        model = sms_sent
        fields = ['mobile_number', 'text_message', 'template_type']

        widgets = {
            'text_message': Textarea(attrs={'rows': 3, 'cols': 60, }),
        }

        labels = {
            "mobile_number": _("Send To (Mobile No)"),
            "text_message": _("Message Body "),
            "template_type": _("SMS Type ")
        }
