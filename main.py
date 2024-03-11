# pip install selenium
# pip install webdriver-manager
# pip install chromedriver-binary

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import re # modulo de expressões regulares (regex)
import random
import getpass # modulo para receber senhas sem exibi-las no terminal enquanto o usuário digita
import time

num_dispensa = input("Cole o numero da dispensa: ")
cnpj = " " + input("Cole o cnpj: ")
senha = getpass.getpass("Digite sua senha: ")
meu_preco = 1111, 2222, 3333

quant_item = len(meu_preco)
em_disputa = True * quant_item
xpath_btn_enviar = '//*[@id="btnCotarPrecoRodape"]'

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + num_dispensa)

def converte_preco_float(str_valor):
      numero = re.sub('[^\d,]', '', str_valor)
      numero = float(numero.replace(',', '.'))
      return numero

def xpath_vence_perde(item):
    n_item = 4 * (item + 1)
    xpath = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(n_item) + ']/td[8]/span'
    return xpath

def vence_perde(param):
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_vence_perde(param))))
        elemento = navegador.find_element("xpath", xpath_vence_perde(param)).text
        if (elemento == "Você perde!"):
            return True
        if (elemento == "Você vence!"):
            return False
    except:
        print("Erro xpath_vence_perde")
        input("Pressione qualquer tecla para continuar...")
        return True

def melhor_preco(f_item):
    n_item = 4 * (f_item + 1)
    xpath = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(n_item) + ']/td[7]'
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
        preco = navegador.find_element("xpath", xpath).text
        preco = converte_preco_float(preco) # converter preço em número
        return preco
    except:
        print("Erro: def melhor_preco item: ", f_item)
        input("Pressione qualquer tecla para continuar...")

def xpath_frm_lance(f_item):
    xpath = '//*[@id="txtFrmPreco' + str(f_item) + '"]'
    return xpath

# Credenciais/Autenticação
try:
    WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="txtCnpj"]')))
    WebDriverWait(navegador, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="txtSenha"]')))
    elemento = navegador.find_element("xpath", '//*[@id="txtCnpj"]')
    for char in cnpj:
        elemento.send_keys(char)
        time.sleep(0.1)
    elemento = navegador.find_element("xpath", '//*[@id="txtSenha"]')
    for char in senha:
        elemento.send_keys(char)
        time.sleep(0.1)
    navegador.find_element("xpath", '//*[@id="btnAcessar"]').click()
except:
    print("Digite as credenciais manualmente.")
    input("Pressione qualquer tecla para continuar...")

while (any(em_disputa)):
    i = deu_lance = 0
    navegador.refresh()
    while (i < quant_item):
        em_disputa[i] = meu_preco[i] <= melhor_preco(i)
        if (meu_preco[i] != 0 and vence_perde(i) and em_disputa[i]):
            lance = melhor_preco(i)
            lance -= random.uniform(0.01, 1)
            try:
                WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.XPATH, xpath_frm_lance(i))))
                elemento = navegador.find_element("xpath", xpath_frm_lance(i)) # Campo formulario de lance
                elemento.send_keys("{:.4f}".format(lance)) # Enviando lances com 4 casas decimais
            except:
                print("Erro aguardando xpath_frm_lance item: ", i)
                input("Pressione qualquer tecla para encerrar...")
            deu_lance = True
        i += 1
    if (deu_lance):
        try:
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, xpath_btn_enviar)))
            navegador.find_element("xpath", xpath_btn_enviar).click()
        except:
            print("Erro aguardando xpath_btn_enviar")
            input("Pressione qualquer tecla para encerrar...")
        try:
            WebDriverWait(navegador, 300).until(EC.visibility_of_element_located((By.XPATH, xpath_btn_enviar)))
        except:
            print("Erro aguardando xpath_btn_enviar")
            input("Pressione qualquer tecla para encerrar...")

print("Disputa encerrada!")
input("Pressione qualquer tecla para encerrar...")