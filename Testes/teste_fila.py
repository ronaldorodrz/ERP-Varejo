import random
from statistics import median
from time import perf_counter

import erp_base

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        codigos = list(range(1, quantidade + 1))

        if ordem == "inversa":
            codigos.reverse()
        elif ordem == "aleatória":
            random.Random(42).shuffle(codigos)

        erp_base.produtos.clear()

        for codigo in codigos:
            # Estoques 0 e 1 precisam de reposição. Estoque 2 está no mínimo.
            estoque = codigo % 3
            produto = erp_base.Produto(
                codigo, "Mouse", "Informática", 19.90, estoque, 2
            )
            erp_base.produtos.append(produto)

        tempos_montagem = []
        tempos_retirada = []

        for repeticao in range(5):
            inicio = perf_counter()
            erp_base.atualizar_fila_prioridade()
            fila_pronta = perf_counter()

            item = erp_base.fila_prioridade.remover()
            fim = perf_counter()

            if item is None or item["produto"].estoque != 0:
                raise ValueError("A fila deveria retirar um produto esgotado.")

            tempos_montagem.append((fila_pronta - inicio) * 1000)
            tempos_retirada.append((fim - fila_pronta) * 1000)

        print(
            f"{quantidade} produtos | {ordem} | "
            f"montar fila: {median(tempos_montagem):.6f} ms | "
            f"retirar maior prioridade: {median(tempos_retirada):.6f} ms"
        )