from django.urls import path

# For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .smsthread import *
from sms.views import *

urlpatterns = [
    path('sms-application-settings/', sms_application_settings_view.as_view(),name='sms-application-settings'),
    path('sms-application-settings-insert/', sms_application_settings_insert,name='sms-application-settings-insert'),
    path('sms-template-form/', sms_template_view.as_view(), name='sms-template-form'),
    path('sms-template-insert/', sms_template_insert, name="sms-template-insert"),
    path('sms-template-edit/<slug:id>',sms_template_edit, name="sms-template-edit"),
    path('sms-que-form/', sms_que_view.as_view(), name='sms-que-form'),
    path('sms-que-form-insert/', sms_que_form_insert, name="sms-que-form-insert"),
    path('sms-que-form-edit/<slug:id>', sms_que_form_edit, name="sms-que-form-edit"),
    path('sms-que-delete/<slug:id>', sms_que_delete, name="sms-que-delete"),    
    path('sms-sent-query/', sms_sent_query.as_view(), name='sms-sent-query'),


]

#status = fn_start_sms_job()
# For Image Upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
