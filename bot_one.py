from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from re import sub # modulo de expressões regulares (regex)
from random import uniform
from time import sleep

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver

def conv_float(str_value):
      float_value = sub(r'[^\d,]', '', str_value)
      float_value = float(float_value.replace(',', '.'))
      return float_value

num_dispensa = input("Digite o número da dispensa: ")
item = 1
meu_preco = input(f"Digite o preço do item {item}: ")
meu_preco = conv_float(meu_preco)
print(f'\033[7;35;40m Confira seu preço, você digitou: {meu_preco} \033[m')

# Inicializa o navegador webdriver Chrome E Abre uma página da web
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + num_dispensa)

xpath_status_disputa = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[8]/span'
xpath_preco_registrado = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[7]'
xpath_frm_preco = '//*[@id="txtFrmPreco' + str(item-1) + '"]'

try:
    # Para isso funcionar crie um arquivo senha.py com as variaveis "senha" e "cnpj"
    with open(r'C:\ambiente_virtual\senha.py', 'rb') as resposta:
        conteudo_arquivo = resposta.read()
    exec(conteudo_arquivo.decode())
    WebDriverWait(navegador, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="txtCnpj"]')))
    navegador.find_element("xpath", '//*[@id="txtSenha"]').click()
    navegador.find_element("xpath", '//*[@id="txtSenha"]').send_keys(senha)
    navegador.find_element("xpath", '//*[@id="txtCnpj"]').click()
    navegador.find_element("xpath", '//*[@id="txtCnpj"]').send_keys(cnpj)
    navegador.find_element("xpath", '//*[@id="btnAcessar"]').click()
except:
    print(r'Não localizamos o diretorio C:\ambiente_virtual\senha.py')

print('\033[1;34;40m Preencha a autenticação no site \033[m')
print('\033[1;34;40m Após credenciar pressione qualquer tecla para continuar... \033[m')
input('')

while True:
    try:
        status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Texto Você vence! ou Você perde!
        preco_registrado = navegador.find_element("xpath", xpath_preco_registrado).text # recebe preço em string
        preco_registrado = conv_float(preco_registrado) # converter preço em número
    except:
        break
    
    while (status_disputa == "Você perde!" and preco_registrado > meu_preco):
        try:
            preco_registrado -= uniform(0.01, 0.10) # Lance entre 1 centavo e 1 real para não ficar uniforme
            frm_preco = navegador.find_element("xpath", xpath_frm_preco) # Campo formulario de lance
            frm_preco.clear()
            frm_preco.send_keys("{:.4f}".format(preco_registrado)) # Enviando lances com 4 casas decimais
            btn_enviar_preco = navegador.find_element("xpath", '//*[@id="btnCotarPrecoRodape"]').click() # Botao cotar preço
            WebDriverWait(navegador, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCotarPrecoRodape"]')))
            status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Atualiza Você vence! ou Você perde!
            preco_registrado = navegador.find_element("xpath", xpath_preco_registrado).text # Atualiza o preço
            preco_registrado = conv_float(preco_registrado) # Converte preço em número
        except:
            break
    
    if (preco_registrado < meu_preco):
        print('\033[1;33;41m PREÇO ABAIXO DO VALOR REGISTRADO!!! \033[m')
        break

    while (status_disputa == "Você vence!"):
        navegador.refresh()
        sleep(0.1)
        try:
            status_disputa = navegador.find_element("xpath", xpath_status_disputa).text
        except:
            break

    # Verifica se ainda está em disputa
    try:
        WebDriverWait(navegador, 60).until(EC.presence_of_element_located((By.XPATH, xpath_status_disputa)))
        continue
    except:
        break

input('\033[7;35;40m Pressione qualquer tecla para encerrar... \033[m')