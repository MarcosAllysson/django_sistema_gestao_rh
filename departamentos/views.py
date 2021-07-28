from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Departamento


# Create your views here.
class DepartamentosList(ListView):
    model = Departamento
    template_name = 'departamentos/list_departamentos.html'

    # Filtrando departamentos do usuário logado
    def get_queryset(self):
        empresa_logado = self.request.user.funcionario.empresa
        return Departamento.objects.filter(empresa=empresa_logado)


class DepartamentosCreate(CreateView):
    model = Departamento
    template_name = 'departamentos/form_departamentos.html'
    fields = ['nome']
    success_url = reverse_lazy('list_departamentos')

    def form_valid(self, form):
        departamento = form.save(commit=False)  # não salva no banco, apenas em memória
        departamento.empresa = self.request.user.funcionario.empresa

        # Salvando funcionário
        departamento.save()
        return super(DepartamentosCreate, self).form_valid(form)


class DepartamentosUpdate(UpdateView):
    model = Departamento
    template_name = 'departamentos/form_departamentos.html'
    fields = ['nome']
    success_url = reverse_lazy('list_departamentos')


class DepartamentosDelete(DeleteView):
    model = Departamento
    template_name = 'departamentos/delete_departamento_confirmation.html'
    success_url = reverse_lazy('list_departamentos')
