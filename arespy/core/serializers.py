from .models import leitePreco
from rest_framework import serializers


class leitePrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = leitePreco
        fields = ['data', 'producao', 'unidade', 'valor', 'coments']