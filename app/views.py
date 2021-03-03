from django.shortcuts import render, HttpResponse
import requests
from django.views import View

from selenium import webdriver

class ConstanciaInscripcion(View):
    
    def get(self, request):
       return render(request, 'app/constancia-inscripcion.html')
       