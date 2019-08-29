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


class RandomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomList
        fields = '__all__'
