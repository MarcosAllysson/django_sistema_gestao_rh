from registro_hora_extra.models import RegistroHoraExtra
from rest_framework import serializers


class RegistroHoraExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHoraExtra
        fields = ('motivo', 'funcionario', 'horas', 'utilizada')

