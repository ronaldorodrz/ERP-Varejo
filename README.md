# ERP de Varejo

Sistema de estoque em Python desenvolvido para a disciplina de Algoritmos e Estruturas de Dados da UNIFAN. Pelo terminal, é possível cadastrar produtos e fornecedores, registrar entradas e saídas, desfazer a última movimentação e consultar a fila de reposição.

## Organização

| Pasta | Conteúdo |
| --- | --- |
| `Versão Base/` | ERP da Parte 1. O cadastro usa uma lista, a busca percorre os produtos por código e o Selection Sort ordena o relatório por estoque. |
| `Versão Otimizado/` | ERP da Parte 2. O cadastro usa uma árvore AVL, o relatório usa Merge Sort e a fila de reposição é reaproveitada enquanto está atualizada. |
| `Testes/` | Scripts que verificam os resultados e comparam o desempenho das duas versões. |

## Como executar

Com Python 3 instalado, abra o terminal na pasta que contém as três pastas acima. Para iniciar a versão otimizada, execute:

```sh
python "Versão Otimizado/ERP de Varejo 2.py"
```

Para iniciar a versão base, execute:

```sh
python "Versão Base/ERP de Varejo.py"
```

Use as opções numeradas do menu. Os cadastros ficam em memória durante a execução.

## Testes de desempenho

Execute cada comparação a partir da mesma pasta:

```sh
python "Testes/comparar_busca.py"
python "Testes/comparar_insercao_remocao.py"
python "Testes/comparar_ordenação.py"
python "Testes/comparar_fila.py"
```

Os testes usam 100, 1.000 e 10.000 produtos em ordem crescente, inversa e aleatória. O embaralhamento usa a semente 42. Cada resultado mostra a mediana de cinco medições em milissegundos.

## Integrantes

Ronaldo Rodrigues Pedreira, Rhuan Costa Andrade e Gildo Queiroz da Silva Júnior.
