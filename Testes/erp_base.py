# MENU PRINCIPAL
def texto():
    print(f"""
--== ERP de Varejo - Estoque e Vendas ==--

1 - Cadastrar
2 - Consultar
3 - Alteração
4 - Remoção
5 - Movimentação de estoque
6 - Fila de prioridade
7 - Relatórios
8 - Desfazer última movimentação
0 - Sair
""")

# CLASSE PRODUTO
class Produto:
    def __init__(self, codigo, nome, categoria, preco, estoque, estoque_minimo):
        # Aqui guardamos os dados do produto dentro do objeto.
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.estoque = estoque
        self.estoque_minimo = estoque_minimo

    def __str__(self):
        # Define como o produto será exibido quando usarmos print(produto).
        return f"[{self.codigo}] {self.nome} / {self.categoria} - R$ {self.preco:.2f} (Estoque: {self.estoque} / Mínimo: {self.estoque_minimo})"

# CLASSE FORNECEDOR
class Fornecedor:
    def __init__(self, codigo, nome, telefone): 
        # Guarda os dados do fornecedor dentro do objeto.
        self.codigo = codigo
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        # Define como o fornecedor será exibido no print().
        return f"[{self.codigo}] {self.nome} / {self.telefone}"

# CLASSE FILA DE PRIORIDADE
class Prioridade:
    def __init__(self):
        # A lista "itens" será usada internamente para armazenar os produtos da fila.
        self.itens = []
    
    def inserir(self, produto, prioridade):
        # Cria um item contendo:
        item = {
            "produto": produto,
            "prioridade": prioridade
        }

        # Adiciona o item ao final da lista.
        self.itens.append(item)

    def remover(self):
        # Se a fila estiver vazia, não existe nada para remover.
        if len(self.itens) == 0:
            return None

        # Começamos considerando que o primeiro item possui a maior prioridade.
        maior = 0

        # Percorremos os outros elementos da fila.
        for i in range(1, len(self.itens)):
            # Comparamos a prioridade atual com a maior encontrada.
            if self.itens[i]["prioridade"] > self.itens[maior]["prioridade"]:
                maior = i

        # Remove e retorna o produto com maior prioridade.
        return self.itens.pop(maior)

    def exibir(self):
        # Verifica se a fila está vazia.
        if len(self.itens) == 0:
            print("\nFila de prioridade vazia.")
            return

        print("\n--== FILA DE PRIORIDADE ==--")

        # Percorre todos os itens da fila.
        for item in self.itens:
            produto = item["produto"]
            prioridade = item["prioridade"]

            print(
                f"Prioridade: {prioridade} | "
                f"Produto: {produto.nome} | "
                f"Estoque: {produto.estoque} | "
                f"Mínimo: {produto.estoque_minimo}"
            )

# ESTRUTURAS PRINCIPAIS DO SISTEMA
# Lista que armazena os produtos cadastrados e os fornecedores.
produtos = []
fornecedores = []

# Lista usada como Pilha.
historico = []

# Esse objeto representa a fila de prioridade.
fila_prioridade = Prioridade()

# BUSCA MANUAL DE PRODUTO
def buscar_produto(codigo):
    # Percorremos manualmente todos os produtos.
    for produto in produtos:
        # Comparamos o código informado com o código cadastrado.
        if produto.codigo == codigo: 
            return produto

    # Se chegar aqui, significa que nenhum produto foi encontrado.
    return None 

# BUSCA MANUAL DE FORNECEDOR
def buscar_fornecedor(codigo):
    # Percorre manualmente todos os fornecedores.
    for fornecedor in fornecedores: 
        # Compara os códigos.
        if fornecedor.codigo == codigo:
            return fornecedor
        
    # Retorna None quando não encontrar.
    return None

# VALIDAÇÃO
def validar_texto(texto): 
    # strip() remove espaços do começo e do final.
    # Se depois disso a string estiver vazia, significa que o usuário não informou um texto válido.
    if texto.strip() == "":
        return False

    return True

