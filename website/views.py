from appauth.views import get_global_data
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from edu.models import Application_Settings as Academic_Info
from hrm.models import Employee_Details
from .forms import *
from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
import sys
import logging
logger = logging.getLogger(__name__)

def get_website_global(request):
    try:
        condition = Q(designation_id__desig_name='অধ্যক্ষ') | Q(designation_id__desig_name='Principal') | Q(designation_id__desig_name='principal')
        principal_info=get_object_or_404(Employee_Details,condition)
        notices=Notic_Bord.objects.filter(status=1).order_by('-app_data_time')
        edu_lavel=Education_Lavel.objects.filter()
        academic_info=get_object_or_404(Academic_Info)
        img_carousel=Image_Carousel.objects.all()
        navbar_menu=Navbar_Menu.objects.filter(status=1).order_by('serial')
        footer_link=Footer_Link.objects.all()
    except Exception as e:
        return render(request, 'appauth/appauth-login.html')

    context = {
        'notices':notices,
        'edu_lavels':edu_lavel,
        'principal_info':principal_info,
        'academic_info':academic_info,
        'img_carousel':img_carousel,
        'navbar_menu':navbar_menu,
        'footer_link':footer_link
    }
    return context
# Create your views here.
class home_page(TemplateView):
    template_name = 'website/website-home.html'
    def get(self, request):
        
        home=Page_Create.objects.filter(url_slug='home')
        data=get_website_global(request)
        data['home']=home
        return render(request, self.template_name,data)

class get_page(TemplateView):
    template_name = 'website/website-page.html'
    def get(self, request,url_slug):
        home=Page_Create.objects.filter(url_slug=url_slug)
        data=get_website_global(request)
        data['home']=home
        return render(request, self.template_name,data)

class all_pdf_form(TemplateView):
      template_name = 'website/website-all-form-list.html'

      def get(self, request):
           notices=Notic_Bord.objects.filter(status=1).order_by('-app_data_time')
           data=get_website_global(request)
           data['download_links']=notices
           return render(request, self.template_name,data)



class listof_employee(TemplateView):
     template_name = 'website/website-listof_employee.html'

     def get(self, request):
           emp_list=Employee_Details.objects.filter().values('serial','profile_image','employee_name','designation_id','employee_phone_office','email_official').order_by('serial')
           paginator = Paginator(emp_list, 10)
           page_number = request.GET.get('page',1)
           pages = paginator.get_page(page_number)
           profile_image=Employee_Details.objects.all()
           data=get_website_global(request)
           data['pages']=pages
           data['profile_image']=profile_image
           return render(request, self.template_name,data)
     
  
     


# Backend Function
class Page_create_form(TemplateView):
    template_name = 'websitebackand/websitebackand-create-page.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form=WebsiteBackand_Page_create_Form()
        context = get_global_data(request)
        context['form']=form
        return render(request, self.template_name,context)

@transaction.atomic
def Page_create_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'websitebackand/websitebackand-create-page.html'
    data = get_global_data(request)
    if request.method == "POST":
        form = WebsiteBackand_Page_create_Form(request.POST)
        data['form'] = form
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    update=request.POST.get('update',None)
                    post = form.save(commit=False)
                    post.app_user_id=app_user_id
                    if(not Page_Create.objects.filter(url_slug=post.url_slug).exists()):
                        post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = "Save Success"
                        data['update']=True
                        data['page_id']=post.pk
                    elif update:
                        page_id=request.POST.get('page_id',None)
                        instance_data = get_object_or_404(Page_Create, pk=page_id)
                        form = WebsiteBackand_Page_create_Form(request.POST, instance=instance_data)
                        post = form.save(commit=False)
                        post.id=page_id
                        post.save()
                        data['form_is_valid'] = True
                        data['success_message'] = "Save Success"
                        data['update']=True
                        data['page_id']=page_id
                    else:
                        data['form_is_valid'] = False
                        data['error_message'] = "Url/Link duplicated."
                    return render(request, template_name,data)
                    
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return render(request, template_name,data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = form.errors.as_json()
            return render(request, template_name,data)

def page_update_form(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    template_name = 'websitebackand/websitebackand-create-page.html'
    data = get_global_data(request)
    page_id=request.POST.get('page_id',None)
    if page_id:
        inst=get_object_or_404(Page_Create,pk=page_id)
        if(inst):
            form = WebsiteBackand_Page_create_Form(instance=inst)
            data['form']=form
            data['page_id']=page_id
            data['update']=True
    return render(request, template_name,data)

def Page_list(request):
    template_name = 'websitebackand/websitebackand-page-list.html'
    
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
        
    context = get_global_data(request)
    if request.method == "POST":
        branch_code=request.POST.get('branch_code',None)
        title=request.POST.get('title',None)
        status=request.POST.get('status',None)
        pages=Page_Create.objects.filter(branch_code=branch_code,status=status)
        
        if title:
            pages.filter(title=title)    
        
        form=WebsiteBackand_Page_create_Form(initial={'branch_code':branch_code,'title':title,'status': 1})
        form.fields['title'].required = False
        
        context['pages']=pages
    else:
        form=WebsiteBackand_Page_create_Form(initial={'status': 1})
        form.fields['title'].required = False
    context['form']=form
    return render(request, template_name,context)





class notic_upload_pdf_create(TemplateView):
    template_name = 'websitebackand/websitebackand_notic_upload_pdf.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form =  Notic_BordForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    



@transaction.atomic
def notic_upload_pdf_insert(request):
        if not request.user.is_authenticated:
                return render(request, 'appauth/appauth-login.html')

        if request.method == 'POST': 
            data = dict()
            data['form_is_valid'] = False
            form=Notic_BordForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                form = Notic_BordForm()
                context = get_global_data(request)
                context['form'] = form
                context['success'] = 'PDF added successfully.'
                return render(request,'websitebackand/websitebackand_notic_upload_pdf.html',context)
        
        else:
            form = Notic_BordForm()
            context = get_global_data(request)
            context['form'] = form
            return render(request,'websitebackand/websitebackand_notic_upload_pdf.html',{'form':form})

       
@transaction.atomic
def upload_pdf_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Notic_Bord,id=id)
    template_name = 'websitebackand/websitebackand_upload_pdf_edit.html'
    data = dict()
    if request.method == "POST":
        form = Notic_BordForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    obj = form.save(commit=False)
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = forms.errors.as_json()
            return JsonResponse(data)

    else:
        form= Notic_BordForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)
    





