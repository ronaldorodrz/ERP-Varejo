import random
from statistics import median
from time import perf_counter

import erp_base

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        estoques = list(range(1, quantidade + 1))

        if ordem == "inversa":
            estoques.reverse()
        elif ordem == "aleatória":
            random.Random(42).shuffle(estoques)

        erp_base.produtos.clear()

        for codigo, estoque in enumerate(estoques, start=1):
            produto = erp_base.Produto(
                codigo, "Mouse", "Informática", 19.90, estoque, 2
            )
            erp_base.produtos.append(produto)

        tempos = []

        for repeticao in range(5):
            inicio = perf_counter()
            ordenados = erp_base.produtos_ordenados_por_estoque()
            fim = perf_counter()

            # O resultado deve conter todos os estoques, de 1 até quantidade.
            resultado = [produto.estoque for produto in ordenados]
            if resultado != list(range(1, quantidade + 1)):
                raise ValueError("O relatório retornou estoques fora da ordem esperada.")

            tempos.append((fim - inicio) * 1000)

        print(f"{quantidade} produtos | {ordem} | mediana: {median(tempos):.6f} ms")