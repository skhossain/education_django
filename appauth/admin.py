from django.contrib import admin

# Register your models here.
from appauth.models import *

admin.site.register(Global_Parameters)
admin.site.register(Report_Configuration)
admin.site.register(Report_Parameter)
admin.site.register(Report_Parameter_Mapping)
admin.site.register(User_Settings)
admin.site.register(Branch)
admin.site.register(Employees)
admin.site.register(Eodsod_Process_List)
admin.site.register(Inventory_Number)
admin.site.register(Report_List)