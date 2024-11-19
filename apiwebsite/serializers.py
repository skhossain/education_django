from django.db.models import fields
from rest_framework import serializers
import datetime

from website.models import *
from apiauth.serializers import *


class ImageCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Carousel
        fields = ('__all__')

class NoticBordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notic_Bord
        fields = ('__all__')

class NavbarMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar_Menu
        fields = ('__all__')


class NavbarSubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navbar_Sub_Menu
        fields = ('__all__')


class ImportentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footer_Link
        fields = ('__all__')


