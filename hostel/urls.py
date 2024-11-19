from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('hostel-bedtype-createlist', hostel_bedtype_createlist.as_view() ,name='hostel-bedtype-createlist'),
    path('hostel-bedtype-insert', hostel_bedtype_insert ,name='hostel-bedtype-insert'),
    path('hostel-bedtype-edit/<slug:id>', hostel_bedtype_edit ,name='hostel-bedtype-edit'),

    path('hostel-payfortype-createlist', hostel_payfortype_createlist.as_view() ,name='hostel-payfortype-createlist'),
    path('hostel-payfortype-insert', hostel_payfortype_insert ,name='hostel-payfortype-insert'),
    path('hostel-payfortype-edit/<slug:id>', hostel_payfortype_edit ,name='hostel-payfortype-edit'),

    path('hostel-bedmanagement-createlist', hostel_bedmanagement_createlist.as_view() ,name='hostel-bedmanagement-createlist'),
    path('hostel-bedmanagement-insert', hostel_bedmanagement_insert ,name='hostel-bedmanagement-insert'),
    path('hostel-bedmanagement-edit/<slug:id>', hostel_bedmanagement_edit ,name='hostel-bedmanagement-edit'),

    path('hostel-roommanagement-createlist', hostel_roommanagement_createlist.as_view() ,name='hostel-roommanagement-createlist'),
    path('hostel-roommanagement-insert', hostel_roommanagement_insert ,name='hostel-roommanagement-insert'),
    path('hostel-roommanagement-edit/<slug:id>', hostel_roommanagement_edit ,name='hostel-roommanagement-edit'),

    path('hostel-paymentmanage-createlist', hostel_paymentmanage_createlist.as_view() ,name='hostel-paymentmanage-createlist'),
    path('hostel-paymentmanage-insert', hostel_paymentmanage_insert ,name='hostel-paymentmanage-insert'),
    path('hostel-paymentmanage-edit/<slug:id>', hostel_paymentmanage_edit ,name='hostel-paymentmanage-edit'),

    path('hostel-admission-createlist', hostel_admission_createlist.as_view() ,name='hostel-admission-createlist'),
    path('hostel-admission-insert', hostel_admission_insert ,name='hostel-admission-insert'),
    path('hostel-admission-cancel/<slug:id>', hostel_admission_cancel ,name='hostel-admission-cancel'),
    path('hostel-admission-edit/<slug:id>', hostel_admission_edit ,name='hostel-admission-edit'),

    path('hostel-addingmeal-createlist', hostel_addingmeal_createlist.as_view() ,name='hostel-addingmeal-createlist'),
    path('hostel-addingmeal-insert', hostel_addingmeal_insert ,name='hostel-addingmeal-insert'),
    path('hostel-addmeal-edit/<slug:id>', hostel_addmeal_edit ,name='hostel-addmeal-edit'),

    # path('hostel-admissionroll-select2', hostel_admissionroll_select2 ,name='hostel-admissionroll-select2'),

    path('hostel-mealtype-createlist', hostel_mealtype_createlist.as_view(), name='hostel-mealtype-createlist'),
    path('hostel-mealtype-insert', hostel_mealtype_insert, name='hostel-mealtype-insert'),
    path('hostel-mealtype-edit/<slug:id>', hostel_mealtype_edit, name='hostel-mealtype-edit'),

    path('hostel-meal-createlist', hostel_meal_createlist.as_view(), name='hostel-meal-createlist'),
    path('hostel-meal-insert', hostel_meal_insert, name='hostel-meal-insert'),
    path('hostel-meal-edit/<slug:id>', hostel_meal_edit, name='hostel-meal-edit'),

    path('hostel-dailymeal-createlist', hostel_dailymeal_createlist.as_view(), name='hostel-dailymeal-createlist'),
    path('hostel-dailymeal-filterlist', hostel_dailymeal_filterlist, name='hostel-dailymeal-filterlist'),
    path('hostel-dailymeal-insert', hostel_dailymeal_insert, name='hostel-dailymeal-insert'),

    path('hostel-dailymeal-studentlist',hostel_dailymeal_studentlist.as_view(), name='hostel-dailymeal-studentlist'),
    path('hostel-dailymeal-studentfilterlist',hostel_dailymeal_studentfilterlist, name='hostel-dailymeal-studentfilterlist'),
    path('hostel-dailymeal-search-cancel',hostel_dailymeal_search_cancel, name='hostel-dailymeal-search-cancel'),
    path('hostel-dailymeal-cancel',hostel_dailymeal_cancel, name='hostel-dailymeal-cancel'),
    path('hostel-dailymeal-shortsummary',hostel_dailymeal_shortsummary, name='hostel-dailymeal-shortsummary'),
    path('hostel-hall-createlist', hostel_hall_createlist.as_view(),name='hostel-hall-createlist'),
    path('hostel-hall-insert',hostel_hall_insert,name='hostel-hall-insert'),
    path('hostel-hall-edit/<slug:id>', hostel_hall_edit, name='hostel-hall-edit'),
    path('hostel-hall-delete/<slug:id>', hostel_hall_delete, name='hostel-hall-delete'),

    path('hostel-feesmapping-createlist', hostel_feesmapping_createlist.as_view(),name='hostel-feesmapping-createlist'),
    path('hostel-feesmapping-insert',hostel_feesmapping_insert,name='hostel-feesmapping-insert'),
    path('hostel-feesmapping-edit/<slug:id>', hostel_feesmapping_edit, name='hostel-feesmapping-edit'),
    path('hostel-feesmapping-delete/<slug:id>', hostel_feesmapping_delete, name='hostel-feesmapping-delete'),

    path('hostel-fees-processing',hostel_fees_processing.as_view(),name='hostel-fees-processing'),
    path('hostel-fees-processing-insert', hostel_fees_processing_insert,name='hostel-fees-processing-insert'),
    
]