class notic_pdf_list(TemplateView):
     template_name = 'websitebackand/websitebackand_notice-pdf-list.html'

     def get(self, request):
           data_list=Notic_Bord.objects.filter()
           paginator = Paginator(data_list, 10)
           page_number = request.GET.get('page',1)
           pages = paginator.get_page(page_number)
           form =  Notic_BordForm()
           data=get_global_data(request)
           data['pages']=pages
           data['form']=form
           return render(request, self.template_name,data)
    


# Image_Carousel
class image_carousel_create(TemplateView):
    template_name = 'websitebackand/websitebackand_image_carousel.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Image_CarouselForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    



@transaction.atomic
def image_carousel_insert(request):
        if not request.user.is_authenticated:
                return render(request, 'appauth/appauth-login.html')

        if request.method == 'POST': 
            data = dict()
            data['form_is_valid'] = False
            form=Image_CarouselForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data['form_is_valid'] = True
                form = Image_CarouselForm()
                context = get_global_data(request)
                context['form'] = form
                context['success'] = 'Image added successfully.'
                return render(request,'websitebackand/websitebackand_image_carousel.html',context)
        
        else:
            form =Image_CarouselForm()
            context = get_global_data(request)
            context['form'] = form
            return render(request,'websitebackand/websitebackand_image_carousel.html',{'form':form})
        
@transaction.atomic
def image_carousel_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Image_Carousel,id=id)
    template_name = 'websitebackand/websitebackand_image_carousel_edit.html'
    data = dict()
    if request.method == "POST":
        form = Image_CarouselForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    obj = form.save(commit=False)
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = forms.errors.as_json()
            return JsonResponse(data)

    else:
        form= Image_CarouselForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)
    
    
    
    
@transaction.atomic
def image_carousel_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == "POST":
        try:
        
            Image_Carousel.objects.get(id=id).delete()
            data['form_is_valid'] = True
            data['success_message'] = "Delete Successfully!"
        except Exception as e:
            data['error_message'] = str(e)
            data['form_is_valid'] = False
        return JsonResponse(data)



# Navbar_Menu
class navbar_menu_create(TemplateView):
    template_name = 'websitebackand/websitebackand_navbar_menu.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Navbar_MenuForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    

@transaction.atomic
def navbar_menu_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""

    try:
        if request.method == 'POST':
            form = Navbar_MenuForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        app_user_id = request.session["app_user_id"]
                        post = form.save(commit=False)
                        post.app_user_id = app_user_id
                        post.save()
                        message = "Added Successfully!"
                        data['success_message'] = message
                        data['form_is_valid'] = True
                        return JsonResponse(data)
                except Exception as e:
                    data['form_is_valid'] = False
                    data['error_message'] = str(e)
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            else:
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
        else:
            message = "Post Request Error!"
            data['error_message'] = message
            data['form_is_valid'] = False
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)


@transaction.atomic
def navbar_menu_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Navbar_Menu,id=id)
    template_name = 'websitebackand/websitebackand_navbar_menu_edit.html'
    data = dict()
    if request.method == "POST":
        form = Navbar_MenuForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    obj = form.save(commit=False)
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            form =Navbar_MenuForm()
            context = get_global_data(request)
            context['form'] = form
            return render(request,'websitebackand/websitebackand_navbar_menu.html',{'form':form})
        
