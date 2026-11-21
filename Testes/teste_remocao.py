import erp_base
from time import perf_counter
from statistics import median
import random

quantidade = 10000

codigos = list(range(1, quantidade + 1))

for codigo in codigos:
    produto = erp_base.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
    erp_base.produtos.append(produto)

produtos_originais = erp_base.produtos.copy()
codigo_alvo = quantidade
tempos = []

for repeticao in range(5):
    erp_base.produtos = produtos_originais.copy()

    inicio = perf_counter()
    removeu = erp_base.remover_produto_por_codigo(codigo_alvo)
    fim = perf_counter()

    if not removeu or len(erp_base.produtos) != quantidade - 1:
        print("Falha na remoção.")
        break

    if erp_base.buscar_produto(codigo_alvo) is not None:
        print("O produto ainda está na lista.")
        break

    tempos.append((fim - inicio) * 1000)

if len(tempos) == 5:
    print("Código removido em cada repetição:", codigo_alvo)
    print("Tempos das 5 remoções (ms):", tempos)
    print(f"Mediana: {median(tempos):.6f} ms")