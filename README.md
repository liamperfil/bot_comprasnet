# bot_comprasnet

O que ainda preciso fazer?
```py
qtd_itens_na_cotacao = int(input("Digite a quantidade de itens na cotação: "))
meu_preco = [0] * qtd_itens_na_cotacao
for i, _ in enumerate(meu_preco):
    print("Digite o menor preco para o item ", str(i+1), ": ")
    meu_preco[i] = float(input())
```