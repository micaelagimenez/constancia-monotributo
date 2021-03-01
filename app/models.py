from django.db import models
import urllib.request
import urllib
import json
from urllib.parse import quote

class Monotributo(models.Model):
    
    cuit = models.CharField(max_length=200)
    email = models.CharField()
    fecha_solicitud = models.DateTimeField()
    resultado = models.CharField(max_length=100)
    enviado = models.BooleanField()

    def __str__(self):
        return self.title