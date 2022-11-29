from django.db import models

# Create your models here.
class leitePreco(models.Model):
    data = models.DateField(auto_now=False, auto_now_add=False,)
    producao = models.CharField(max_length=50)
    unidade = models.CharField(max_length=20)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    coments = models.CharField(max_length=50)