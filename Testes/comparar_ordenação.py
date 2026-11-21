import random
from statistics import median
from time import perf_counter

import erp_base
import erp_otimizado


def comparar_ordenacao(quantidade, ordem):
    estoques = list(range(1, quantidade + 1))

    if ordem == "inversa":
        estoques.reverse()
    elif ordem == "aleatória":
        random.Random(42).shuffle(estoques)

    erp_base.produtos.clear()
    arvore = erp_otimizado.ArvoreAVL()
    esperado = [None] * quantidade

    for codigo, estoque in enumerate(estoques, start=1):
        produto_base = erp_base.Produto(
            codigo, "Mouse", "Informática", 19.90, estoque, 2
        )
        produto_avl = erp_otimizado.Produto(
            codigo, "Mouse", "Informática", 19.90, estoque, 2
        )

        erp_base.produtos.append(produto_base)
        arvore.inserir(produto_avl)

        # Os estoques vão de 1 até quantidade, sem repetição.
        esperado[estoque - 1] = (estoque, codigo)

    tempos_base = []
    tempos_merge = []

    for repeticao in range(5):
        inicio = perf_counter()
        ordenados_base = erp_base.produtos_ordenados_por_estoque()
        fim = perf_counter()
        tempos_base.append((fim - inicio) * 1000)

        inicio = perf_counter()
        registros = arvore.em_ordem()
        ordenados_merge = erp_otimizado.merge_sort_por_estoque(registros)
        fim = perf_counter()
        tempos_merge.append((fim - inicio) * 1000)

        # Confere os dois resultados depois de parar o cronômetro.
        resultado_base = [(p.estoque, p.codigo) for p in ordenados_base]
        resultado_merge = [(p.estoque, p.codigo) for p in ordenados_merge]

        if resultado_base != esperado:
            print(f"{quantidade} | {ordem} | VERIFICAR VERSÃO BASE")
            return

        if resultado_merge != esperado:
            print(f"{quantidade} | {ordem} | VERIFICAR VERSÃO OTIMIZADA")
            return

    print(
        f"{quantidade:>5} | {ordem:<9} | "
        f"{median(tempos_base):.6f} | {median(tempos_merge):.6f} | OK",
        flush=True
    )


print("Total | Ordem     | Base (ms) | AVL + Merge Sort (ms) | Resultado")

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        comparar_ordenacao(quantidade, ordem)