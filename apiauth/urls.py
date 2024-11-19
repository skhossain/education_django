from django.urls  import path

from .views import *
# from .views import NoticPdfInfo
# from rest_framework import routers
# router = routers.DefaultRouter()
# router.register(r'pdf-documents', NoticPdfInfo)

urlpatterns = [
    path('apiauth-branch-api/', BranchApiView.as_view(), name='apiauth-branch-api'),
    path('apiauth-country-api/', Country_Api_View.as_view(), name='apiauth-country-api'),
    path('apiauth-employee-api/', Employee_Api_View.as_view(), name='apiauth-employee-api'),
    path('apiauth-applicationuser-api/', User_Settings_Api_View.as_view(), name='apiauth-applicationuser-api'), 
    path('apiauth-division-api/', Division_Api_View.as_view(), name='apiauth-division-api'), 
    path('apiauth-district-api/', District_Api_View.as_view(), name='apiauth-district-api'), 
    path('apiauth-upazila-api/', Upazila_Api_View.as_view(), name='apiauth-upazila-api'), 
    path('apiauth-union-api/', Union_Api_View.as_view(), name='apiauth-union-api'), 
    path('notic-pdf-api/', NoticPdfInfo.as_view(), name='notic-pdf-api'),
   

]

