from funcionarios.models import Funcionario
from rest_framework import serializers
from registro_hora_extra.api.serializers import RegistroHoraExtraSerializer


class FuncionarioSerializer(serializers.ModelSerializer):
    registrohoraextra_set = RegistroHoraExtraSerializer(many=True)  # retornar os dados, invéa dos ID's

    class Meta:
        model = Funcionario
        fields = ('id', 'nome', 'departamentos', 'empresa', 'user', 'total_horas_extra', 'registrohoraextra_set')

