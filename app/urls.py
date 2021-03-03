from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('constancia-inscripcion', views.ConstanciaInscripcion.as_view(), name='constancia-inscripcion'),
]