from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('transport-transportation-type', transport_transportation_type.as_view(),name='transport-transportation-type'),
    path('transport-transportationtype-insert',transport_transportationtype_insert,name='transport-transportationtype-insert'),
    path('transport-transportationtype-edit/<slug:id>', transport_transportationtype_edit, name='transport-transportationtype-edit'),

    path('transport-transportation', transport_transportation.as_view(),name='transport-transportation'),
    path('transport-transportation-insert',transport_transportation_insert,name='transport-transportation-insert'),
    path('transport-transportation-edit/<slug:id>', transport_transportation_edit, name='transport-transportation-edit'),
    
    path('transport-location-info', transport_location_info.as_view(),name='transport-location-info'),
    path('transport-locationinfo-insert',transport_locationinfo_insert,name='transport-locationinfo-insert'),
    path('transport-locationinfo-edit/<slug:id>', transport_locationinfo_edit, name='transport-locationinfo-edit'),
    
    path('transport-vehicle-type', transport_vehicle_type.as_view(),name='transport-vehicle-type'),
    path('transport-vehicletype-insert',transport_vehicle_type_insert,name='transport-vehicletype-insert'),
    path('transport-vehicletype-edit/<slug:id>', transport_vehicle_type_edit, name='transport-vehicletype-edit'),
    

    path('transport-vehicle-info', transport_vehicle_info.as_view(),name='transport-vehicle-info'),
    path('transport-vehicleinfo-insert',transport_vehicleinfo_insert,name='transport-vehicleinfo-insert'),
    path('transport-vehicleinfo-edit/<slug:id>', transport_vehicleinfo_edit, name='transport-vehicleinfo-edit'),
    
    path('transport-driver-info', transport_driver_info.as_view(),name='transport-driver-info'),
    path('transport-driver-insert',transport_driver_insert,name='transport-driver-insert'),
    path('transport-driver-edit/<slug:id>', transport_driver_edit, name='transport-driver-edit'),
    
    path('transport-conductor-info', transport_conductor_info.as_view(),name='transport-conductor-info'),
    path('transport-conductor-insert',transport_conductor_insert,name='transport-conductor-insert'),
    path('transport-conductor-edit/<slug:id>', transport_conductor_edit, name='transport-conductor-edit'),
    
    path('transport-road-map', transport_roadmap_info.as_view(),name='transport-road-map'),
    path('transport-roadmap-insert',transport_roadmap_insert,name='transport-roadmap-insert'),
    path('transport-roadmap-edit/<slug:id>', transport_roadmap_edit, name='transport-roadmap-edit'),
    
    path('transport-roadmap-dtl', transport_roadmapdtl_info.as_view(),name='transport-roadmap-dtl'),
    path('transport-roadmapdtl-insert',transport_roadmapdtl_insert,name='transport-roadmapdtl-insert'),
    path('transport-roadmapdtl-edit/<slug:id>', transport_roadmapdtl_edit, name='transport-roadmapdtl-edit'),
    
    path('transport-admit-transportation', transport_admit_transportation.as_view(),name='transport-admit-transportation'),
    path('transport-admit-transportation-insert',transport_admit_transportation_insert,name='transport-admit-transportation-insert'),
    path('transport-admit-transportation-edit/<slug:id>', transport_admit_transportation_edit, name='transport-admit-transportation-edit'),
    
    path('transport-payfor-type', transport_payfor_type.as_view(),name='transport-payfor-type'),
    path('transport-payfor-type-insert',transport_payfor_type_insert,name='transport-payfor-type-insert'),
    path('transport-payfor-type-edit/<slug:id>', transport_payfor_type_edit, name='transport-payfor-type-edit'),
    
    path('transport-payment-management', transport_payment_management.as_view(),name='transport-payment-management'),
    path('transport-payment-management-insert',transport_payment_management_insert,name='transport-payment-management-insert'),
    path('transport-payment-management-edit/<slug:id>', transport_payment_management_edit, name='transport-payment-management-edit'),
    
    path('transport-student-attendance', transport_student_attendance.as_view(), name='transport-student-attendance'),
    path('transport-student-list-ajax', transport_student_list_ajax, name='transport-student-list-ajax'),
    path('transport-student-attendance-insert', transport_student_attendance_insert, name='transport-student-attendance-insert'),
    path('transport-use-summery', transport_use_summery.as_view(), name='transport-use-summery'),
    path('transport-use-summery-edit/<slug:id>', transport_use_summery_edit, name='transport-use-summery-edit'),
    path('transport-quick-drop/<slug:id>', transport_quick_drop, name='transport-quick-drop'),

]