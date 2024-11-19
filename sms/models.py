from django.db import models
from .smstemplate import *

SMS_SOURCE = (
    ('P', 'Percentage'),
    ('F', 'Fixed Amount'),
)


OPERATOR_LIST = (
    ('1', 'ADN SMS'),
    ('2', 'sManager'),
    ('3', 'REVE'),
)


class SMS_Application_Settings(models.Model):
    messaging_auth_url = models.CharField(max_length=500, null=False)
    messaging_url = models.CharField(max_length=500, null=False)
    messaging_username = models.CharField(max_length=500, null=False)
    messaging_password = models.CharField(max_length=500, null=False)
    total_message_limit = models.IntegerField(blank=True, null=True)
    is_messaging_on = models.BooleanField(default=False)
    total_message_sent = models.IntegerField(blank=True, null=True)
    senderid = models.CharField(max_length=500, null=True, blank=True)
    api_key = models.CharField(max_length=500, null=True, blank=True)
    api_secret = models.CharField(max_length=500, null=True, blank=True)
    client_id = models.CharField(max_length=500, null=True, blank=True)
    balance_url = models.CharField(max_length=500, null=True, blank=True)
    sms_api = models.CharField(
        max_length=10, choices=OPERATOR_LIST, default='')
    is_headers_require = models.BooleanField(default=False)
    messaging_error = models.CharField(max_length=500, null=True, blank=True)
    

    def __str__(self):
        return str(self.messaging_url)


class sms_que(models.Model):
    template_type = models.CharField(
        max_length=10, choices=TEMPLATE_LIST, default='')
    mobile_number = models.CharField(max_length=20, null=False)
    text_message = models.CharField(max_length=500, null=False)
    message_error = models.CharField(max_length=500, null=True, blank=True)
    app_user_id = models.CharField(max_length=20, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.mobile_number)

class sms_sent(models.Model):
    template_type = models.CharField(
        max_length=10, choices=TEMPLATE_LIST, default='')
    mobile_number = models.CharField(max_length=20, null=False)
    text_message = models.CharField(max_length=500, null=False)
    sms_uid = models.CharField(max_length=500, null=True, blank=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.mobile_number)

class sms_template(models.Model):
    template_type = models.CharField(
        max_length=10, choices=TEMPLATE_LIST, default='')
    template_text = models.CharField(max_length=500, null=False)
    message_type = models.CharField(
        max_length=100, choices=MESSAGE_TYPE, default='')
    message_label = models.CharField(
        max_length=100, choices=MESSAGE_LABEL, default='')
    minimum_tran_amount = models.DecimalField(
        max_digits=22, decimal_places=2, default=0.00)
    is_messaging_enable = models.BooleanField(default=False)
    app_user_id = models.CharField(max_length=20, null=False)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.template_type)+' '+str(self.template_text)

class sms_key_value(models.Model):
    identity_id =  models.CharField(max_length=50, null=False)
    message_key = models.CharField(max_length=200, null=False)
    message_value = models.CharField(max_length=500, null=False)