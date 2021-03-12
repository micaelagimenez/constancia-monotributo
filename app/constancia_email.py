from django.core.mail import EmailMultiAlternatives
from . import views

def constancia_email(email):

    subject, from_email, to = 'Constancia Monotributo', 'braavosi@outlook.es', email
    text_content = 'Hola! Gracias por usar Gestorando.  Te enviamos el PDF de la Constancia Monotributo que solicistate. Saludos, El equipo de Gestorando'
    html_content = '<p><strong>Hola!</strong></p> <p> Gracias por usar Gestorando. Te enviamos el PDF de la Constancia Monotributo que solicistate. </p> <p>Saludos,</p> <p>El equipo de Gestorando</p>'
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    attachment = open('constancia.pdf', 'rb')
    msg.attach('constancia.pdf', attachment.read(), 'text/pdf')
    msg.content_subtype = 'html'
    msg.attach_alternative(html_content, "text/html")
    msg.send()
