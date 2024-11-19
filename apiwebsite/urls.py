from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('apiwebsite-imagecarousel-api/',imagecarouselApiView.as_view(),name='apiwebsite-imagecarousel-api'),
    path('apiwebsite-navbarmenu-api/',navbarmenuApiView.as_view(),name='apiwebsite-navbarmenu-api'),
    path('apiwebsite-navbarsubmenu-api/',navbarsubmenuApiView.as_view(),name='apiwebsite-navbarsubmenu-api'),
     path('notic_upload_pdf-api/', Notic_Upload_Pdf_Api.as_view(), name='notic_upload_pdf-api'),
     path('importent-link-api/', importent_link_Api.as_view(), name='importent-link-api'),

]