import requests
from time import sleep

def resolve_simple_captcha(image_base64):
            CAPTCHA_API_KEY = 'e00087e2ee1a7d2b357231746ce1884b'

            payload = {
                    'method':'base64',
                    'key':CAPTCHA_API_KEY,
                    'body': image_base64
                }

            r = requests.post('https://2captcha.com/in.php', data=payload)
             
            if len(r.text.split('|')) > 1:
                captcha_id = r.text.split('|')[1]
                captcha_res_url = 'http://2captcha.com/res.php?key='+CAPTCHA_API_KEY+'&action=get&id='+captcha_id
                captcha_answer = requests.get(captcha_res_url).text
                while captcha_answer == None or 'CAPCHA_NOT_READY' in captcha_answer :
                    sleep(4)
                    captcha_res_url = 'http://2captcha.com/res.php?key='+CAPTCHA_API_KEY+'&action=get&id='+captcha_id
                    try:
                        captcha_answer = requests.get(captcha_res_url).text
                    except Exception as e:
                        print('Ha ocurrido un error: '+str(e))
                        sleep(4)
                        captcha_answer = None
                print(captcha_answer)
                if 'ERROR_CAPTCHA_UNSOLVABLE' in captcha_answer:
                    captcha_answer = False
                    print('ERROR_CAPTCHA_UNSOLVABLE')
                else:
                    captcha_answer = captcha_answer.split('|')[1]
            else:
                captcha_answer = False
                print('Ocurrió un error al obtener el captcha id.')
            return captcha_answer