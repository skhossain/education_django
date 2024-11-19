from django.shortcuts import render
from rest_framework import generics
from django.views.generic import TemplateView, ListView
from .serializers import *
from website.models import *

# Create your views here.

class imagecarouselApiView(generics.ListAPIView):

    serializer_class = ImageCarouselSerializer
    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        

        queryset =Image_Carousel.objects.filter().order_by('id')

        if id:
            queryset = queryset.filter(id=id)

        return queryset
    
class  Notic_Upload_Pdf_Api(generics.ListAPIView):

    serializer_class = NoticBordSerializer
    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        

        queryset =Notic_Bord.objects.filter().order_by('id')

        if id:
            queryset = queryset.filter(id=id)

        return queryset

class navbarmenuApiView(generics.ListAPIView):

    serializer_class = NavbarMenuSerializer
    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        

        queryset = Navbar_Menu.objects.filter().order_by('id')

        if id:
            queryset = queryset.filter(id=id)

        return queryset
    
class navbarsubmenuApiView(generics.ListAPIView):

    serializer_class = NavbarSubMenuSerializer
    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        

        queryset = Navbar_Sub_Menu.objects.filter().order_by('id')

        if id:
            queryset = queryset.filter(id=id)

        return queryset
    

class importent_link_Api(generics.ListAPIView):

    serializer_class = ImportentLinkSerializer
    def get_queryset(self):
        id = self.request.query_params.get('id',None)
        

        queryset = Footer_Link.objects.filter().order_by('id')

        if id:
            queryset = queryset.filter(id=id)

        return queryset