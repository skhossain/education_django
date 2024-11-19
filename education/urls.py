from django.contrib import admin
from django.urls import path, include
from filebrowser.sites import site

urlpatterns = [
    path('webadm/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('webadm/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('student/', include('studentportal.urls')),
    path('apistudent/',include('apistudentportal.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('',include('appauth.urls')),
    path('',include('apiauth.urls')),
    path('',include('finance.urls')),
    path('',include('apifinance.urls')),
    path('',include('hrm.urls')),
    path('',include('edu.urls')),
    path('',include('hostel.urls')),
    path('',include('apihrm.urls')),
    path('',include('apiedu.urls')),
    path('',include('apihostel.urls')),
    path('',include('transport.urls')),
    path('',include('apitransport.urls')),
    path('', include('sms.urls')),
    path('', include('apisms.urls')),
    path('', include('website.urls')),
    path('', include('apiwebsite.urls')),

    
]