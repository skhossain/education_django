from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('apitransport-transportationtype-api/', TransportationTypeApiView.as_view(), name='apitransport-transportationtype-api'),
    path('apitransport-transportation-api/', TransportationApiView.as_view(), name='apitransport-transportation-api'),
    path('apitransport-locationinfo-api/',LocationInfoApiView.as_view(), name='apitransport-locationinfo-api'),
    path('apitransport-vehicleinfo-api/', VehicleInfoApiView.as_view(), name='apitransport-vehicleinfo-api'),
    path('apitransport-driver-api/', DriverApiView.as_view(), name='apitransport-driver-api'),
    path('apitransport-conductor-api/', ConductorApiView.as_view(), name='apitransport-conductor-api'),
    path('apitransport-roadmap-api/', RoadMapApiView.as_view(), name='apitransport-roadmap-api'),
    path('apitransport-roadmapdtl-api/', RoadMapDetailApiView.as_view(), name='apitransport-roadmapdtl-api'),
    path('apitransport-admit-transportation-api/', Admit_TransportationApiView.as_view(), name='apitransport-admit-transportation-api'),
    path('apitransport-payfor-type-api', PayforApiView.as_view(), name='apitransport-payfor-type-api'),
    path('apitransport-paumentmanagement-api', Payment_ManagementApiView.as_view(), name='apitransport-paumentmanagement-api'),
    path('apitransport-vehicletype-api/', Vehicle_typeApiView.as_view(), name='apitransport-vehicletype-api'),
    path('apitransport-use-summery-api/', Use_summery_ApiView.as_view(), name='apitransport-vehicletype-api'),

]

