import requests as rq
import argparse

parser = argparse.ArgumentParser(description='Verifica código de status de um domínio via HTTP.')
parser.add_argument('dominio', type=str, help='O domínio a ser testado.')


args = parser.parse_args()
site = args.dominio

site = site.lower().strip()
if ('https://' in site):
    print('SSL não suportado, alterando para HTTP.')
    site = site.replace('https://', 'http://') 

if ('http://' not in site):
    site = 'http://' + site

if ('http://www.' in site):
    site = site.replace('http://www.', 'http://')

if ('https://www.' in site):
    site = site.replace('https://www.', 'http://')


print('Website: ' + site)
try:
    x = rq.get(site).status_code

    if (x >= 200 and x < 300):
        print('Conexão OK (200-299)')
    elif (x >= 300 and x <= 302):
        print('Movido, OK (300-302')
    elif (x == 400):
        print('Bad Request (400)')
    elif (x == 401 or x == 403):
        print('Não autorizado (401 ou 403)')
    elif (x == 404):
        print('Não Encontrado (404)')
    elif (x == 500):
        print('Erro no servidor (500)')
    elif (x == 502):
        print('Bad Gateway (502)')
    else:
        print('Outro Status: '+str(x))


except rq.ConnectionError as e:
    print('Não foi possível estabelecer conexão.')

except Exception as e:
    print(str(e))
