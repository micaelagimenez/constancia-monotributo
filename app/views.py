from django.shortcuts import render, HttpResponse
import requests
from django.views import View

from selenium import webdriver

from bs4 import BeautifulSoup

from .forms import MonotributoForm


class ConstanciaInscripcion(View):

    def get(self, request):
       return render(request, 'app/constancia-inscripcion.html')
    
    def post(self,request):

        if request:

            form = MonotributoForm(request.POST)

            if form.is_valid():
                cuit = form.cleaned_data.get('cuit')
                email = form.cleaned_data.get('email')
                cuit.save()
                email.save()
                return HttpResponseRedirect('app/constancia-inscripcion.html')
        else:
             pass # could add a notification here
        
        