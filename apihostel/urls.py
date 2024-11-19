from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [
    path('apihostel-bedtype-api/', BedTypeApiView.as_view(), name='apihostel-bedtype-api'),
    path('apihostel-payfortype-api/', PayForTypeApiView.as_view(), name='apihostel-payfortype-api'),
    path('apihostel-bedmanagement-api/', BedManagementApiView.as_view(), name='apihostel-bedmanagement-api'),
    path('apihostel-roommanagement-api/', RoomManagementApiView.as_view(), name='apihostel-roommanagement-api'),
    path('apihostel-paymentmanage-api/', PaymentManageApiView.as_view(), name='apihostel-paymentmanage-api'),
    path('apihostel-admission-api/', HostelAdmissionApiView.as_view(), name='apihostel-admission-api'),
    path('apihostel-mealtype-api/', HostelMealTypeApiView.as_view(), name='apihostel-mealtype-api'),
    path('apihostel-meal-api/', HostelMealApiView.as_view(), name='apihostel-meal-api'),
    path('apihostel-addmeal-api/', HostelAddMealApiView.as_view(), name='apihostel-addmeal-api'),
    path('apihostel-hall-api/',Hall_details_ApiView.as_view(), name='apihostel-hall-api'),
    path('apihostel-feesmapping-api/',Hostel_Fees_Mapping_ApiView.as_view(), name='apihostel-feesmapping-api'),
    path('apihostel-fees-processing-api/',Fees_Processing_Details_ApiView.as_view(), name='apihostel-fees-processing-api'),

]
