from django.shortcuts import render
from django.views.generic import TemplateView
# App Auth
from itertools import count
import threading
from appauth.views import get_global_data
from appauth.utils import fn_get_query_result
from appauth.forms import *
import time
import os
# from turtle import position
#Edu app
from edu.models import *
from edu.forms import *
#Studentportal app
from .models import *
# from forms import *
all_permissions = {}
# Create your views here.
def get_gobale_edu_data(request):
    appinfo= Application_Settings.objects.filter().first()
    context = get_global_data(request)
    context['academic_name']=appinfo.academic_name
    context['academic_address']=appinfo.academic_address
    context['academic_mobile_1']=appinfo.academic_mobile_1
    context['academic_mobile_2']=appinfo.academic_mobile_2
    context['academic_email']=appinfo.academic_email
    context['eiin_number']=appinfo.eiin_number
    if appinfo.academic_logo:
        context['academic_logo']=appinfo.academic_logo.url
    return context

class wellcome(TemplateView):
    template_name = 'studentportal/studentportal-welcome.html'

    def get(self, request):
        context = get_gobale_edu_data(request)
        print(type(context))
        
        return render(request, self.template_name,context)

class admission(TemplateView):
    template_name = 'studentportal/studentportal-admission-info.html'

    def get(self, request):
        education_branchs=Education_Branch.objects.all()
        branch_codes=[]
        for code in education_branchs:
            branch_codes.append(code.branch_code)
        branchs=Branch.objects.filter(branch_code__in=branch_codes)
        context = get_gobale_edu_data(request) 
        context['branchs']=branchs       
        return render(request, self.template_name,context)

class admission_form(TemplateView):
    template_name = 'studentportal/studentportal-admission.html'

    def get(self, request):
        education_branchs=Education_Branch.objects.all()
        branch_codes=[]
        for code in education_branchs:
            branch_codes.append(code.branch_code)
        branchs=Branch.objects.filter(branch_code__in=branch_codes)
        context = get_gobale_edu_data(request) 
        context['branchs']=branchs       
        return render(request, self.template_name,context)

