from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import Funcionario


# Create your views here.
class FuncionarioList(ListView):
    model = Funcionario
    template_name = 'funcionarios/list_funcionarios.html'

    def get_queryset(self):
        """
        Sobrescrevendo o método para que retorne apenas os objetos filtrados pela empresa
        no qual o funcionário cadastrou / trabalha.
        """
        empresa_logada = self.request.user.funcionario.empresa
        queryset = Funcionario.objects.filter(empresa=empresa_logada)
        return queryset


class FuncionarioUpdate(UpdateView):
    model = Funcionario
    template_name = 'funcionarios/form_funcionario.html'
    fields = ['nome', 'departamentos']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    template_name = 'funcionarios/delete_funcionario_confirmation.html'
    success_url = reverse_lazy('list_funcionarios')


class FuncionarioCreate(CreateView):
    model = Funcionario
    template_name = 'funcionarios/form_funcionario.html'
    fields = ['nome', 'departamentos']
    success_url = reverse_lazy('list_funcionarios')

    # Quando novo funcionário é criado, é necessário criar um novo usuário, empresa etc. Override django método
    def form_valid(self, form):
        funcionario = form.save(commit=False)  # não salva no banco, apenas em memória
        funcionario.empresa = self.request.user.funcionario.empresa

        # Usando User do django pra criar usuário
        funcionario.user = User.objects.create(
            username=funcionario.nome.split(' ')[0] + funcionario.nome.split(' ')[1]
        )

        # Salvando funcionário
        funcionario.save()
        return super(FuncionarioCreate, self).form_valid(form)

