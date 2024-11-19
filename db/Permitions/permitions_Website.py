from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Website', model='Website')
content_type = ContentType.objects.get(app_label='Website', model='Website')

permission = Permission.objects.create(codename='W10000000',
                                       name='Create Pages',
                                       content_type=content_type)
permission = Permission.objects.create(codename='W10000001',
                                       name='Create PDF Notice',
                                       content_type=content_type)
permission = Permission.objects.create(codename='W10000002',
                                       name='Slider Manage',
                                       content_type=content_type)
permission = Permission.objects.create(codename='W10000003',
                                       name='Website Menu',
                                       content_type=content_type)
permission = Permission.objects.create(codename='W10000005',
                                       name='Add Important Link',
                                       content_type=content_type)
