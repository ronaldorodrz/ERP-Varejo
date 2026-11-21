import erp_base
from time import perf_counter
from statistics import median
import random

quantidade = 10000

codigos = list(range(1, quantidade + 1))
random.Random(42).shuffle(codigos)

for codigo in codigos:
    produto = erp_base.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
    erp_base.produtos.append(produto)

for codigo_buscado in [quantidade, quantidade + 1]:
    tempos = []

    for repeticao in range(5):
        inicio = perf_counter()
        resultado = erp_base.buscar_produto(codigo_buscado)
        fim = perf_counter()

        tempo_ms = (fim - inicio) * 1000
        tempos.append(tempo_ms)

    print(f"\nCódigo buscado: {codigo_buscado}")
    print("Resultado:", resultado)
    print("Tempos das 5 buscas (ms):", tempos)
    print(f"Mediana: {median(tempos):.6f} ms")