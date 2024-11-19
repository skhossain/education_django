from django.urls import path

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('apiauth-department-api',departmentApiView.as_view()),
    path('apihrm-designation-api',designationApiView.as_view()),
    path('apihtm-companyInfo-api',companyInfoApiView.as_view()),
    path('apihrm-officeInfo-api',OfficeInfoApiView.as_view()),
    path('apihrm-shiftInfo-api',ShiftInfoApiView.as_view()),
    path('apiauth-emp-degree-api',EmployeeDegreeApiView.as_view()),
    path('apihrm-employeeType-api',EmployeeTypeApiView.as_view()),
    path('apihrm-salaryScaleType-api',SalaryScaleTypeApiView.as_view()),
    path('apihrm-salaryScale-details-api',SalaryScaleDetailasTypeApiView.as_view()),
    path('apihrm-salaryBonus-api',SalaryBonusApiView.as_view()),
    path('apihrm-extra-alownace-api',ExtraAlownceApiView.as_view()),
    path('apihrm-Bank-api',BankTypeApiView.as_view()),    
    path('apihrm-employee-api',EmployeeINfoApiView.as_view()),
    path('apihrm-employeeExperiance-api',EmployeeExperianceApiView.as_view()),
    path('apihrm-employeeExperience-create-api', EmployeeExperienceCreateApiView.as_view()),
    path('apihrm-employeeEducation-create-api',
         EmployeeEducationCreateApiView.as_view()),
    path('apihrm-employeeExperience-edit-api/<slug:id>', EmployeeExperienceEditApiView.as_view()),
    path('apihrm-employeeEducation-edit-delete-api/<slug:id>',EmpEducationEditDeleteApiView.as_view()),
    path('apihrm-empNominee-api',EmployeeNomineeApiView.as_view()),
    path('apihrm-empDocument-api',EmployeeDocumentApiView.as_view()),
    path('apihrm-documentType-api',DocumentTypeApiView.as_view() ),
    path('apihrm-LeaveInfo-api',EmpLeaveInfoApiView.as_view() ),
    path('apihrm-LeaveInfoApplication-api',EmpLeaveApplicationApiView.as_view()),
    path('apihrm-trainingInfo-api',EmpTrainingInfoApiView.as_view()),
    path('apihrm-payBill-api',PayBillApiView.as_view())
]
