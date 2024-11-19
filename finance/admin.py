from django.contrib import admin

# Register your models here.

from finance.models import *

admin.site.register(Application_Settings)
admin.site.register(Accounts_Balance)
admin.site.register(Cash_And_Bank_Ledger)
admin.site.register(General_Ledger)
admin.site.register(Account_Type)
admin.site.register(Client_Type)
admin.site.register(Transaction_Type)
admin.site.register(Ledger_Transaction_Type)
admin.site.register(Client_Account_Mapping)