from rest_framework import serializers
import datetime

from sms.models import *
from appauth.models import Query_Table, WEEK_DAY_DICT


class SMS_Application_Setting_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SMS_Application_Settings
        fields = ('__all__')


class sms_template_Serializer(serializers.ModelSerializer):
    template_type_name = serializers.SerializerMethodField(
        'get_template_type_name')

    class Meta:
        model = sms_template
        fields = ('__all__')

    def get_template_type_name(self, obj):
        template_type = ''
        try:
            template_type = str(TEMPLATE_DICT[obj.template_type])
        except Exception as e:
            print(str(e))
        return template_type


class sms_sent_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sms_sent
        fields = ('__all__')

class sms_que_Serializer(serializers.ModelSerializer):
    class Meta:
        model = sms_que
        fields = ('__all__')