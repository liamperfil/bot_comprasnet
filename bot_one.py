# pip install selenium
# pip install webdriver-manager
# pip install chromedriver-binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from re import sub # modulo de expressões regulares (regex)
from random import uniform
import getpass # modulo para receber senhas sem exibi-las no terminal enquanto o usuário digita
from time import sleep

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver

def ValorNumerico(StrValor):
      numero = sub('[^\d,]', '', StrValor)
      numero = float(numero.replace(',', '.'))
      return numero

#########################################
NumeroDispensa = input("Digite o número da dispensa: ")
cnpj = " " + input("Digite o cnpj: ")
senha = str(getpass.getpass("Digite sua senha: "))
iMeuPreco = input("Digite o preço do item x: ")
MeuPreco = ValorNumerico(iMeuPreco)
#########################################

# Inicializa o navegador webdriver Chrome E Abre uma página da web
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + NumeroDispensa)

# Preencher os dados de login e senha
try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtCnpj"]')))
    navegador.find_element("xpath", '//*[@id="txtCnpj"]').send_keys(cnpj)
    navegador.find_element("xpath", '//*[@id="txtSenha"]').send_keys(senha)
    navegador.find_element("xpath", '//*[@id="btnAcessar"]').click()
except:
    input('Insira as credenciais manualmente')

item = 1
XpathVencePerde = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[8]/span'
xpath_checar_preco = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[7]'
xpath_frm_preco = '//*[@id="txtFrmPreco' + str(item-1) + '"]'

input('Pressione qualquer tecla para continuar...')

while True:
    try:
        TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text # Texto Você vence! ou Você perde!
        ChecarPreco = navegador.find_element("xpath", xpath_checar_preco).text # recebe preço em string
        ChecarPreco = ValorNumerico(ChecarPreco) # converter preço em número
    except:
        break
    
    while (TxtVencePerde == "Você perde!" and ChecarPreco > MeuPreco):
        try:
            ChecarPreco -= uniform(0.01, 1) # Lance entre 1 centavo e 1 real para não ficar uniforme
            elemento = navegador.find_element("xpath", xpath_frm_preco) # Campo formulario de lance
            elemento.send_keys("{:.4f}".format(ChecarPreco)) # Enviando lances com 4 casas decimais
            elemento = navegador.find_element("xpath", '//*[@id="btnCotarPrecoRodape"]').click() # Botao cotar preço
            WebDriverWait(navegador, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCotarPrecoRodape"]')))
            TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text # Atualiza Você vence! ou Você perde!
            ChecarPreco = navegador.find_element("xpath", xpath_checar_preco).text # Atualiza o preço
            ChecarPreco = ValorNumerico(ChecarPreco) # Converte preço em número
        except:
            break
    
    if (ChecarPreco < MeuPreco):
        print('PREÇO ABAIXO DO VALOR REGISTRADO!!!')

    while (TxtVencePerde == "Você vence!"):
        navegador.refresh()
        sleep(0.1)
        try:
            TxtVencePerde = navegador.find_element("xpath", XpathVencePerde).text
        except:
            break

    # Verifica se ainda está em disputa
    try:
        WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, XpathVencePerde)))
        continue
    except:
        break

input('Pressione qualquer tecla para encerrar...')
