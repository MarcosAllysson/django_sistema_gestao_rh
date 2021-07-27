from django.db import models


# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=100, help_text='Nome da empresa')

    def __str__(self):
        return self.nome

    # Outra maneira de redicionar o usuário após editar o objeto
    # Após objeto ser editado, django procura pelo get_absolute_url. Outra opção é usar success_url
    # def get_absolute_url(self):
    #     return reverse('home')
