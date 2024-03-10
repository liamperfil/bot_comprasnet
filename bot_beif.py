from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from cryptography.fernet import Fernet
from selenium.webdriver.common.keys import Keys

import re
import random
import getpass
import time

meu_preco = 500, 500, 500 # Isso é uma tupla, se for um item só é necessario que termine em virgula
endereco = input("Informe o endereço: ")
chave = input("Cole a chave: ").encode()
fernet = Fernet(chave)

cnpj = 'gAAAAABl674n5lqx8oqT0R9DYpsr1HkuSsw2_LIhtU5MY2Z4fXcWEhmEgR6wgbYLURKUcNoTxzHsGAS64EUX79rY4TsP0ZqgwA=='
cnpj = cnpj.encode()
cnpj = fernet.decrypt(cnpj).decode()

senha = 'gAAAAABl68J91nQsr0urGT4NrYAtdS2yDxZaolYyM5V0mVZKQG_oh_YDxICQHOXYHDD1Q_fdBjjZFAPCCXRVkmApmApgY1nf2w=='
senha = senha.encode()
senha = fernet.decrypt(senha).decode()

#cnpj = input("Cole o cnpj: ")
#senha = getpass.getpass("Cole a senha: ")
#endereco = input("Cole o site")

quant_item = len(meu_preco)

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver
navegador = webdriver.Chrome(service=servico)
navegador.get(endereco)

xpath_cd = '//*[@id="dtgPesquisaItens_ctl01_hidCdItem"]' # xpath compra direta
#xpath_cd = '//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl01_hidCdItem"]' # no caso de lote
xpath_btn_acessar = '//*[@id="btnAcessar"]' # Navegação antes da autenticação
xpath_frm_cnpj = '//*[@id="UserName"]'
xpath_frm_senha = '//*[@id="Password"]'
xpath_btn_entrar = '//*[@id="btn-login"]' # Login/Autenticação
xpath_btn_enviar = '//*[@id="layBotaoEnviar"]/span' # Enviar lance
xpath_btn_cookie = '//*[@id="btn-accept"]'

def converte_preco_float(preco_str):
      preco_float = re.sub('[^\d,]', '', preco_str)
      preco_float = float(preco_float.replace(',', '.'))
      return preco_float

def converte_preco_str(preco_float):
      preco_str = re.sub('[^\d.]', '', preco_float)
      preco_str = str(preco_str.replace('.', ','))
      return preco_str

def melhor_preco(f_item):
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_cd)))
        valor_cd = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    except:
        valor_cd = input("Digite o value da compra direta, ex: 112233")
    valor_cd = f_item + int(valor_cd)
    xpath_melhor_preco = '//*[@id="divMelhorLance_' + str(valor_cd) + '_"]'
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_melhor_preco)))
        melhor_preco_reg = navegador.find_element("xpath", xpath_melhor_preco).text # recebe preço em string
    except:
        melhor_preco_reg = input("Digite o melhor preço registrado para o item: ", (f_item+1))
    melhor_preco_reg = converte_preco_float(melhor_preco_reg)
    return melhor_preco_reg

def func_em_disputa(f_item):
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_cd)))
        valor_cd = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    except:
        valor_cd = input("Digite o value da compra direta, ex: 112233")
    valor_cd = f_item + int(valor_cd)
    xpath_frm_lance = '//*[@id="divValor_' + str(valor_cd) + '_"]/span[2]/span/input[1]'
    try:
        WebDriverWait(navegador, 2).until(EC.visibility_of_element_located((By.XPATH, xpath_frm_lance)))
        return True
    except:
        return False
    
def xpath_frm_lance(f_item):
    compra_direta = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    compra_direta = f_item + int(compra_direta)
    xpath = '//*[@id="divValor_' + str(compra_direta) + '_"]/span[2]/span/input[1]'
    return xpath

def xpath_marca(param):
    xpath = '//*[@id="dtgPesquisaItens_ctl' + str(param).zfill(2) + '_tbxMarca"]'
    return xpath

def xpath_modelo(param):
    xpath = '//*[@id="dtgPesquisaItens_ctl' + str(param).zfill(2) + '_tbxModelo"]'
    return xpath

try:
    WebDriverWait(navegador, 60).until(EC.element_to_be_clickable((By.XPATH, xpath_btn_acessar)))
    elemento = navegador.find_element("xpath", xpath_btn_acessar).click()
except:
    input('Nao encontrei o botao acessar, ENTER para continuar')

try:
    WebDriverWait(navegador, 2).until(EC.element_to_be_clickable((By.XPATH, xpath_btn_cookie)))
    elemento = navegador.find_element("xpath", xpath_btn_cookie).click()
except:
    print('Onde estao os cookies?')

try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, xpath_frm_cnpj)))
    elemento = navegador.find_element("xpath", xpath_frm_cnpj)
    elemento.send_keys(cnpj)
    elemento = navegador.find_element("xpath", xpath_frm_senha)
    elemento.send_keys(senha)
    elemento = navegador.find_element("xpath", xpath_btn_entrar).click() # Login/Autenticação
except:
    input('Verifique as credenciais, ENTER para continuar')

input("Pressione qualquer tecla para continuar...")

navegador.get(endereco)

em_disputa = [None] * quant_item
for i, x in enumerate(em_disputa):
    em_disputa[i] = func_em_disputa(i)
    if (em_disputa[i] and meu_preco[i] != 0 and meu_preco[i] < melhor_preco(i)):
        try:
            WebDriverWait(navegador, 1).until(EC.visibility_of_element_located((By.XPATH, xpath_marca(i+1))))
            elemento = navegador.find_element("xpath", xpath_marca(i+1)).send_keys("TR")
        except:
            print("marca não solicitada")
        try:
            WebDriverWait(navegador, 1).until(EC.visibility_of_element_located((By.XPATH, xpath_modelo(i+1))))
            elemento = navegador.find_element("xpath", xpath_modelo(i+1)).send_keys("TR")
        except:
            print("modelo não solicitado")

while (any(em_disputa)):
    item = 0
    while (item < quant_item):
        em_disputa[item] = func_em_disputa(item)
        if (meu_preco[item] != 0 and em_disputa[item] and meu_preco[item] < melhor_preco(item)):
            lance = melhor_preco(item)
            lance -= random.uniform(0.01, 1)
            lance = "{:.2f}".format(lance)
            lance = converte_preco_str(lance)
            try:
                WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_frm_lance(item))))
                WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_frm_lance(item))))
                elemento = navegador.find_element("xpath", xpath_frm_lance(item))
                time.sleep(0.1)
                elemento.send_keys(lance)
            except:
                print("Algo deu errado no item: ", (item+1))
                print("Digite seu preço manualmente.")
                input("Pressione qualquer tecla para continuar...")
        item += 1
    input("PRESSIONE QUALQUER TECLA PARA ENVIAR")
    #elemento = navegador.find_element("xpath", xpath_btn_enviar).click()


print("ATENCAO PRECO MUITO BAIXO")
input("PRESSIONE QUALQUER TECLA PARA FINALIZAR A SESSÃO")