import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

print('''
Digite:
1 - Emitente
2 - Destinatário
''')
escolha_emi_dest = input()

print('''
1 - Amoêdo
2 - Beatriz
3 - Dsouza
4 - T. Julia
5 - Nex
''')

escolha = input('')

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

if (escolha_emi_dest == '1'):
    navegador.get('https://nfe.sefaz.ba.gov.br/servicos/NFENC/SSL/ASLibrary/Login?ReturnUrl=%2fservicos%2fnfenc%2fModulos%2fAutenticado%2fRestrito%2fNFENC_consulta_emitente.aspx#')
else:
    navegador.get('https://nfe.sefaz.ba.gov.br/servicos/NFENC/SSL/ASLibrary/Login?ReturnUrl=%2fservicos%2fnfenc%2fModulos%2fAutenticado%2fRestrito%2fNFENC_consulta_destinatario.aspx')

try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="details-button"]')))
    navegador.find_element('xpath', '//*[@id="details-button"]').click()
    navegador.find_element('xpath', '//*[@id="proceed-link"]').click()
except:
    input('Pressione qualquer tecla para continuar...')

if (escolha == '1'):
    login = '6964663400'
    senha = 'amo2015'

if (escolha == '2'):
    login = '11090770500'
    senha = '1109bea'

if (escolha == '3'):
    login = '20039854900'
    senha = 'souza22'

if (escolha == '4'):
    login = '14859928400'
    senha = 'bom1912'

if (escolha == '5'):
    login = '20517684700'
    senha = 'NEX3008'

try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="PHCentro_userLogin"]')))
    navegador.find_element('xpath', '//*[@id="PHCentro_userLogin"]').send_keys(login)
    navegador.find_element('xpath', '//*[@id="PHCentro_userPass"]').send_keys(senha)
except:
    input('Digite as credenciais manualmente')

input('Pressione qualquer tecla para continuar...')