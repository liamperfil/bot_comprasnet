# pip install selenium
# pip install webdriver-manager
# pip install chromedriver-binary
# pip install getpass

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

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver

def ValorNumerico(StrValor):
      numero = re.sub('[^\d,]', '', StrValor)
      numero = float(numero.replace(',', '.'))
      return numero

print("Digite o número da dispensa: ")
NumeroDispensa = input()
cnpj = " 50120844000144"
senha = getpass.getpass("Digite sua senha: ")
MeuPreco = 7300.0

# Inicializa o navegador webdriver Chrome
navegador = webdriver.Chrome(service=servico)

# Abre uma página da web
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + NumeroDispensa)

# Antes de continuar aguardar o XPATH CNPJ e SENHA até um prazo de 300 segundos (5 min)
aguardar_xpath = WebDriverWait(navegador, 300).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="txtCnpj"]'))
)
aguardar_xpath = WebDriverWait(navegador, 300).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="txtSenha"]'))
)

# Preencher os dados de login e senha
elemento = navegador.find_element("xpath", '//*[@id="txtCnpj"]')

for char in cnpj:
    elemento.send_keys(char)
    time.sleep(0.1)

elemento = navegador.find_element("xpath", '//*[@id="txtSenha"]')

for char in senha:
    elemento.send_keys(char)
    time.sleep(0.1)
    
elemento = navegador.find_element("xpath", '//*[@id="btnAcessar"]').click()

# Verifica se a disputa encerrou, aguardar o XPATH Você vence! ou Você perde! até um prazo de 10 segundos
XpathVencePerde = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[4]/td[8]/span'
try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, XpathVencePerde)))
    EmDisputa = True
except:
    EmDisputa = False

while (EmDisputa):
    TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text # Texto Você vence! ou Você perde!
    ChecarPreco = navegador.find_element("xpath", '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[4]/td[7]').text # recebe preço em string
    ChecarPreco = ValorNumerico(ChecarPreco) # converter preço em número
    
    while (TxtVencePerde == "Você perde!" and ChecarPreco > MeuPreco):
        ChecarPreco -= random.uniform(0.01, 1) # Lance entre 1 centavo e 1 real para não ficar uniforme
        elemento = navegador.find_element("xpath", '//*[@id="txtFrmPreco0"]') # Campo formulario de lance
        elemento.send_keys("{:.4f}".format(ChecarPreco)) # Enviando lances com 4 casas decimais
        elemento = navegador.find_element("xpath", '//*[@id="btnCotarPrecoRodape"]').click() # Botao cotar preço
        
        # O comando abaixo aguarda o usuario marcar o captcha e confirmar o lance
        # Ao fazer isso o xpath fica disponível e o fluxo segue
        aguardar_xpath = WebDriverWait(navegador, 300).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCotarPrecoRodape"]'))
        )
        TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text # Atualiza Você vence! ou Você perde!
        ChecarPreco = navegador.find_element("xpath", '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[4]/td[7]').text # Atualiza o preço
        ChecarPreco = ValorNumerico(ChecarPreco) # Converte preço em número

    while (TxtVencePerde == "Você vence!"):
        navegador.refresh()
        time.sleep(1)
        TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text

    # Verifica se ainda está em disputa
    try:
        WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, XpathVencePerde)))
        EmDisputa = True
    except:
        EmDisputa = False
        print("Mensagem: disputa encerrada")

time.sleep(10)

# //*[@id="Dados"]/div[4]/table/thead/tr/th[3]
# //*[@id="btnMostrarDetalhe"]
# //*[@id="btnVoltar"]