from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from cryptography.fernet import Fernet

import re # modulo de expressões regulares (regex)
import random
import getpass # modulo para receber senhas sem exibi-las no terminal enquanto o usuário digita
import time

def converte_preco(preco_str):
      preco_float = re.sub('[^\d,]', '', preco_str)
      preco_float = float(preco_float.replace(',', '.'))
      return preco_float

chave = input("digite a chave: ").encode()
fernet = Fernet(chave)

cnpj = 'gAAAAABl674n5lqx8oqT0R9DYpsr1HkuSsw2_LIhtU5MY2Z4fXcWEhmEgR6wgbYLURKUcNoTxzHsGAS64EUX79rY4TsP0ZqgwA=='
cnpj = cnpj.encode()
cnpj = fernet.decrypt(cnpj).decode()

senha = 'gAAAAABl68J91nQsr0urGT4NrYAtdS2yDxZaolYyM5V0mVZKQG_oh_YDxICQHOXYHDD1Q_fdBjjZFAPCCXRVkmApmApgY1nf2w=='
senha = senha.encode()
senha = fernet.decrypt(senha).decode()

endereco = ""

#cnpj = input("Cole o cnpj: ")
#senha = getpass.getpass("Cole a senha: ")
#endereco = input("Cole o site")

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver
navegador = webdriver.Chrome(service=servico)
navegador.get(endereco)

xpath_btn_acessar = '//*[@id="btnAcessar"]'
elemento = navegador.find_element("xpath", xpath_btn_acessar).click()

xpath_frm_cnpj = '//*[@id="UserName"]'
elemento = navegador.find_element("xpath", xpath_frm_cnpj)
elemento.send_keys(cnpj)

xpath_frm_senha = '//*[@id="Password"]'
elemento = navegador.find_element("xpath", xpath_frm_senha)
elemento.send_keys(senha)

xpath_btn_entrar = '//*[@id="btn-login"]'
elemento = navegador.find_element("xpath", xpath_btn_entrar).click()

navegador.get(endereco)
# após autenticação usar get site novamente que já vai cair no site de lances
# talvez precise informar novamente marca e modelo tr tr

xpath_btn_enviar = '//*[@id="layBotaoEnviar"]/span'
xpath_frm_lance1 = '//*[@id="divValor_241994_"]/span[2]/span/input[1]'
xpath_melhor_preco1 = '//*[@id="divMelhorLance_241994_"]'

try:
    WebDriverWait(navegador, 60).until(EC.visibility_of_element_located((By.XPATH, xpath_frm_lance1)))
except:
    time.sleep(20)
    navegador.quit()

meu_preco = 99999
checar_preco = navegador.find_element("xpath", xpath_melhor_preco1).text # recebe preço em string
checar_preco = converte_preco(checar_preco) # converter preço em número

while (meu_preco < checar_preco):
    checar_preco -= random.uniform(0.01, 1)
    elemento = navegador.find_element("xpath", xpath_frm_lance1)
    elemento.send_keys("{:.4f}".format(checar_preco)) # Enviando lances com 4 casas decimais
    elemento = navegador.find_element("xpath", xpath_btn_enviar).click()
    
    checar_preco = navegador.find_element("xpath", xpath_melhor_preco1).text # recebe preço em string
    checar_preco = converte_preco(checar_preco) # converter preço em número

print("ATENCAO PRECO MUITO BAIXO")
print("AGUARDANDO USUARIO FINALIZAR A SESSAO")
time.sleep(600)