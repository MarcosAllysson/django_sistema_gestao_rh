from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Documento


# Create your views here.
class DocumentoCreate(CreateView):
    model = Documento
    fields = ['descricao', 'arquivo']
    template_name = 'documentos/documento_form.html'
    # success_url = reverse_lazy('list_funcionarios')

    # Ao criar um documento, deve-se associa-lo ao usuário. Override no post
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.pertence_id = self.kwargs['funcionario_id']  # passado na url como parâmetro

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
