from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.create(app_label='Education', model='Education')
content_type = ContentType.objects.get(app_label='Education', model='Education')

permission = Permission.objects.create(codename='E10000000',
                                       name='Academic Setting',
                                       content_type=content_type)
                                       
permission = Permission.objects.create(codename='E10000001',
                                       name='Academic Information',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E10000002',
                                       name='Create Year',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E10000003',
                                       name='Create Class',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E10000004',
                                       name='Create Class Group',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E10000005',
                                       name='Create Subject Category',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000006',
                                       name='Create Subject Type',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000007',
                                       name='Create Subject',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000008',
                                       name='Create Section',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000009',
                                       name='Create Session',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E100000010',
                                       name='Create Department',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000011',
                                       name='Create Shift',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000012',
                                       name='Create Degree',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000013',
                                       name='Create Profession',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E10000014',
                                       name='Create Student Category',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E20000000',
                                       name='Admission',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000001',
                                       name='Education Institiute',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E20000002',
                                       name='Admission Form',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E20000003',
                                       name='Admitted Student',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E20000004',
                                       name='Quick Admission',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000005',
                                       name='Quick Admission Edit',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000006',
                                       name='Student Subject Choice',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000007',
                                       name='Choice Subject List',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000008',
                                       name='Transfer Certificate',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000009',
                                       name='Create ID Card',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E20000010',
                                       name='Create Admit Card',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000011',
                                       name='Student Name Plate',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000012',
                                       name='Student Migrations',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E20000013',
                                       name='Course Registration',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E30000000',
                                       name='Academic Routine',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E30000001',
                                       name='Create Class Teacher',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E30000002',
                                       name='Create Class Room',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E30000003',
                                       name='Create Class Routine',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E30000004',
                                       name='Create Routine Details',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E30000005',
                                       name='Routine Query',
                                       content_type=content_type)


permission = Permission.objects.create(codename='E40000000',
                                       name='Fees Create and Mapping',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E40000001',
                                       name='Create Fees Head',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000002',
                                       name='Create Fees Waiver',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000003',
                                       name='Create Fees Mapping',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000004',
                                       name='Create Absent Fine Mapping',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000005',
                                       name='Pay Slip Processing',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000006',
                                       name='Fees Receive Student',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000007',
                                       name='Quick Collection',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E40000008',
                                       name='Create Fees Waive Student',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E50000000',
                                       name='Pre Admission',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E50000001',
                                       name='Visited Student',
                                       content_type=content_type)


permission = Permission.objects.create(codename='E60000000',
                                       name='Student Attendance',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E60000001',
                                       name='Attendance Sheet',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E60000002',
                                       name='Add a New Student Attendance Sheet',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000000',
                                       name='Exam & Result',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000001',
                                       name='Result Grade',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000002',
                                       name='Exam Type',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000003',
                                       name='Exam Term',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000004',
                                       name='Exam Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000005',
                                       name='Online Exam Setup',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000006',
                                       name='Submitted Question',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000007',
                                       name='Exam Marks Entry',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000008',
                                       name='Result View Before Publish',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000009',
                                       name='Result View After Publish',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E70000010',
                                       name='Merge Result',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000011',
                                       name='Marks Blank Sheet',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000012',
                                       name='Exam Seat Label',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000013',
                                       name='Result Before Publish',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000014',
                                       name='Result Before Publish Hefz',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000015',
                                       name='Result Publish Enable',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000016',
                                       name='Result View Setting',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000017',
                                       name='Result Process',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000018',
                                       name='Result View',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000019',
                                       name='Term Result Marge',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000020',
                                       name='Term Result Marge Process',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000021',
                                       name='Three Term Marge',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E70000022',
                                       name='Hefz Result Entry',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000000',
                                       name='Libray Management',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000001',
                                       name='Libray Rack Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000002',
                                       name='Libray Author Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000003',
                                       name='Libray Editor Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000004',
                                       name='Libray Books Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000005',
                                       name='Libray Card Create',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000006',
                                       name='Libray Book Issue',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E80000007',
                                       name='Libray Book Request',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E90000000',
                                       name='Education Report',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E90000001',
                                       name='Student Filter',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E11000001',
                                       name='Forms',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E11000002',
                                       name='Admission Form Download',
                                       content_type=content_type)

permission = Permission.objects.create(codename='E12000001',
                                       name='Fees & Charge Reports',
                                       content_type=content_type)
                                       
permission = Permission.objects.create(codename='E12000002',
                                       name='Student Fees Collection',
                                       content_type=content_type)


permission = Permission.objects.create(codename='E13000000',
                                       name='Teacher Info',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E13000001',
                                       name='Down menu Teacher Info',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E13000002',
                                       name='Subject Mapping Teacher',
                                       content_type=content_type)

#Certificat
permission = Permission.objects.create(codename='E14000000',
                                       name='Certificat',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E14000001',
                                       name='Certificat Header Address',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E14000002',
                                       name='Create Certificate Name',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E14000003',
                                       name='Create Board Name',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E14000004',
                                       name='Search Students for Certificate',
                                       content_type=content_type)
permission = Permission.objects.create(codename='E14000005',
                                       name='Testimonial List',
                                       content_type=content_type)



permission = Permission.objects.create(codename='P10000000',
                                       name='Payroll',
                                       content_type=content_type)
permission = Permission.objects.create(codename='P10000001',
                                       name='Salary Scale',
                                       content_type=content_type)
permission = Permission.objects.create(codename='P10000002',
                                       name='Allownce Setup',
                                       content_type=content_type)
permission = Permission.objects.create(codename='P10000003',
                                       name='Paybill',
                                      content_type=content_type)



permission = Permission.objects.create(codename='ME10000000',
                                       name='Manage Employee',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000001',
                                       name='ADD Employee',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000002',
                                       name='Employee List',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000003',
                                       name='Document Type',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000004',
                                       name='Upload Document',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000005',
                                       name='Leave Info',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000006',
                                       name='Leave application',
                                       content_type=content_type)
permission = Permission.objects.create(codename='ME10000007',
                                       name='Training Information',
                                       content_type=content_type)

