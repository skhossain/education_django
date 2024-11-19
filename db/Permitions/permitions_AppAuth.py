from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='AppAuth', model='AppAuth')
content_type = ContentType.objects.get(app_label='AppAuth', model='AppAuth')

permission = Permission.objects.create(codename='D99999999',
                                       name='Dashboard',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A10000000',
                                       name='Authentication',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A11000001',
                                       name='Create User',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='A11000002',
                                       name='User List',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='A20000000',
                                       name='Settings',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000001',
                                       name='Manage Branch',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000002',
                                       name='Employee Register',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000003',
                                       name='Director Register',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000004',
                                       name='Country Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000005',
                                       name='Division Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000006',
                                       name='District Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000007',
                                       name='Upazila Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='A20000008',
                                       name='Union Setup',
                                       content_type=content_type) 
									   
									   