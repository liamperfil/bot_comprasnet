```python
print("Hello, World")


def minhaFunc():
    i = 10
    while i > 0:
        print(i)
        i -= 1
minhaFunc()


abc = "abcdefg"
for x in abc:
    print(x)


exit()


if 5 > 2:
    print("Cinco é maior que dois.")


# Variáveis ​​não precisam ser declaradas tipo específico e podem até mudar de tipo depois de terem sido definidas.
# Se você quiser especificar o tipo de dados de uma variável, isso pode ser feito com conversão.

a = str(3)    # x will be '3'
b = int(3)    # y will be 3
c = float(3)  # z will be 3.0
d = str(y)    # y will be '3'


# Você pode obter o tipo de dados de uma variável com a função type().

print(type(x))
print(type(y))


# múltiplas variáveis

x, y, z = "Orange", "Banana", "Cherry"


# Um valor para múltiplas variáveis

x = y = z = "Orange"


# Python não tem uma função random() para criar números aleatórios
# mas possui um módulo interno chamado random que pode ser usado para criar números aleatórios:

import random
print(random.randrange(1, 10))
print(random.uniform(0.01, 1))


# A função len() retorna o comprimento de uma string:

a = "Hello, World!"
print(len(a))


# Para verificar se determinada frase ou caractere está presente em uma string, 
# podemos utilizar a palavra-chave in.

txt = "hoje temos sorvete"
print("hoje" in txt) # return true or false


if "temos" in txt:
    print(txt)


# metodos string

txt = "Hello, World!"
txt = txt[2:5] # return llo
txt = txt.strip() # remove espaços em branco do inicio e do fim
txt = txt.upper() # maiuscula
txt = txt.lower() # minuscula
txt = txt.replace("H", "J") # substituir
txt = txt.split(",") # returns ['Hello', ' World!']
txt = txt.find("lo") # Pesquisa a string por um valor especificado e retorna a posição onde ele foi encontrado
```