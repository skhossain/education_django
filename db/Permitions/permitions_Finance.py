from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Finance', model='Finance')
content_type = ContentType.objects.get(app_label='Finance', model='Finance')

permission = Permission.objects.create(codename='F10000000',
                                       name='Accounts Transaction',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10000001',
                                       name='Account Transaction',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10000002',
                                       name='Ledger Transaction',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10000003',
                                       name='Journal Voucher',
                                       content_type=content_type)
									   
permission = Permission.objects.create(codename='F10000005',
                                       name='Account Statement',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10000006',
                                       name='Transaction List',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10000007',
                                       name='Transaction Cancel',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F20000000',
                                       name='Teller Management',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F20000001',
                                       name='Balance Transfer Request',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F20000002',
                                       name='Cash Receive/Payment',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F20000003',
                                       name='Teller Balance Report',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F30000000',
                                       name='Accounts Query',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F30000001',
                                       name='Account Balance',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F30000002',
                                       name='Account Transaction Details',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F30000003',
                                       name='Transaction List',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F30000004',
                                       name='Transaction Details Query',
                                       content_type=content_type) 
									   
permission = Permission.objects.create(codename='F40000000',
                                       name='Accounts Settings',
                                       content_type=content_type) 
									   
permission = Permission.objects.create(codename='F40000001',
                                       name='Chart Of Account (COA)',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000002',
                                       name='Charge Parameter Settings',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000003',
                                       name='Transaction Type Settings',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000004',
                                       name='Transaction Ledger Mapping',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000005',
                                       name='Cash & Bank Ledger',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000006',
                                       name='Manage Account Type',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000007',
                                       name='Manage Clients Type',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F40000008',
                                       name='Client Account Mapping',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F50000000',
                                       name='Inter Branch Transaction',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F50000001',
                                       name='Fund Transfer Request',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F50000002',
                                       name='Transfer Request List',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001000',
                                       name='Accounts Report',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001001',
                                       name='Account Balance',
                                       content_type=content_type)

permission = Permission.objects.create(codename='F10001002',
                                       name='Cash Transaction Details',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001003',
                                       name='Ledger Statement',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001004',
                                       name='Receipt & Payment',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001005',
                                       name='Balance Sheet (Asset & Liabilities)',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001006',
                                       name='Income & Expenses',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001007',
                                       name='Trial Balance',
                                       content_type=content_type) 

permission = Permission.objects.create(codename='F10001008',
                                       name='Cash & Bank (Receipt & Payment)',
                                       content_type=content_type) 



