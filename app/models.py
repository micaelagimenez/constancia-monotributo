from django.db import models

class Monotributo(models.Model):
    
    cuit = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    fecha_solicitud = models.DateTimeField()
    resultado = models.CharField(max_length=100)
    enviado = models.BooleanField()

    def __str__(self):
        return self.title