@transaction.atomic
def navbar_menu_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == "POST":
        try:
        
           Navbar_Menu.objects.get(id=id).delete()
           data['form_is_valid'] = True
           data['success_message'] = "Delete Successfully!"
        except Exception as e:
            data['error_message'] = str(e)
            data['form_is_valid'] = False
        return JsonResponse(data)

# Navbar_Sub_Menu
class navbar_sub_menu_create(TemplateView):
    template_name = 'websitebackand/websitebackand_navbar_sub_menu.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form =  Navbar_Sub_MenuForm()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    

@transaction.atomic
def navbar_sub_menu_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""

    try:
        if request.method == 'POST':
            form = Navbar_Sub_MenuForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        app_user_id = request.session["app_user_id"]
                        post = form.save(commit=False)
                        post.app_user_id = app_user_id
                        post.save()
                        message = "Added Successfully!"
                        data['success_message'] = message
                        data['form_is_valid'] = True
                        return JsonResponse(data)
                except Exception as e:
                    data['form_is_valid'] = False
                    data['error_message'] = str(e)
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            else:
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
        else:
            message = "Post Request Error!"
            data['error_message'] = message
            data['form_is_valid'] = False
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)
    

@transaction.atomic
def navbar_sub_menu_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Navbar_Sub_Menu,id=id)
    template_name = 'websitebackand/websitebackand_navbar_sub_menu_edit.html'
    data = dict()
    if request.method == "POST":
        form = Navbar_Sub_MenuForm(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    obj = form.save(commit=False)
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = forms.errors.as_json()
            return JsonResponse(data)

    else:
        form= Navbar_Sub_MenuForm(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)
    
    
    
    
@transaction.atomic
def navbar_sub_menu_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == "POST":
        try:
        
            Navbar_Sub_Menu.objects.get(id=id).delete()
            data['form_is_valid'] = True
            data['success_message'] = "Delete Successfully!"
        except Exception as e:
            data['error_message'] = str(e)
            data['form_is_valid'] = False
        return JsonResponse(data)



# importent Link
class importent_link_create(TemplateView):
    template_name = 'websitebackand/websitebackand_importent_link.html'

    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'appauth/appauth-login.html')
        form = Importent_Link_Form()
        context = get_global_data(request)
        context['form'] = form
        return render(request, self.template_name, context)
    

@transaction.atomic
def importent_link_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    data['error_message'] = ""

    try:
        if request.method == 'POST':
            form = Importent_Link_Form(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        app_user_id = request.session["app_user_id"]
                        post = form.save(commit=False)
                        post.app_user_id = app_user_id
                        post.save()
                        message = "Added Successfully!"
                        data['success_message'] = message
                        data['form_is_valid'] = True
                        return JsonResponse(data)
                except Exception as e:
                    data['form_is_valid'] = False
                    data['error_message'] = str(e)
                    logger.error("Error on line {} \nType: {} \nError:{}".format(
                        sys.exc_info()[-1], type(e).__name__, str(e)))
                    return JsonResponse(data)
            else:
                data['error_message'] = form.errors.as_json()
                return JsonResponse(data)
        else:
            message = "Post Request Error!"
            data['error_message'] = message
            data['form_is_valid'] = False
            return JsonResponse(data)
    except Exception as e:
        data['error_message'] = str(e)
        return JsonResponse(data)
    

@transaction.atomic
def importent_link_edit(request,id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    instance_data = get_object_or_404(Footer_Link,id=id)
    template_name = 'websitebackand/websitebackand_importent_link_edit.html'
    data = dict()
    if request.method == "POST":
        form = Importent_Link_Form(request.POST, instance=instance_data)
        data['form_error'] = form.errors.as_json()
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    obj = form.save(commit=False)
                    obj.app_user_id = app_user_id
                    obj.save()
                    data['success_message'] = "Updated Successfully!"
                    data['error_message'] = ''
                    data['form_is_valid'] = True
                    return JsonResponse(data)
            except Exception as e:
                data['form_is_valid'] = False
                data['error_message'] = str(e)
                return JsonResponse(data)
        else:
            data['form_is_valid'] = False
            data['error_message'] = forms.errors.as_json()
            return JsonResponse(data)

    else:
        form= Importent_Link_Form(instance=instance_data)
        context = get_global_data(request)
        context['form'] = form
        context['id'] = id
        data['html_form'] = render_to_string(
            template_name, context, request=request
        )
        return JsonResponse(data)
    
    
    
    
@transaction.atomic
def importent_link_delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'appauth/appauth-login.html')
    data = dict()
    data['form_is_valid'] = False
    if request.method == "POST":
        try:
        
            Footer_Link.objects.get(id=id).delete()
            data['form_is_valid'] = True
            data['success_message'] = "Delete Successfully!"
        except Exception as e:
            data['error_message'] = str(e)
            data['form_is_valid'] = False
        return JsonResponse(data)
