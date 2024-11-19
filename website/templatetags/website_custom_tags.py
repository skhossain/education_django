from django.db.models.aggregates import Count, Sum
from hrm.models import Employee_Designation
from django import template
from django.shortcuts import get_object_or_404

register = template.Library()


def get_designation_name(designation_id):
    if designation_id:
        designation_name=Employee_Designation.objects.get(desig_id=designation_id).desig_name
    else:
        designation_name=""    
    return designation_name
register.filter('get_designation_name', get_designation_name)

