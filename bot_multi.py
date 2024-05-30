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
from time import sleep

def converte_preco_float(str_valor):
    numero = sub(r'[^\d,]', '', str_valor)
    numero = float(numero.replace(',', '.'))
    return numero

num_dispensa = input("Cole o numero da dispensa: ")
num_dispensa = sub(r'[^\d]', '', num_dispensa)

servico = Service(ChromeDriverManager().install()) # Atualiza o webdriver
navegador = webdriver.Chrome(service=servico)
navegador.get("https://comprasnet3.ba.gov.br/Fornecedor/LoginDispensa.asp?txtFuncionalidade=&txtNumeroDispensa=" + num_dispensa)
sleep(1)

# Credenciais/Autenticação
print('----------------------------------------')
print('----------------------------------------')
print('\033[1;33;41m ATENÇÃO! Credencie e cadastre marca, modelo e preço. \033[m')
input("Pressione qualquer tecla para INICIAR...")

while True:
    try:
        quant_item = int(input('Digite a quantidade de itens na disputa: '))
        if quant_item <= 0:
            print("Por favor, insira um número inteiro positivo.")
            continue
        break
    except ValueError:
        print("Por favor, insira um número inteiro positivo.")

# Obter preços dos itens
meu_preco = []
for i in range(quant_item):
    while True:
        try:
            preco = input(f'Digite o preço para o item {i + 1}: ')
            preco = converte_preco_float(preco)
            meu_preco.append(preco)
            break
        except ValueError:
            print('\033[1;33;41m Digite um valor válido. \033[m')

em_disputa = [True] * quant_item
xpath_btn_enviar = '//*[@id="btnCotarPrecoRodape"]'

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
        print(f"Erro: def melhor_preco item: {f_item}")
        input("Pressione qualquer tecla para continuar...")

def xpath_frm_lance(f_item):
    xpath = '//*[@id="txtFrmPreco' + str(f_item) + '"]'
    return xpath

print('----------------------------------------')
input("Pressione qualquer tecla para INICIAR...")

while (any(em_disputa)):
    i, deu_lance = 0, False
    navegador.refresh()
    while (i < quant_item):
        em_disputa[i] = meu_preco[i] <= melhor_preco(i)
        if (meu_preco[i] != 0 and vence_perde(i) and em_disputa[i]):
            lance = melhor_preco(i)
            lance -= uniform(0.01, 0.1)
            try:
                elemento = navegador.find_element("xpath", xpath_frm_lance(i)) # Campo formulario de lance
                elemento.send_keys("{:.4f}".format(lance)) # Enviando lances com 4 casas decimais
            except:
                print(f"Erro aguardando xpath_frm_lance item: {i}")
                input("Pressione qualquer tecla para encerrar...")
            deu_lance = True
        i += 1
    if (deu_lance):
        try:
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
