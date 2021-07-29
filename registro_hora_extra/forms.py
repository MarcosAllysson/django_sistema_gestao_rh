from django.forms import ModelForm
from .models import RegistroHoraExtra
from funcionarios.models import Funcionario


class RegistroHoraExtraForm(ModelForm):
    # Filtrando select para que aparece somente funcionários da mesma empresa logada

    def __init__(self, user, *args, **kwargs):
        # user -> usuário logado da requisição passado na função da view HoraExtraCreate -> get_form_kwargs()
        super(RegistroHoraExtraForm, self).__init__(*args, **kwargs)
        self.fields['funcionario'].queryset = Funcionario.objects.filter(
            empresa=user.funcionario.empresa
        )

    class Meta:
        model = RegistroHoraExtra
        fields = ['motivo', 'funcionario', 'horas']
