from rest_framework import serializers

from core.models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    ''' Serializer para empresas '''

    class Meta:
        model = Empresa
        fields = ('id', 'name')
        read_only_fields = ('id',)
