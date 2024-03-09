from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from cryptography.fernet import Fernet

import re
import random
import getpass
import time

def converte_preco_float(preco_str):
      preco_float = re.sub('[^\d,]', '', preco_str)
      preco_float = float(preco_float.replace(',', '.'))
      return preco_float

def converte_preco_str(preco_float):
      preco_str = re.sub('[^\d.]', '', preco_float)
      preco_str = str(preco_str.replace('.', ','))
      return preco_str

def melhor_preco(f_item):
    xpath_cd = '//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl01_hidCdItem"]'
    valor_cd = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    valor_cd = f_item + int(valor_cd)
    xpath_melhor_preco = '//*[@id="divMelhorLance_' + str(valor_cd) + '_"]'
    melhor_preco_reg = navegador.find_element("xpath", xpath_melhor_preco).text # recebe preço em string
    melhor_preco_reg = converte_preco_float(melhor_preco_reg)
    return melhor_preco_reg

def func_em_disputa(f_item):
    xpath_cd = '//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl01_hidCdItem"]'
    compra_direta = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    compra_direta = f_item + int(compra_direta)
    xpath_frm_lance = '//*[@id="divValor_' + compra_direta + '_"]/span[2]/span/input[1]'
    try:
        WebDriverWait(navegador, 5).until(EC.visibility_of_element_located((By.XPATH, xpath_frm_lance)))
        return True
    except:
        return False
    
def xpath_frm_lance(f_item):
    xpath_cd = '//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl01_hidCdItem"]'
    compra_direta = navegador.find_element("xpath", xpath_cd).get_attribute('value')
    compra_direta = f_item + int(compra_direta)
    xpath = '//*[@id="divValor_' + compra_direta + '_"]/span[2]/span/input[1]'
    return xpath

endereco = ""
meu_preco = 999999, 0, 333 # Isso é uma tupla, se for um item só é necessario que termine em virgula
chave = input("digite a chave: ").encode()

quant_item = len(meu_preco)
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

xpath_btn_enviar = '//*[@id="layBotaoEnviar"]/span'

navegador.get(endereco)

em_disputa = [None] * quant_item
for i, x in enumerate(em_disputa):
    em_disputa[i] = func_em_disputa(i)

# talvez precise informar novamente marca e modelo tr tr
# talvez precise informar novamente marca e modelo tr tr
# talvez precise informar novamente marca e modelo tr tr

while (any(em_disputa)):
    item = 0
    while (item < quant_item):
        if (meu_preco[item] != 0 and em_disputa[item] and meu_preco[item] < melhor_preco(item)):
            lance = melhor_preco(item)
            lance -= random.uniform(0.01, 1)
            lance = "{:.2f}".format(lance)
            lance = converte_preco_str(lance)
            elemento = navegador.find_element("xpath", xpath_frm_lance(item))
            elemento.send_keys(lance)
            for i, x in enumerate(em_disputa):
                em_disputa[i] = func_em_disputa(i)
        item += 1
    elemento = navegador.find_element("xpath", xpath_btn_enviar).click()

print("ATENCAO PRECO MUITO BAIXO")
print("AGUARDANDO USUARIO FINALIZAR A SESSAO")
time.sleep(600)

#//*[@id="divValor_242376_"]/span[2]/span/input[1]
#//*[@id="divValor_242377_"]/span[2]/span/input[1]
#//*[@id="divValor_242378_"]/span[2]/span/input[1]
#//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl01_hidCdItem"]
#//*[@id="dtgPesquisaAgrupada_ctl01_dtgPesquisaAgrupadaItens_ctl03_hidCdItem"]