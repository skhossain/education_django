from django.contrib import admin

from edu.models import *

admin.site.register(Application_Settings)
admin.site.register(Academic_Year)
admin.site.register(Academic_Class)
admin.site.register(Academic_Class_Group)
admin.site.register(Section_Info)
admin.site.register(Subject_Category)
admin.site.register(Subject_List)
admin.site.register(Students_Info)
admin.site.register(Shift_Info)
admin.site.register(Degree_Info)
admin.site.register(Fees_Processing_Details)
# Result
admin.site.register(Exam_Marks_By_Subject)
admin.site.register(Exam_Marks_Final)
admin.site.register(Teacher)
admin.site.register(Employee_Details)

