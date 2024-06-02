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

def conv_float(str_value):
      float_value = sub('[^\d,]', '', str_value)
      float_value = float(float_value.replace(',', '.'))
      return float_value

#########################################
num_dispensa = input("Digite o número da dispensa: ")
cnpj = " " + input("Digite o cnpj: ")
senha = str(getpass.getpass("Digite sua senha: "))
meu_preco = input("Digite o preço do item x: ")
meu_preco = conv_float(meu_preco)
item = 1
#########################################

# Inicializa o navegador webdriver Chrome E Abre uma página da web
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + num_dispensa)

# Preencher os dados de login e senha
try:
    WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="txtCnpj"]')))
    navegador.find_element("xpath", '//*[@id="txtCnpj"]').send_keys(cnpj)
    navegador.find_element("xpath", '//*[@id="txtSenha"]').send_keys(senha)
    navegador.find_element("xpath", '//*[@id="btnAcessar"]').click()
except:
    input('Insira as credenciais manualmente')

xpath_status_disputa = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[8]/span'
xpath_preco_registrado = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[7]'
xpath_frm_preco = '//*[@id="txtFrmPreco' + str(item-1) + '"]'

input('Pressione qualquer tecla para continuar...')

while True:
    try:
        #status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Texto Você vence! ou Você perde!
        preco_registrado = navegador.find_element("xpath", xpath_preco_registrado).text # recebe preço em string
        preco_registrado = conv_float(preco_registrado) # converter preço em número
    except:
        break
    
    #while (status_disputa == "Você perde!" and preco_registrado > meu_preco):
    while (preco_registrado > meu_preco):
        try:
            preco_registrado -= uniform(0.01, 1) # Lance entre 1 centavo e 1 real
            frm_preco = navegador.find_element("xpath", xpath_frm_preco) # Campo formulario de lance
            frm_preco.send_keys("{:.4f}".format(preco_registrado)) # Enviando lances com 4 casas decimais
            btn_enviar = navegador.find_element("xpath", '//*[@id="btnCotarPrecoRodape"]').click() # Botao cotar preço
            
            while True:
                status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Texto Você vence! ou Você perde!
                if (status_disputa == "Você vence!"):
                    navegador.refresh()
                    sleep(0.1)
                else:
                    preco_registrado = navegador.find_element("xpath", xpath_preco_registrado).text # Atualiza o preço
                    preco_registrado = conv_float(preco_registrado) # Converte preço em número
                    preco_registrado -= uniform(0.01, 1) # Lance entre 1 centavo e 1 real
                    break
            
            # Aqui precisamos definir o formulario de lance 
            # Aqui precisamos definir o formulario de lance 
            # Aqui precisamos definir o formulario de lance 
            # Aqui precisamos definir o formulario de lance 
            try:
                WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, xpath_status_disputa)))
                continue
            except:
                break
        except:
            break

input(r'\033[1;33;41m O programa foi encerrado! \033[m')