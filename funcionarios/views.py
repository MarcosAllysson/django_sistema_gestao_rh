from django.urls import reverse
from django.views.generic import ListView, UpdateView
from .models import Funcionario


# Create your views here.
class FuncionarioList(ListView):
    model = Funcionario
    template_name = 'funcionarios/list_funcionarios.html'

    def get_queryset(self):
        """
        Sobrescrevendo o método para que retorne apenas os objetos filtrados pela empresa
        no qual o funcionário cadastrou / trabalha.
        :return:
        """
        empresa_logada = self.request.user.funcionario.empresa
        queryset = Funcionario.objects.filter(empresa=empresa_logada)
        return queryset


class FuncionarioUpdate(UpdateView):
    model = Funcionario
    template_name = 'funcionarios/form_funcionario.html'
    fields = ['nome', 'departamentos']
