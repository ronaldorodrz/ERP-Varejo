import random
from statistics import median
from time import perf_counter

import erp_base
import erp_otimizado


def preparar_produtos(codigos):
    erp_base.produtos.clear()
    erp_otimizado.produtos = erp_otimizado.ArvoreAVL()

    for posicao, codigo in enumerate(codigos, start=1):
        estoque = codigo % 3

        produto_base = erp_base.Produto(
            codigo, "Mouse", "Informática", 19.90, estoque, 2
        )
        erp_base.produtos.append(produto_base)

        produto_otimizado = erp_otimizado.Produto(
            codigo, "Mouse", "Informática", 19.90, estoque, 2
        )
        produto_otimizado.ordem_cadastro = posicao
        erp_otimizado.produtos.inserir(produto_otimizado)


def medir_fila(erp, codigo_esperado):
    montagem = []
    segunda_chamada = []
    retirada = []

    for repeticao in range(5):
        # Faz cada repetição começar com uma montagem completa.
        if erp is erp_otimizado:
            erp.marcar_fila_desatualizada()

        inicio = perf_counter()
        erp.atualizar_fila_prioridade()
        fim = perf_counter()
        montagem.append((fim - inicio) * 1000)

        # O estoque continua igual nas duas versões.
        inicio = perf_counter()
        erp.atualizar_fila_prioridade()
        fim = perf_counter()
        segunda_chamada.append((fim - inicio) * 1000)

        inicio = perf_counter()
        item = erp.fila_prioridade.remover()
        fim = perf_counter()
        retirada.append((fim - inicio) * 1000)

        if item is None or item["produto"].codigo != codigo_esperado:
            raise ValueError(f"{erp.__name__}: retirada incorreta. Esperado {codigo_esperado}.")

    return median(montagem), median(segunda_chamada), median(retirada)


print("Total | Ordem | Versão | Montagem (ms) | 2ª chamada (ms) | Retirada (ms)")

for quantidade in [100, 1000, 10000]:
    for ordem in ["crescente", "inversa", "aleatória"]:
        codigos = list(range(1, quantidade + 1))

        if ordem == "inversa":
            codigos.reverse()
        elif ordem == "aleatória":
            random.Random(42).shuffle(codigos)

        preparar_produtos(codigos)

        # Entre os esgotados, deve sair o primeiro cadastrado.
        for codigo in codigos:
            if codigo % 3 == 0:
                codigo_esperado = codigo
                break

        for nome, erp in [("Base", erp_base), ("Otimizada", erp_otimizado)]:
            montagem, segunda, retirada = medir_fila(erp, codigo_esperado)
            print(
                f"{quantidade:>5} | {ordem:<9} | {nome:<9} | "
                f"{montagem:.6f} | {segunda:.6f} | {retirada:.6f}",
                flush=True
            )