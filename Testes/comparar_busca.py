import random
from statistics import median
from time import perf_counter

import erp_base
import erp_otimizado


def medir_busca(buscar, codigo):
    tempos = []

    for repeticao in range(5):
        inicio = perf_counter()
        resultado = buscar(codigo)
        fim = perf_counter()

        tempos.append((fim - inicio) * 1000)

    return resultado, median(tempos)


def comparar_buscas(quantidade, ordem):
    codigos = list(range(1, quantidade + 1))

    if ordem == "inversa":
        codigos.reverse()
    elif ordem == "aleatória":
        random.Random(42).shuffle(codigos)

    # Cada cenário começa com a lista e a árvore vazias.
    erp_base.produtos.clear()
    arvore = erp_otimizado.ArvoreAVL()

    # As duas versões recebem os mesmos códigos na mesma ordem.
    for codigo in codigos:
        produto_base = erp_base.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
        produto_avl = erp_otimizado.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)

        erp_base.produtos.append(produto_base)
        arvore.inserir(produto_avl)

    for alvo in [quantidade, quantidade + 1]:
        produto_base, tempo_base = medir_busca(erp_base.buscar_produto, alvo)
        produto_avl, tempo_avl = medir_busca(arvore.buscar, alvo)

        if alvo == quantidade:
            caso = "existente"
            correto = (
                produto_base is not None and produto_base.codigo == alvo
                and produto_avl is not None and produto_avl.codigo == alvo
            )
        else:
            caso = "ausente"
            correto = produto_base is None and produto_avl is None

        status = "OK" if correto else "VERIFICAR"
        print(
            f"{quantidade:>5} | {ordem:<9} | {alvo:>5} | {caso:<9} | "
            f"{tempo_base:.6f} | {tempo_avl:.6f} | {status}"
        )


print(" Total | Ordem     |  Alvo | Caso      | Base (ms) | AVL (ms) | Resultado")

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        comparar_buscas(quantidade, ordem)