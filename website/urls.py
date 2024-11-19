from django.urls import path
from . import views

##### For Image Upload
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('', home_page.as_view() ,name='home-page'),
    path('page/<slug:url_slug>', get_page.as_view() ,name='get-page'),
    path('view-all-form', all_pdf_form.as_view() ,name='view-all-form'),
    path('listof-employee', listof_employee.as_view() ,name='listof-employee'),
    


    

    # Backend Url
    path('websitebackend-create-page', Page_create_form.as_view() ,name='websitebackend-create-page'),
    path('websitebackend-create-page-insert', Page_create_insert ,name='websitebackend-create-page-insert'),
    path('websitebackend-update-page', page_update_form ,name='websitebackend-update-page'),
    path('websitebackend-pages-list', Page_list ,name='websitebackend-pages-list'),

   
    path('websitebackend-pdf-list', notic_pdf_list.as_view(), name='websitebackend-pdf-list'),

    
    #Image_Carousel
    path('websitebackend-image-carousel-create', image_carousel_create.as_view(), name='websitebackend-image-carousel-create'),
    path('websitebackend-image-carousel-insert', image_carousel_insert, name='websitebackend-image-carousel-insert'), 
    path('websitebackend-image-carousel-edit/<slug:id>', image_carousel_edit, name='websitebackend-image-carousel-edit'),
    path('websitebackend-image-carousel-delete/<slug:id>', image_carousel_delete, name='websitebackend-image-carousel-delete'),
    #Navbar_Menu
    path('websitebackend-navbar-menu-create', navbar_menu_create.as_view(), name='websitebackend-navbar-menu-create'),
    path('websitebackend-navbar-menu-insert', navbar_menu_insert, name='websitebackend-navbar-menu-insert'),
    path('websitebackend-navbar-menu-edit/<slug:id>', navbar_menu_edit, name='websitebackend-navbar-menu-edit'),
    path('websitebackend-navbar-menu-delete/<slug:id>', navbar_menu_delete, name='websitebackend-navbar-menu-delete'),
    #Navbar_Sub_Menu
    path('websitebackend-navbar-sub-menu-create', navbar_sub_menu_create.as_view(), name='websitebackend-navbar-sub-menu-create'),
    path('websitebackend-navbar-sub-menu-insert', navbar_sub_menu_insert, name='websitebackend-navbar-sub-menu-insert'),
    path('websitebackend-navbar-sub-menu-edit/<slug:id>', navbar_sub_menu_edit, name='websitebackend-navbar-sub-menu-edit'),
    path('websitebackend-navbar-sub-menu-delete/<slug:id>', navbar_sub_menu_delete, name='websitebackend-navbar-sub-menu-delete'),

    #Notic_Uplode
    path('websitebackend-upload-pdf-create', notic_upload_pdf_create.as_view(), name='websitebackend-upload-pdf-create'),
    path('websitebackend-upload-pdf-insert', notic_upload_pdf_insert, name='websitebackend-upload-pdf-insert'),
    path('websitebackend-upload-pdf-edit/<slug:id>', upload_pdf_edit, name='websitebackend-upload-pdf-edit'),
    
    #Importent Link
    path('websitebackend-importent-link-create', importent_link_create.as_view(), name='websitebackend-importent-link-create'),
    path('websitebackend-importent-link-insert', importent_link_insert, name='websitebackend-importent-link-insert'),
    path('websitebackend-importent-link-edit/<slug:id>', importent_link_edit, name='websitebackend-importent-link-edit'),
    path('websitebackend-importent-link-delete/<slug:id>',importent_link_delete, name='websitebackend-importent-link-delete'),

]   



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    