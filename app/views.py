from django.shortcuts import render, HttpResponse
import requests
from django.views.generic import FormView
from .forms import MonotributoForm
from app.ws_sr_padron import ws_sr_padron13_get_persona

from selenium import webdriver
from bs4 import BeautifulSoup

class ConstanciaInscripcion(FormView):

    def get(self, request):
       return render(request, 'app/constancia-inscripcion.html')
    
    def post(self,request):

        form = MonotributoForm(request.POST)
        
        cuit_r = int(request.POST["CUIT"])
        response = ws_sr_padron13_get_persona(cuit_r)
        
        try:
            nombre = response["persona"]["nombre"]
            apellido = response["persona"]["apellido"]
        except KeyError:
            nombre, apellido = None, None
            print("El CUIT ingresado es incorrecto")

        except TypeError:
            nombre, apellido = None, None
            print("El CUIT ingresado es incorrecto")
        
        else:
            print(nombre, apellido)

            if form.is_valid():
                cuit = form.cleaned_data.get('cuit')
                email = form.cleaned_data.get('email')
                cuit.save()
                email.save()
                return HttpResponseRedirect('app/constancia-inscripcion.html')

        return render(request, 'app/constancia-inscripcion.html')