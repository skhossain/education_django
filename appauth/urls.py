from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
     path('appauth/', HomeView.as_view(), name='appauth'),
     path('software/home', HomeView.as_view(), name=''),
     path('appauth-home/', appauth_home, name='appauth-home'),
     path('appauth-login', login_view, name='appauth-login'),  
     path('appauth-logout/', logout_view, name='appauth-logout'),
     path('appauth-reset-password/', reset_password.as_view(), name='appauth-reset-password'),
     path('appauth-reset-passwordpost', reset_user_password, name='appauth-reset-passwordpost'),
     path('appauth-reset-userspassword', reset_appuser_password, name='appauth-reset-userspassword'),
     path("appauth-dashboard", DashboardView, name='appauth-dashboard'),
     path("appauth-dashboard-data", appauth_dashboard_data, name='appauth-dashboard-data'),
     path('appauth-user-create', CreateUser.as_view() , name ='appauth-user-create'),
     path('appauth-application-users', ApplicationUserList.as_view(), name='appauth-application-users'),
     path('appauth-appuser-update/<int:id>', appauth_appuser_update, name='appauth-appuser-update'),
     path('appauth-branch-createlist', appauth_branch_view.as_view(), name='appauth-branch-createlist'),
     path('appauth-branch-insert', appauth_branch_insert, name='appauth-branch-insert'),
     path('appauth-branch-edit/<slug:id>', appauth_branch_edit, name='appauth-branch-edit'),
     path('appauth-country-createlist', appauth_country_view.as_view(), name='appauth-country-createlist'),
     path('appauth-country-insert', appauth_country_insert, name='appauth-country-insert'),
     path('appauth-country-edit/<slug:id>', appauth_country_edit, name='appauth-country-edit'),
     path('appauth-employee-createlist', appauth_employee_view.as_view(), name='appauth-employee-createlist'),
     path('appauth-employee-insert', appauth_employee_insert, name='appauth-employee-insert'),
     path('appauth-employee-edit/<slug:id>', appauth_employee_edit, name='appauth-employee-edit'),
     path('appauth-get-employeedetails', fn_get_employee_details_view, name='appauth-get-employeedetails'),
     path('appauth-choice-employeelist/', appauth_choice_employeelist, name='appauth-choice-employeelist'),
     path('appauth-choice-branchlist/', appauth_choice_branchlist, name='appauth-choice-branchlist'),
     path('appauth-choice-appuserlist/', appauth_choice_appuserlist, name='appauth-choice-appuserlist'),
     path('appauth-report-submit/', appauth_report_submit, name='appauth-report-submit'),
     path('appauth-director-createlist', appauth_director_view.as_view(), name='appauth-director-createlist'),
     path('appauth-director-insert', appauth_director_insert, name='appauth-director-insert'),
     path('appauth-director-edit/<slug:id>', appauth_director_edit, name='appauth-director-edit'),
     path('appauth-country-createlist', appauth_country_view.as_view(), name='appauth-country-createlist'),
     path('appauth-country-insert', appauth_country_insert, name='appauth-country-insert'),
     path('appauth-country-edit/<slug:id>', appauth_country_edit, name='appauth-country-edit'),
     path('appauth-division-createlist', appauth_division_view.as_view(), name='appauth-division-createlist'),
     path('appauth-division-insert', appauth_division_insert, name='appauth-division-insert'),
     path('appauth-division-edit/<slug:id>', appauth_division_edit, name='appauth-division-edit'),
     path('appauth-district-createlist', appauth_disrict_view.as_view(), name='appauth-district-createlist'),
     path('appauth-district-insert', appauth_district_insert, name='appauth-district-insert'),
     path('appauth-district-edit/<slug:id>', appauth_district_edit, name='appauth-district-edit'),
     path('appauth-upazila-createlist', appauth_upazila_view.as_view(), name='appauth-upazila-createlist'),
     path('appauth-upazila-insert', appauth_upazila_insert, name='appauth-upazila-insert'),
     path('appauth-upazila-edit/<slug:id>', appauth_upazila_edit, name='appauth-upazila-edit'),
     path('appauth-union-createlist', appauth_union_view.as_view(), name='appauth-union-createlist'),
     path('appauth-union-insert', appauth_union_insert, name='appauth-union-insert'),
     path('appauth-union-edit/<slug:id>', appauth_union_edit, name='appauth-union-edit'),
     path('appauth-choice-reportlist/', appauth_choice_reportlist, name='appauth-choice-reportlist'),
     path("appauth-getreport-url", appauth_get_report_url,name='appauth-getreport-url'),
]

#### For Image Upload
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
