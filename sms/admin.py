from sms.models import *
from django.contrib import admin

# Register your models here.
admin.site.register(SMS_Application_Settings)
admin.site.register(sms_template)
admin.site.register(sms_que)
admin.site.register(sms_sent)