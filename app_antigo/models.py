from django.db import models


# Create your models here.
class Teste(models.Model):
    descricao = models.TextField()

    def __str__(self):
        return self.descricao
