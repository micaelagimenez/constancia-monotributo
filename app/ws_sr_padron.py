from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from zeep import Client
import wsaa

padron13_wsdl = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA13?wsdl"
padron5_wsdl = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?wsdl"
cuit_consultante = "20309556381"



def ws_sr_padron5(cuit_requested, ta_sign=None, ta_token=None):
    try:
        if ta_sign is None and ta_token is None:
            ta_sign, ta_token = wsaa.get_ta_sign_token('ws_sr_padron_a5')
        client = Client(padron5_wsdl)
        response = client.service.getPersona(
            sign=ta_sign,
            token=ta_token,
            cuitRepresentada=cuit_consultante,
            idPersona=cuit_requested,
        )
        return serialize_object(response, target_cls=dict)
    except Exception as e:
        print('Error: ', e)
        return None


def ws_sr_padron13_get_persona(cuit_requested, ta_sign=None, ta_token=None):
    try:
        if ta_sign is None and ta_token is None:
            ta_sign, ta_token = wsaa.get_ta_sign_token('ws_sr_padron_a13')
        client = Client(padron13_wsdl)
        response = client.service.getPersona(
            sign=ta_sign,
            token=ta_token,
            cuitRepresentada=cuit_consultante,
            idPersona=cuit_requested,
        )
        return serialize_object(response, target_cls=dict)
    except Fault as e:
        if e.message == 'No existe persona con ese Id':
            return None
        elif e.message == 'Persona inactiva':
            return 'Persona inactiva'
        print('Error: ', e)
        return None
    except Exception as e:
        print('Error: ', e)
        return None