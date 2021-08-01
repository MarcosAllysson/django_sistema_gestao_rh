import json
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from .models import RegistroHoraExtra
from .forms import RegistroHoraExtraForm

# CSV
import csv


# Create your views here.
class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        """
        Sobrescrevendo o método para que retorne apenas os objetos filtrados pela empresa
        no qual o funcionário cadastrou / trabalha.
        """
        empresa_logada = self.request.user.funcionario.empresa
        queryset = RegistroHoraExtra.objects.filter(funcionario__empresa=empresa_logada)
        return queryset


class HoraExtraUpdate(UpdateView):
    model = RegistroHoraExtra
    # success_url = reverse_lazy('list_hora_extra')
    form_class = RegistroHoraExtraForm  # Filtrando select pra que apareça funcionários da mesma empresa logada

    def get_form_kwargs(self):
        # Filtrando select pra que apareça funcionários da mesma empresa logada
        kwargs = super(HoraExtraUpdate, self).get_form_kwargs()
        # print(kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs


class HoraExtraDelete(DeleteView):
    model = RegistroHoraExtra
    template_name = 'registro_hora_extra/registrohoraextra_confirm_delete.html'
    success_url = reverse_lazy('list_hora_extra')


class HoraExtraCreate(CreateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm  # Filtrando select pra que apareça funcionários da mesma empresa logada
    success_url = reverse_lazy('list_hora_extra')

    def get_form_kwargs(self):
        # Filtrando select pra que apareça funcionários da mesma empresa logada
        kwargs = super(HoraExtraCreate, self).get_form_kwargs()
        # print(kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs


class UtilizouHoraExtra(View):
    def post(self, *args, **kwargs):
        # Fazendo consulta no banco, pelo pk, para registrar que as horas foram utilizadas
        registro_hora_extra = RegistroHoraExtra.objects.get(pk=kwargs['pk'])
        registro_hora_extra.utilizada = True
        registro_hora_extra.save()

        # Retornando saldo atualizado do funcionario
        empregado = self.request.user.funcionario

        response = json.dumps({
            'mensagem': 'Requisição executada',
            'horas': float(empregado.total_horas_extra)
        })

        # Retornando HttpResponse
        return HttpResponse(response, content_type='application/json')


class ExportarCSV(View):
    """
    Exportando CSV do registro de banco de horas
    """

    def get(self, request):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )

        registro_hora_extra = RegistroHoraExtra.objects.filter(utilizada=False)

        writer = csv.writer(response)

        # Título das colunas (CABEÇALHO)
        writer.writerow(['ID', 'Motivo', 'Funcionário', 'Horas restantes', 'Horas'])

        # Iterando sobre as linhas
        for registro in registro_hora_extra:
            writer.writerow([
                registro.id,
                registro.motivo,
                registro.funcionario,
                registro.funcionario.total_horas_extra,
                registro.horas
            ])

        return response
