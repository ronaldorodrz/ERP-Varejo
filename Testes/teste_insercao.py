import erp_base
from time import perf_counter
from statistics import median
import random

quantidade = 10000

codigos = list(range(quantidade, 0, -1))

for codigo in codigos:
    produto = erp_base.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
    erp_base.produtos.append(produto)

novo = erp_base.Produto(quantidade + 1, "Teclado", "Informática", 89.90, 3, 1)
tempos = []

for repeticao in range(5):
    inicio = perf_counter()

    if erp_base.buscar_produto(novo.codigo) is None:
        erp_base.produtos.append(novo)

    fim = perf_counter()

    if erp_base.produtos[-1] is not novo:
        print("O produto de teste não foi inserido.")
        break

    tempos.append((fim - inicio) * 1000)
    erp_base.produtos.pop()

if len(tempos) == 5 and len(erp_base.produtos) == quantidade:
    print("Produtos antes de cada inserção:", quantidade)
    print("Código inserido:", novo.codigo)
    print("Tempos das 5 inserções (ms):", tempos)
    print(f"Mediana: {median(tempos):.6f} ms")