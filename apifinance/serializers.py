from rest_framework import serializers
import datetime

from finance.models import *
from appauth.models import Query_Table


def fn_finance_general_ledger(p_gl_code):
    try:
        ledger = General_Ledger.objects.get(gl_code=p_gl_code)
        return ledger.gl_name
    except Exception as e:
        return ''


class General_Ledger_Serializer(serializers.ModelSerializer):
    class Meta:
        model = General_Ledger
        fields = ('__all__')


class Transaction_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_Type
        fields = ('__all__')


class Ledger_Transaction_Type_Serializer(serializers.ModelSerializer):
    gl_name = serializers.SerializerMethodField('get_general_ledger')

    class Meta:
        model = Ledger_Transaction_Type
        fields = ['id', 'tran_type_id', 'gl_code', 'gl_name', 'is_active']

    def get_general_ledger(self, obj):
        return str(obj.gl_code)


class Cash_And_Bank_Ledger_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cash_And_Bank_Ledger
        fields = ('__all__')


class Account_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Account_Type
        fields = ('__all__')


class Client_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Type
        fields = ('__all__')


class Client_Account_Mapping_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Account_Mapping
        fields = ('__all__')


class Transaction_Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_Table
        fields = ('__all__')


class Transaction_Master_Serializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    branch_code = serializers.IntegerField()
    tran_date = serializers.DateField(initial=datetime.date.today)
    batch_number = serializers.IntegerField()
    total_debit_amount = serializers.DecimalField(
        max_digits=22, decimal_places=2)
    transaction_narration = serializers.CharField()
    cancel_by = serializers.CharField()
    app_user_id = serializers.CharField()
    auth_by = serializers.CharField()


class Transaction_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_Details
        fields = ('__all__')


class Finance_Query_Table_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Query_Table
        fields = ('__all__')

class Search_Accounts_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_account_number')
    text = serializers.SerializerMethodField('get_account_details')

    class Meta:
        model = Accounts_Balance
        fields = ['id', 'text']

    def get_account_number(self, obj):
        return obj.account_number

    def get_account_details(self, obj):
        return str(obj.account_title)+" - "+str(obj.account_comments).replace("None","")+" - "+str(obj.account_address).replace("None","")+" - "+str(obj.phone_number).replace("None","")


class Accounts_Balance_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts_Balance
        fields = ('__all__')


class Tran_Telbal_Details_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tran_Telbal_Details
        fields = ('__all__')


class Deposit_Receive_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit_Receive
        fields = ('__all__')


class Deposit_Payment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit_Payment
        fields = ('__all__')


class Charges_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        fields = ('__all__')

class IBR_Transaction_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_Ibr
        fields = ('__all__')

class Transaction_Table_Ledger_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction_Table_Ledger
        fields = ('__all__')

