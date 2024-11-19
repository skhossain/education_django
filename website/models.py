from django.db import models
# from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
STATUS=(
    (0,'Inactive'),
    (1,'Active')
)

TYPE_PDF=(
    (0,"Notic"),
    (1,"From Downloade")
    
)

class Education_Lavel(models.Model):
    lavel_name = models.CharField(max_length=30,null=True,blank=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.lavel_name)


class Page_Create(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    title=models.CharField(max_length=200)
    url_slug=models.CharField(max_length=200,null=True,blank=True)
    content = RichTextUploadingField()
    view_count=models.IntegerField(default=0)
    status=models.IntegerField(default=0,choices=STATUS)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.title)
    


class Notic_Bord(models.Model):
    branch_code = models.IntegerField(blank=True, null=True)
    notic_title = models.CharField(max_length=500,blank=True,null=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    status=models.IntegerField(default=0,choices=STATUS)
    education_lavel=models.ForeignKey(Education_Lavel,on_delete=models.CASCADE,default=1,related_name='notic_education_lavel')
    types=models.IntegerField(default=0,choices=TYPE_PDF)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notic_title
    

class Image_Carousel(models.Model):
    title1= models.CharField(max_length=200,blank=True,null=True)
    title2= models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    status=models.IntegerField(default=0,choices=STATUS)
    button_lavel=models.CharField(max_length=100,blank=True,null=True)
    button_url=models.CharField(max_length=100,blank=True,null=True)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title1

class Navbar_Menu(models.Model):
    menu_lavel=models.CharField(max_length=200,blank=True,null=True)
    menu_url=models.CharField(max_length=200,blank=True,null=True)
    serial = models.DecimalField(default=999,decimal_places=2,max_digits=6)
    status=models.IntegerField(default=0,choices=STATUS)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.menu_lavel

class Navbar_Sub_Menu(models.Model):
    navbar_lavel=models.ForeignKey(Navbar_Menu,on_delete=models.CASCADE,default=1,related_name='nsm_navbar_lavel')
    menu_lavel=models.CharField(max_length=200,blank=True,null=True)
    menu_url=models.CharField(max_length=200,blank=True,null=True)
    serial = models.DecimalField(default=999, decimal_places=2,max_digits=6)
    status=models.IntegerField(default=0,choices=STATUS)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['serial']
    
    def __str__(self):
        return self.menu_lavel
    

class Footer_Link(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    link = models.CharField(max_length=200,blank=True,null=True)
    status=models.IntegerField(default=0,choices=STATUS)
    app_user_id = models.CharField(max_length=20, null=False, blank=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    

    
