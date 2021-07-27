from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from funcionarios.models import Funcionario


# Create your views here.
@login_required
def home(request):
    """
    Permitir funcionário visualizar somente os dados da empresa que ele trabalha.
    """
    data = dict()
    data['usuario'] = request.user
    return render(request, 'core/index.html', data)
