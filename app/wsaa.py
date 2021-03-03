import datetime
from django.utils import timezone
from lxml import etree
from zeep import Client
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.bindings.openssl.binding import Binding

wsaa_wsdl = "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl"
cert_filepath = 'test.crt'
privatekey_filepath = 'test.key'


def _create_tra(service):
    unique_id = str(int(datetime.datetime.now().replace(microsecond=0).timestamp()))
    generation_time = datetime.datetime.now().isoformat()
    expiration_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat()

    parser = etree.XMLParser(remove_blank_text=True)
    xml = etree.fromstring("""
    <loginTicketRequest version="1.0">
        <header>
            <uniqueId>""" + unique_id + """</uniqueId>
            <generationTime>""" + generation_time + """</generationTime>
            <expirationTime>""" + expiration_time + """</expirationTime>
        </header>
        <service>""" + service + """</service>
    </loginTicketRequest>""", parser=parser)
    return etree.tostring(xml, encoding='utf-8')


def _create_cms(tra):
    _lib = Binding.lib
    _ffi = Binding.ffi

    with open(privatekey_filepath, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), None, default_backend())

    with open(cert_filepath, 'rb') as cert_file:
        cert = x509.load_pem_x509_certificate(
            cert_file.read(), default_backend())

    bio_in = _lib.BIO_new_mem_buf(tra, len(tra))
    pkcs7 = _lib.PKCS7_sign(cert._x509, private_key._evp_pkey, _ffi.NULL, bio_in, 0)

    bio_out = _lib.BIO_new(_lib.BIO_s_mem())
    _lib.PEM_write_bio_PKCS7(bio_out, pkcs7)

    result_buffer = _ffi.new('char**')
    buffer_length = _lib.BIO_get_mem_data(bio_out, result_buffer)
    sout = _ffi.buffer(result_buffer[0], buffer_length)[:]

    sout = '\n'.join(sout.decode('utf-8').splitlines()[1:-1])  # remove first and last line
    return sout


def _login(cms):
    client = Client(wsaa_wsdl)
    response = client.service.loginCms(in0=cms)
    return etree.fromstring(response.encode('utf-8'))


def get_ta_sign_token(service):
    tra = _create_tra(service)
    cms = _create_cms(tra)
    ta = _login(cms)
    ta_sign = ta.find('credentials').find('sign').text
    ta_token = ta.find('credentials').find('token').text
    return ta_sign, ta_token