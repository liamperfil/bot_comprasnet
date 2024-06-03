from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

# Inicializa o navegador webdriver Chrome E Abre uma página da web
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + num_dispensa)

xpath_status_disputa = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[8]/span'
xpath_checar_preco = '//*[@id="frmCotarCotacaoEmDisputa"]/table/tbody/tr[' + str(4 * item) + ']/td[7]'
xpath_frm_preco = '//*[@id="txtFrmPreco' + str(item-1) + '"]'

print('\033[1;34;40m Credenciamento manual \033[m')
input('Pressione qualquer tecla para continuar...')

while True:
    try:
        status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Texto Você vence! ou Você perde!
        checar_preco = navegador.find_element("xpath", xpath_checar_preco).text # recebe preço em string
        checar_preco = conv_float(checar_preco) # converter preço em número
    except:
        break
    
    while (status_disputa == "Você perde!" and checar_preco > meu_preco):
        try:
            checar_preco -= uniform(0.01, 1) # Lance entre 1 centavo e 1 real para não ficar uniforme
            frm_preco = navegador.find_element("xpath", xpath_frm_preco) # Campo formulario de lance
            frm_preco.send_keys("{:.4f}".format(checar_preco)) # Enviando lances com 4 casas decimais
            btn_enviar_preco = navegador.find_element("xpath", '//*[@id="btnCotarPrecoRodape"]').click() # Botao cotar preço
            WebDriverWait(navegador, 300).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCotarPrecoRodape"]')))
            status_disputa = navegador.find_element("xpath", xpath_status_disputa).text # Atualiza Você vence! ou Você perde!
            checar_preco = navegador.find_element("xpath", xpath_checar_preco).text # Atualiza o preço
            checar_preco = conv_float(checar_preco) # Converte preço em número
        except:
            break
    
    if (checar_preco < meu_preco):
        print('PREÇO ABAIXO DO VALOR REGISTRADO!!!')

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

input('Pressione qualquer tecla para encerrar...')
