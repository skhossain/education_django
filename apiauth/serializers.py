from rest_framework import serializers
import datetime
from website.models import *

from appauth.models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('__all__')

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Loc_Country
        fields = ('__all__')

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('__all__')

class User_Settings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User_Settings
        fields = ('__all__')

        

class Division_Serializer(serializers.ModelSerializer):
    country_id=CountrySerializer()
    class Meta:
        model = Loc_Division
        fields = ('__all__')
        

class District_Serializer(serializers.ModelSerializer):
    division_id=Division_Serializer()
    class Meta:
        model = Loc_District
        fields = ('__all__')

        

class Upazila_Serializer(serializers.ModelSerializer):
    district_id=District_Serializer()
    class Meta:
        model = Loc_Upazila
        fields = ('__all__')
        

class Union_Serializer(serializers.ModelSerializer):
    upozila_id=Upazila_Serializer()
    class Meta:
        model = Loc_Union
        fields = ('__all__')


class pdf_information(serializers.ModelSerializer):
    class Meta:
        model = Education_Lavel
        fields = ['id','notic_title', 'pdf_file','status']
   