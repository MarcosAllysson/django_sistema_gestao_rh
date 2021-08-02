from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from funcionarios.models import Funcionario

# Django Rest Framework
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer


# Create your views here.
@login_required
def home(request):
    """
    Permitir funcionário visualizar somente os dados da empresa que ele trabalha.
    """
    data = dict()
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)


# Django Rest Framework
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
