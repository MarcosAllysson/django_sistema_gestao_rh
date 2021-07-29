from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from .models import RegistroHoraExtra
from .forms import RegistroHoraExtraForm


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
    success_url = reverse_lazy('list_hora_extra')
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
