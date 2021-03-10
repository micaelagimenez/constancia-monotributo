from django.shortcuts import render, HttpResponse
import requests
from django.views.generic import FormView
from .forms import MonotributoForm
from app.ws_sr_padron import ws_sr_padron13_get_persona
from app.captcha import resolve_simple_captcha
from app.constancia_email import constancia_email
from ratelimit.decorators import ratelimit

#selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

#screenshot pdf
import io
from PIL import Image
from importlib import reload
import sys


class ConstanciaInscripcion(FormView):

    def get(self, request):
       return render(request, 'app/constancia-inscripcion.html')
    
    @ratelimit(key='ip', rate='3/d')
    def post(self,request):

        form = MonotributoForm(request.POST)
        email = request.POST['Email']


        #Verificar cuit en padron13 una vez que es ingresado
        cuit_r = int(request.POST["CUIT"])
        response = ws_sr_padron13_get_persona(cuit_r)
        
        try:
            nombre = response["persona"]["nombre"]
            apellido = response["persona"]["apellido"]
            cuit = response["persona"]["tipoClave"]
       
        except KeyError:
            nombre, apellido = None, None
            print("El CUIT ingresado es incorrecto")

        except TypeError:
            nombre, apellido = None, None
            print("El CUIT ingresado es incorrecto")

        else:
            if cuit != "CUIT":
                print("No es un cuit")

            else:
                print(nombre, apellido)
        
                if form.is_valid():
                    cuit = form.cleaned_data.get('CUIT')
                    email = form.cleaned_data.get('Email')
                    cuit.save()
                    email.save()
                    return render(request, 'app/constancia-inscripcion.html')             
                
    
                #Selenium script
                DRIVER_PATH = 'C:/Users/micae/Documents/python/chromedriver.exe'
                
                driver = webdriver.Chrome(executable_path=DRIVER_PATH)
                driver.get(' https://seti.afip.gob.ar/padron-puc-constancia-internet/jsp/Constancia.jsp')

                
                wait = WebDriverWait(driver, 30) 
                elem_cuit = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='cuit']")))
                elem_cuit.send_keys(cuit_r)
                
                #get captcha
                elem_captcha = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div/div/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/div/div/div[1]/img")))
                img_captcha_base64 = driver.execute_async_script("""
                var ele = arguments[0], callback = arguments[1];
                ele.addEventListener('load', function fn(){
                ele.removeEventListener('load', fn, false);
                var cnv = document.createElement('canvas');
                cnv.width = this.width; cnv.height = this.height;
                cnv.getContext('2d').drawImage(this, 0, 0);
                callback(cnv.toDataURL('image/jpeg').substring(22));
                }, false);
                ele.dispatchEvent(new Event('load'));
                """, elem_captcha) 
                img_captcha_base64 = img_captcha_base64.replace(',', '')
                solved_captcha = resolve_simple_captcha(img_captcha_base64)

                elem_captcha_field = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='captchaField']")))
                elem_captcha_field.send_keys(solved_captcha)

                #submit form
                submit_form = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="btnConsultar"]')))
                submit_form.click()
            
                #save screenshot 
                sleep(4)
                constancia =  wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/table[2]')))
                constancia_screenshot = constancia.screenshot_as_png
                
                #screenshot to pdf
                a = io.BytesIO(constancia_screenshot)
                image1 = Image.open(a)
                im1 = image1.convert('RGB')
                im1.save('constancia.pdf')
                pdf = open('constancia.pdf','rb').read()

                #send email
                constancia_email(pdf, email)

                if constancia_email == True:
                    print("Sus datos fueron enviados correctamente, en un máximo de 2 hs. estarás recibiendo tu constancia por email.")
                else:
                    print("No hemos podido procesar su solicitud, por favor reintente nuevamente más tarde.")

            
        return render(request, 'app/constancia-inscripcion.html')

        

