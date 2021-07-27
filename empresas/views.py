from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from .models import Empresa


# Create your views here.
class EmpresaCreate(CreateView):
    model = Empresa
    template_name = 'empresas/empresa_form.html'
    fields = ['nome']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Ao criar empresa, adicionar a mesma pro usuário que tá logado
        """
        obj = form.save()
        funcionario = self.request.user.funcionario
        funcionario.empresa = obj
        funcionario.save()
        return HttpResponse("Ok")


class EmpresaEdit(UpdateView):
    model = Empresa
    template_name = 'empresas/empresa_form.html'
    fields = ['nome']
    success_url = reverse_lazy('home')
