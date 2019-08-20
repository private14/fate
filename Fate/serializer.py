from rest_framework import serializers
from accounts.models import *


class EnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Env
        fields = '__all__'


class CopyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopyProduct
        fields = '__all__'
