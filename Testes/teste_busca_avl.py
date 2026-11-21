from time import perf_counter
from statistics import median
import erp_otimizado

# Cadastra na árvore os produtos de código 1 até 100.
for codigo in range(1, 101):
    produto = erp_otimizado.Produto(codigo, "Mouse", "Informática", 19.90, 5, 2)
    erp_otimizado.produtos.inserir(produto)

# O código 100 existe. O código 101 está ausente.
for codigo_buscado in [100, 101]:
    tempos = []

    for repeticao in range(5):
        inicio = perf_counter()
        resultado = erp_otimizado.buscar_produto(codigo_buscado)
        fim = perf_counter()

        tempo_ms = (fim - inicio) * 1000
        tempos.append(tempo_ms)

    print("Código buscado:", codigo_buscado)
    print("Resultado:", resultado)
    print(f"Mediana: {median(tempos):.6f} ms")
    print()