from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import Funcionario

# PDF with reportlab:
import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# PDF with xhtml2pdf:
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

# TRANSLATE
from django.utils.translation import ugettext_lazy as _


# Create your views here.
class FuncionarioList(ListView):
    model = Funcionario
    template_name = 'funcionarios/list_funcionarios.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Usando com tradução
        """
        context = super().get_context_data(**kwargs)
        context['report_button'] = _('Employee report')
        return context

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


def pdf_reportlab(request):
    response = HttpResponse(content_type='application/pdf')

    # Baixar arquivo invés de abrir na página
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Eixo X - Y começa no canto inferior esquerdo da página
    # 10 representa da margem esquerda 10px
    # 810 representa debaixo pra cima, no topo da página
    p.drawString(250, 810, "Relatório de funcionários")

    funcionarios = Funcionario.objects.filter(empresa=request.user.funcionario.empresa)
    str_funcionario = 'Nome: %s'

    y = 750
    for funcionario in funcionarios:
        p.drawString(10, y, str_funcionario % (funcionario.nome))
        y -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    return response


class Render:
    # Função base pra renderizar o PDF

    @staticmethod
    def render(path: str, params: dict, filename: str):
        template = get_template(path)
        html = template.render(params)
        response = io.BytesIO()
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode('UTF-8')), response)

        if not pdf.err:
            response = HttpResponse(
                response.getvalue(), content_type='application/pdf'
            )
            response['Content-Disposition'] = 'attachment;filename=%s.pdf' % filename
            return response

        else:
            return HttpResponse('Error rendering pdf', status=400)


class Pdf(View):
    def get(self, request):
        params = {
            'today': "Variável today",
            'sales': "Variável sales",
            'request': request,
        }
        return Render.render('funcionarios/relatorio.html', params, 'myfile')

