from django.db import models

# Create your models here.

"""
 Modelos de la aplicación 'Acorta'
 Basicamente tendremos una tabla, con URL larga y URL corta asociada.
 La clase tiene un método para buscar en la tabla un index libre y dar una url corta
"""

 # Cada clase es una tabla. Y luego larga o corta serán columnas

class URLModel(models.Model):
    larga = models.CharField(max_length=200)
    corta = models.CharField(max_length=200)

    def __str__(self):
        return self.URLModel.larga

    def Search_Last_Index(base, domain):
        #empiezas desde el cero a hacer búsquedas en la base.
        # si falla, significa que esa URL (corta) está libre, así que la usas
        count = 0
        while True:
            try:
                target = 'http://'+domain+'/acorta/'+str(count)
                element = base.objects.get(corta=target)
                count +=1
            except base.DoesNotExist:
                return count
