from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Hostel', model='Hostel')
content_type = ContentType.objects.get(app_label='Hostel', model='Hostel')

permission = Permission.objects.create(codename='H10000000',
                                       name='Hostel and Dining',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000001',
                                       name='Bed Type Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='H10000002',
                                       name='PayFor Type Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='H10000003',
                                       name='Bed Create',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='H10000004',
                                       name='Room Create',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='H10000005',
                                       name='Meal Type Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000006',
                                       name='Meal Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000007',
                                       name='Payment Management',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000008',
                                       name='Hostel Registration',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000009',
                                       name='Add Student to Meal',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H100000010',
                                       name='Daily Meal Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='H10000011',
                                       name='Payfor Type',
                                       content_type=content_type)

