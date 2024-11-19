from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Hrm', model='Hrm')
content_type = ContentType.objects.get(app_label='Hrm', model='Hrm')

permission = Permission.objects.create(codename='HR10000000',
                                       name='HR Setting',
                                       content_type=content_type)

permission = Permission.objects.create(codename='HR10000001',
                                       name='Deparment Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='HR10000002',
                                       name='Designation Setup',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='HR10000003',
                                       name='Company Setup',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='HR10000004',
                                       name='Office Location',
                                       content_type=content_type)

permission = Permission.objects.create(codename='HR10000005',
                                       name='Shift Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='HR10000006',
                                       name='Employee Degree',
                                       content_type=content_type)
permission = Permission.objects.create(codename='HR10000007',
                                       name='Employment Type',
                                       content_type=content_type)

