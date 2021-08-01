from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.urls import reverse

from departamentos.models import Departamento
from empresas.models import Empresa


# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    departamentos = models.ManyToManyField(Departamento)
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('list_funcionarios')

    # Cálculo do registro de horas extra do funcionário
    # @property
    def total_horas_extra(self):
        # Usar Aggregate Sum do django pra retornar a soma da hora extra
        return self.registrohoraextra_set.filter(utilizada=False).aggregate(Sum('horas'))['horas__sum'] or 0
