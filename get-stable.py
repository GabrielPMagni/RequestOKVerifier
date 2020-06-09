# Importa bibliotecas necessárias
import requests as rq
import argparse
# Permite receber parâmetros ao iniciar programa
parser = argparse.ArgumentParser(description='Verifica código de status de um domínio via HTTP.')
parser.add_argument('dominio', type=str, help='O domínio a ser testado.')
parser.add_argument('-v', '--verbose', action='store_true', help='Aumenta o nível de verbosidade para a saída.')
args = parser.parse_args()
# Valida a URL
def validate_url(site):
    # Retira espaços desnecessários no argumento e deixa em minúsculo
    site = site.lower().strip()
    # Retira "https://" e substitui por "http://"
    if ('https://' in site):
        if (args.verbose in args):
            print('SSL não suportado, alterando para HTTP.')
        site = site.replace('https://', 'http://') 
    # Se não existir "http://" na URL, é inserida
    if ('http://' not in site):
        site = 'http://' + site
    # Substitui "http://www." por "http://"
    if ('http://www.' in site):
        site = site.replace('http://www.', 'http://')
    # Substitui "https://www." por "http://"
    if ('https://www.' in site):
        site = site.replace('https://www.', 'http://')
    # Retorna o texto da URL formatada
    return site


# Mostra o resultado da URL passada
def show_url():
    print('Website: ' + site)


# Se for verboso
def show_status_code(site):
    try:
        # Armazena em "x" valor inteiro do Status Code da URL passada
        x = rq.get(site).status_code
        show_url()
        # Verifica resultado e mostra texto baseado
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
        exit(x)

    # Caso haja um erro de conexão
    except rq.ConnectionError as e:
        print('Não foi possível estabelecer conexão.')
        exit(-1)

    # Caso haja algum outro erro
    except Exception as e:
        print(str(e))
        exit(-2)


# Se não for verboso
def return_status_code(site):
    try:
        # Armazena em "x" valor inteiro do Status Code da URL passada
        x = rq.get(site).status_code
        # Retorna o valor de status code como inteiro como saída
        exit(x)
    # Caso haja um erro de conexão
    except rq.ConnectionError:
        exit(-1)
    # Caso haja algum outro erro
    except Exception:
        exit(-2)


site = validate_url(args.dominio)
# Testa verbosidade
if (args.verbose):
    show_status_code(site)
else:
    return_status_code(site)