from logging import exception
from pyexpat import model
from django import forms
from crispy_forms.layout import Field
from django.forms import ModelForm, TextInput, Select, Textarea, IntegerField, ChoiceField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import *
from ckeditor.widgets import CKEditorWidget
class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass

class WebsiteBackand_Page_create_Form(forms.ModelForm):
    branch_code = ChoiceFieldNoValidation(label="Branch Name", required=False)
    # product_id = ChoiceFieldNoValidation(label="Product Name", required=True)

    def __init__(self, *args, **kwargs):
        super(WebsiteBackand_Page_create_Form, self).__init__(*args, **kwargs)

    class Meta:
        model = Page_Create
        fields = ['branch_code','title','url_slug','content','status']

        widgets = {
        #     'comments': Textarea(attrs={'rows': 2, 'cols': 60, }),
        #     'expence_date': DateInput(),
        'content': CKEditorWidget(attrs={'id':'id_page_content'})
        }

        labels = {
            "title": _("Page Title"),
            "url_slug": _("Page Url/Link"),
            "content": _("Page Content"),
            "status": _("Page Status"),
        }
        

class Notic_BordForm(forms.ModelForm):
    class Meta:
        model =Notic_Bord
        fields = ('branch_code','notic_title', 'pdf_file','status','education_lavel','types')

        labels = {
            "branch_code":_("Branch Name"),
            "notic_title":_("Notic Title"),
            "pdf_file":_("PDF FILE"),
            "status":_("Status")
        }

class Image_CarouselForm(forms.ModelForm):
    class Meta:
        model =Image_Carousel
        fields = ('title1','title2','image','status','button_lavel','button_url')

        labels={
            "title1":_("Title1"),
            "title2":_("Title2"),
            "image":_("Image"),
            "status":_("Status"),
            "button_lavel":_("Button_Lavel"),
            "button_url":_("Button_Url")
        }

class Navbar_MenuForm(forms.ModelForm):
    class Meta:
        model =Navbar_Menu
        fields = ('menu_lavel','menu_url','serial','status')

        labels={
            "menu_lavel":_("Menu Lavel"),
            "menu_url":_("Menu Url"),
            "serial":_("Serial"),
            "status":_("Status")
            
            
        }

class Navbar_Sub_MenuForm(forms.ModelForm):
    class Meta:
        model =Navbar_Sub_Menu
        fields =('navbar_lavel','menu_lavel','menu_url','serial','status')

        labels={
            "navbar_lavel":_("Navbar Lavel"),
            "menu_lavel":_("Menu Lavel"),
            "serial":_("Serial"),
            "menu_url":_("Menu Url"),
            "status":_("Status")
            
        }

class Importent_Link_Form(forms.ModelForm):
    class Meta:
        model =Footer_Link
        fields =('title','link','status')

        labels={
            "title":_("Title"),
            "link":_("Link"),
            "status":_("Status")
            
        }