import random
from statistics import median
from time import perf_counter

import erp_base
import erp_otimizado


def comparar(quantidade, ordem):
    codigos = list(range(1, quantidade + 1))

    if ordem == "inversa":
        codigos.reverse()
    elif ordem == "aleatória":
        random.Random(42).shuffle(codigos)

    insercoes_base = []
    insercoes_avl = []
    remocoes_base = []
    remocoes_avl = []

    for repeticao in range(5):
        erp_base.produtos.clear()
        arvore = erp_otimizado.ArvoreAVL()

        for codigo in codigos:
            erp_base.produtos.append(
                erp_base.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
            )
            arvore.inserir(
                erp_otimizado.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
            )

        # Inserção: procurar um código livre e cadastrar o produto.
        novo_codigo = quantidade + 1
        novo_base = erp_base.Produto(novo_codigo, "Teclado", "Informática", 89.90, 3, 1)
        novo_avl = erp_otimizado.Produto(novo_codigo, "Teclado", "Informática", 89.90, 3, 1)

        inicio = perf_counter()
        if erp_base.buscar_produto(novo_codigo) is None:
            erp_base.produtos.append(novo_base)
        insercoes_base.append((perf_counter() - inicio) * 1000)

        inicio = perf_counter()
        if arvore.buscar(novo_codigo) is None:
            arvore.inserir(novo_avl)
        insercoes_avl.append((perf_counter() - inicio) * 1000)

        if (erp_base.buscar_produto(novo_codigo) is not novo_base
                or arvore.buscar(novo_codigo) is not novo_avl):
            print(quantidade, ordem, "Falha na inserção")
            return

        # Retira o produto extra antes de medir a remoção.
        erp_base.produtos.pop()
        arvore.remover(novo_codigo)

        # Remove um produto que já existia nos dados originais.
        alvo = quantidade

        inicio = perf_counter()
        erp_base.remover_produto_por_codigo(alvo)
        remocoes_base.append((perf_counter() - inicio) * 1000)

        inicio = perf_counter()
        if arvore.buscar(alvo) is not None:
            arvore.remover(alvo)
        remocoes_avl.append((perf_counter() - inicio) * 1000)

        if (erp_base.buscar_produto(alvo) is not None
                or arvore.buscar(alvo) is not None):
            print(quantidade, ordem, "Falha na remoção")
            return

    print(
        f"{quantidade:>5} | {ordem:<9} | inserção | "
        f"{median(insercoes_base):.6f} | {median(insercoes_avl):.6f} | OK"
    )
    print(
        f"{quantidade:>5} | {ordem:<9} | remoção  | "
        f"{median(remocoes_base):.6f} | {median(remocoes_avl):.6f} | OK"
    )


print("Total | Ordem     | Operação | Base (ms) | AVL (ms) | Resultado")

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        comparar(quantidade, ordem)