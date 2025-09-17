from rest_framework import serializers
from apps.attributes.models import Parameter, Attribute


class ParameterGetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class AttributeGetSerializers(serializers.ModelSerializer):
    parameter = ParameterGetSerializers()
    class Meta:
        model = Attribute
        fields = ('id', 'name', 'parameter')