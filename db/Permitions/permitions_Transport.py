from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Transport', model='Transport')
content_type = ContentType.objects.get(app_label='Transport', model='Transport')

permission = Permission.objects.create(codename='T10000000',
                                       name='Transportation System',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000001',
                                       name='Transport Type Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='T10000002',
                                       name='Transport Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='T10000003',
                                       name='Location Create',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='T10000004',
                                       name='Vehicle Type Create',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='T10000005',
                                       name='Vehicle Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000006',
                                       name='Driver Info Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000007',
                                       name='Conductor Info Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000008',
                                       name='Road Map Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000009',
                                       name='Road Map Details Create',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T100000010',
                                       name='Admit Transport',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000011',
                                       name='Payfor Type',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000012',
                                       name='Payment Management',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000013',
                                       name='Presence in transport',
                                       content_type=content_type)
permission = Permission.objects.create(codename='T10000014',
                                       name='Transport use summery',
                                       content_type=content_type)