# CADASTRO DE PRODUTO
def cadastrar_produto():
    print("\n--== CADASTRO DE PRODUTO ==--")

    # try/except evita que o programa seja encerrado quando o usuário digitar um valor numérico inválido.
    try:
        codigo = int(input("Código: "))

        # Verifica se já existe um produto com esse código.
        if buscar_produto(codigo) is not None:
            print("Já existe um produto com esse código.")
            return

        nome = input("Nome: ")

        if not validar_texto(nome):
            print("O nome é obrigatório.")
            return

        categoria = input("Categoria: ")

        if not validar_texto(categoria):
            print("A categoria é obrigatória.")
            return

        preco = float(input("Preço: "))
        estoque = int(input("Estoque atual: "))
        estoque_minimo = int(input("Estoque mínimo: "))

        # Não permitimos valores negativos.
        if preco < 0 or estoque < 0 or estoque_minimo < 0:
            print("Os valores não podem ser negativos.")
            return

        # Cria um objeto da classe Produto.
        produto = Produto(codigo, nome, categoria, preco, estoque, estoque_minimo)

        # Adiciona o produto na lista de produtos.
        produtos.append(produto)

        print("\nProduto cadastrado com sucesso!")

    except:
        print("\nDigite valores numéricos válidos.")

# CADASTRO DE FORNECEDOR
def cadastrar_fornecedor():
    print("\n--== CADASTRO DE FORNECEDOR ==--")

    try:
        codigo = int(input("Código: "))

        # Verifica se o código já está cadastrado.
        if buscar_fornecedor(codigo) is not None:
            print("Já existe um fornecedor com esse código.")
            return

        nome = input("Nome: ")

        if not validar_texto(nome):
            print("O nome é obrigatório.")
            return

        telefone = input("Telefone: ")

        if not validar_texto(telefone):
            print("O telefone é obrigatório.")
            return

        # Cria o objeto Fornecedor.
        fornecedor = Fornecedor(codigo, nome, telefone)

        # Adiciona o fornecedor na lista.
        fornecedores.append(fornecedor)

        print("\nFornecedor cadastrado com sucesso!")

    except ValueError:
        print("\nDigite um código válido.")

