from django.db import models

# Create your models here.

""" Modelos de la aplicación 'Acorta'
 Basicamente tendremos una tabla, con URL larga y URL corta asociada.
 """

 # Cada clase es una tabla. Y luego larga o corta serán columnas

class URL(models.Model):
    larga = models.CharField(max_length=200)
    corta = models.CharField(max_length=200)
