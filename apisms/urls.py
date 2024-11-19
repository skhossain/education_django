from django.urls  import path

from .views import *

urlpatterns = [
    path('apisms-application-setting-api/',  SMS_Application_Setting_ApiView.as_view(), name='apisms-application-setting-api'), 
    path('apisms-template-api/',  SMS_template_ApiView.as_view(), name='apisms-template-api'), 
    path('apisms-sent-api/',  SMS_Sent_ApiView.as_view(), name='apisms-sent-api'), 
    path('apisms-que-api/',  SMS_que_ApiView.as_view(), name='apisms-que-api'), 

]