# MENU DE CADASTRO
def cadastrar():
    print("""
--== CADASTRAR ==--

1 - Produto
2 - Fornecedor
0 - Voltar
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_produto()
    elif opcao == "2":
        cadastrar_fornecedor()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")

# LISTAR PRODUTOS
def consultar_produtos():
    print("\n--== PRODUTOS CADASTRADOS ==--")

    # Verifica se a lista está vazia.
    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    # Percorre todos os produtos.
    for produto in produtos:
        print(produto)

# LISTAR FORNECEDORES
def consultar_fornecedores():
    print("\n--== FORNECEDORES CADASTRADOS ==--")

    # Verifica se a lista está vazia.
    if len(fornecedores) == 0:
        print("Nenhum fornecedor cadastrado.")
        return
    
    # Percorre todos os produtos.
    for fornecedor in fornecedores:
        print(fornecedor)

# CONSULTAR PRODUTO POR CÓDIGO
def consultar_produto():
    try:
        codigo = int(input("Digite o código do produto: "))

        # Utiliza nossa busca manual.
        produto = buscar_produto(codigo)

        if produto is None:
            print("Produto não encontrado.")
        else:
            print("\nProduto encontrado:")
            print(produto)

    except ValueError:
        print("Digite um código válido.")

# CONSULTAR FORNECEDOR POR CÓDIGO
def consultar_fornecedor():
    try:
        codigo = int(input("Digite o código do fornecedor: "))

        fornecedor = buscar_fornecedor(codigo)

        if fornecedor is None:
            print("Fornecedor não encontrado.")
        else:
            print("\nFornecedor encontrado:")
            print(fornecedor)

    except ValueError:
        print("Digite um código válido.")

# MENU DE CONSULTA
def consultar():
    print("""
--== CONSULTAR ==--

1 - Listar produtos
2 - Buscar produto
3 - Listar fornecedores
4 - Buscar fornecedor
0 - Voltar
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        consultar_produtos()
    elif opcao == "2":
        consultar_produto()
    elif opcao == "3":
        consultar_fornecedores()
    elif opcao == "4":
        consultar_fornecedor()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")

# ALTERAR PRODUTO
def alterar_produto():
    try:
        codigo = int(input("Código do produto: "))

        # Procura o produto usando a busca manual.
        produto = buscar_produto(codigo)

        if produto is None:
            print("Produto não encontrado.")
            return

        print("\nDeixe vazio para manter o valor atual.")

        # Mostra o valor atual para facilitar a alteração.
        nome = input(f"Nome [{produto.nome}]: ")

        # Se o usuário digitar alguma coisa, substituímos o valor antigo.
        if nome != "":
            produto.nome = nome

        categoria = input(f"Categoria [{produto.categoria}]: ")

        if categoria != "":
            produto.categoria = categoria

        preco = input(f"Preço [{produto.preco}]: ")

        if preco != "":
            produto.preco = float(preco)

        estoque_minimo = input(
            f"Estoque mínimo [{produto.estoque_minimo}]: "
        )

        if estoque_minimo != "":
            produto.estoque_minimo = int(estoque_minimo)

        print("\nProduto alterado com sucesso!")

    except ValueError:
        print("Digite valores válidos.")

# ALTERAR FORNECEDOR
def alterar_fornecedor():
    try:
        codigo = int(input("Código do fornecedor: "))

        fornecedor = buscar_fornecedor(codigo)

        if fornecedor is None:
            print("Fornecedor não encontrado.")
            return

        print("\nDeixe vazio para manter o valor atual.")

        nome = input(f"Nome [{fornecedor.nome}]: ")

        if nome != "":
            fornecedor.nome = nome

        telefone = input(f"Telefone [{fornecedor.telefone}]: ")

        if telefone != "":
            fornecedor.telefone = telefone

        print("\nFornecedor alterado com sucesso!")

    except ValueError:
        print("Digite um código válido.")

# MENU DE ALTERAÇÃO
def alterar():
    print("""
--== ALTERAÇÃO ==--

1 - Produto
2 - Fornecedor
0 - Voltar
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        alterar_produto()
    elif opcao == "2":
        alterar_fornecedor()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")

def remover_produto_por_codigo(codigo):
    produto = buscar_produto(codigo)

    if produto is None:
        return False

    for i in range(len(produtos)):
        if produtos[i].codigo == codigo:
            produtos.pop(i)
            return True

    return False

# REMOVER PRODUTO
def remover_produto():
    try:
        codigo = int(input("Código do produto: "))

        produto = buscar_produto(codigo)

        if produto is None:
            print("Produto não encontrado.")
            return

        # Percorremos a lista usando os índices.
        for i in range(len(produtos)):
            # Verificamos se encontramos o código.
            if produtos[i].codigo == codigo:
                # pop remove o elemento daquela posição.
                produtos.pop(i)

                print("Produto removido com sucesso!")
                return

    except ValueError:
        print("Digite um código válido.")

# REMOVER FORNECEDOR
def remover_fornecedor():
    try:
        codigo = int(input("Código do fornecedor: "))

        fornecedor = buscar_fornecedor(codigo)

        if fornecedor is None:
            print("Fornecedor não encontrado.")
            return

        for i in range(len(fornecedores)):
            if fornecedores[i].codigo == codigo:
                fornecedores.pop(i)
                print("Fornecedor removido com sucesso!")
                return

    except ValueError:
        print("Digite um código válido.")

# MENU DE REMOÇÃO
def remover():
    print("""
--== REMOÇÃO ==--

1 - Produto
2 - Fornecedor
0 - Voltar
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        remover_produto()
    elif opcao == "2":
        remover_fornecedor()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")

# CÁLCULO DA PRIORIDADE
def calcular_prioridade(produto):
    # Prioridade 3: produto completamente sem estoque.
    if produto.estoque == 0:
        return 3
    # Prioridade 2: estoque abaixo do mínimo
    elif produto.estoque < produto.estoque_minimo: 
        return 2
    # Prioridade 1: estoque normal.
    else:
        return 1 

# ATUALIZAR FILA DE PRIORIDADE
def atualizar_fila_prioridade():
    # Limpa a fila atual para reconstruí-la.
    fila_prioridade.itens = []

    for produto in produtos:
        # Calcula a prioridade daquele produto.
        prioridade = calcular_prioridade(produto)
        # Apenas produtos com prioridade maior que 1 precisam entrar na fila de reposição.
        if prioridade > 1:
            fila_prioridade.inserir(produto, prioridade)

# MOVIMENTAÇÃO DO ESTOQUE
def movimentar_estoque(): 
    try:
        codigo = int(input("Código do produto: "))

        # Procura o produto.
        produto = buscar_produto(codigo)

        if produto is None:
            print("Produto não encontrado.")
            return

        print("""
1 - Entrada de estoque
2 - Saída de estoque
""")

        opcao = input("Escolha: ")

        quantidade = int(input("Quantidade: "))

        # A quantidade precisa ser positiva.
        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

        if opcao == "1":
            # Aumenta o estoque.
            produto.estoque += quantidade

            # Registra a movimentação no histórico. Como o histórico funciona como pilha, essa movimentação será colocada no topo.
            historico.append({
                "tipo": "entrada",
                "produto": produto,
                "quantidade": quantidade
            })

            print("Entrada registrada!")

        elif opcao == "2":
            # Não permite retirar mais produtos do que existem no estoque.
            if quantidade > produto.estoque:
                print("Estoque insuficiente.")
                return
            
            # Diminui o estoque.
            produto.estoque -= quantidade

            # Registra a saída no histórico.
            historico.append({
                "tipo": "saida",
                "produto": produto,
                "quantidade": quantidade
            })

            print("Saída registrada!")

        else:
            print("Opção inválida.")
            return
        # Depois de alterar o estoque, atualizamos a fila de prioridade.
        atualizar_fila_prioridade()

    except ValueError:
        print("Digite valores válidos.")

# DESFAZER MOVIMENTAÇÃO
def desfazer_movimentacao(): 
    # Se o histórico estiver vazio, não existe nenhuma movimentação para desfazer.
    if len(historico) == 0:
        print("\nNenhuma movimentação para desfazer.")
        return
    # O último movimento feito é o primeiro a ser desfeito.
    ultima = historico.pop()

    # Recupera os dados da movimentação.
    produto = ultima["produto"]
    quantidade = ultima["quantidade"]
    tipo = ultima["tipo"]

    # Se a movimentação original foi uma entrada, precisamos retirar novamente aquela quantidade.
    if tipo == "entrada":

        produto.estoque -= quantidade

        print(
            f"\nDesfeita entrada de {quantidade} "
            f"unidade(s) de {produto.nome}."
        )
    # Se foi uma saída, devolvemos a quantidade para o estoque.
    elif tipo == "saida":

        produto.estoque += quantidade

        print(
            f"\nDesfeita saída de {quantidade} "
            f"unidade(s) de {produto.nome}."
        )
    # Depois de desfazer, atualizamos novamente a fila de prioridade.
    atualizar_fila_prioridade()

# EXIBIR HISTÓRICO
def exibir_historico():

    print("\n--== HISTÓRICO DE MOVIMENTAÇÕES ==--")

    if len(historico) == 0:
        print("Nenhuma movimentação registrada.")
        return

    # Percorre o histórico de trás para frente. Dessa forma, mostramos primeiro a movimentação mais recente.
    for i in range(len(historico) - 1, -1, -1): 

        movimentacao = historico[i]

        print(
            f"{movimentacao['tipo'].upper()} | "
            f"{movimentacao['produto'].nome} | "
            f"Quantidade: {movimentacao['quantidade']}"
        )

# FILTRO POR CATEGORIA
def filtrar_categoria():
    categoria = input("Digite a categoria: ")

    # Variável usada para saber se encontramos algum produto.
    encontrou = False

    print("\n--== PRODUTOS DA CATEGORIA ==--")

    for produto in produtos:
        if produto.categoria.lower() == categoria.lower():
            print(produto)
            encontrou = True

    # Caso nenhum produto tenha sido encontrado.
    if not encontrou:
        print("Nenhum produto encontrado nessa categoria.")

# ORDENAÇÃO MANUAL
def produtos_ordenados_por_estoque():
    # Criamos uma nova lista para não alterar a ordem original da lista de produtos.
    lista = [] 

    # Copiamos os produtos para a nova lista.
    for produto in produtos:
        lista.append(produto)

    tamanho = len(lista)

    # Aqui temos uma ordenação implementada manualmente.
    for i in range(tamanho - 1):
        # Consideramos inicialmente que a posição i possui o menor estoque.
        menor = i

        # Procuramos um valor menor nas posições seguintes.
        for j in range(i + 1, tamanho):
            if lista[j].estoque < lista[menor].estoque:
                # Encontramos uma posição com estoque menor.
                menor = j

        # Se encontramos outro menor, fazemos a troca.
        if menor != i:
            temp = lista[i]
            lista[i] = lista[menor]
            lista[menor] = temp

    return lista

def ordenar_por_estoque():
    lista = produtos_ordenados_por_estoque()

    print("\n--== PRODUTOS ORDENADOS POR ESTOQUE ==--")

    if len(lista) == 0:
        print("Nenhum produto cadastrado.")
        return

    # Mostra a lista já ordenada.
    for produto in lista:
        print(
            f"{produto.nome} | "
            f"Estoque: {produto.estoque}"
        )

# RELATÓRIO DE ESTOQUE
def relatorio_estoque():

    print("\n--== RELATÓRIO DE ESTOQUE ==--")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        # Se estoque = 0, está esgotado.
        if produto.estoque == 0:
            situacao = "ESGOTADO"
        # Se estoque está abaixo do mínimo, consideramos situação crítica.
        elif produto.estoque < produto.estoque_minimo:
            situacao = "ESTOQUE CRÍTICO"
        # Caso contrário, está normal.
        else:
            situacao = "NORMAL"

        print(
            f"{produto.nome} | "
            f"Estoque: {produto.estoque} | "
            f"Mínimo: {produto.estoque_minimo} | "
            f"{situacao}"
        )

# MENU DE RELATÓRIOS
def relatorios():

    print("""
--== RELATÓRIOS ==--

1 - Listar produtos
2 - Filtrar por categoria
3 - Fila de prioridade
4 - Histórico da pilha
5 - Produtos ordenados por estoque
6 - Relatório de estoque
0 - Voltar
""")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        consultar_produtos()
    elif opcao == "2":
        filtrar_categoria()
    elif opcao == "3":
        # Atualiza a fila antes de exibi-la.
        atualizar_fila_prioridade()
        fila_prioridade.exibir()
    elif opcao == "4":
        exibir_historico()
    elif opcao == "5":
        ordenar_por_estoque()
    elif opcao == "6":
        relatorio_estoque()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")

# PROCESSAR REPOSIÇÃO
def processar_reposicao():
    # Primeiro atualizamos a fila.
    atualizar_fila_prioridade()

    # Remove o produto de maior prioridade.
    item = fila_prioridade.remover()  

    # Se não existir nenhum produto na fila.
    if item is None:
        print("\nNão existem produtos aguardando reposição.")
        return

    # Recupera os dados do item removido.
    produto = item["produto"]
    prioridade = item["prioridade"]

    print("\n--== REPOSIÇÃO PROCESSADA ==--")

    print(f"Produto: {produto.nome}")
    print(f"Prioridade: {prioridade}")
    print(f"Estoque atual: {produto.estoque}")
    print(f"Estoque mínimo: {produto.estoque_minimo}")

    print("\nEsse produto foi escolhido primeiro porque possui a maior prioridade na fila.")

# MENU PRINCIPAL
if __name__ == "__main__":
    while True:
        texto()

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            consultar()
        elif opcao == "3":
            alterar()
        elif opcao == "4":
            remover()
        elif opcao == "5":
            movimentar_estoque()
        elif opcao == "6":
            print("""
    --== FILA DE PRIORIDADE ==--

    1 - Exibir fila
    2 - Processar reposição
    0 - Voltar
    """)

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                # Atualiza e exibe a fila.
                atualizar_fila_prioridade()
                fila_prioridade.exibir()
            elif escolha == "2":
                # Processa o produto com maior prioridade.
                processar_reposicao()
            elif escolha == "0":
                # Volta para o menu principal.
                continue
            else:
                print("Opção inválida.")
        elif opcao == "7":
            relatorios()
        elif opcao == "8":
            desfazer_movimentacao()
        elif opcao == "0":
            print("\nSistema encerrado.")
            break
        else:
            print("\nOpção inválida.")