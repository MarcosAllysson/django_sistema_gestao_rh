from rest_framework import viewsets
from registro_hora_extra.api.serializers import RegistroHoraExtraSerializer
from registro_hora_extra.models import RegistroHoraExtra

# Permissão / autenticação
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RegistroHoraExtraViewSet(viewsets.ModelViewSet):
    queryset = RegistroHoraExtra.objects.all()
    serializer_class = RegistroHoraExtraSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
