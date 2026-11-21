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
        self.ordem_cadastro = None

    def __str__(self):
        # Define como o produto será exibido quando usarmos print(produto).
        return f"[{self.codigo}] {self.nome} / {self.categoria} - R$ {self.preco:.2f} (Estoque: {self.estoque} / Mínimo: {self.estoque_minimo})"

class NoAVL:
    def __init__(self, produto):
        self.produto = produto
        self.esquerda = None
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self):
        self.raiz = None

    def buscar(self, codigo):
        atual = self.raiz

        while atual is not None:
            if codigo == atual.produto.codigo:
                return atual.produto

            if codigo < atual.produto.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita

        return None
    
    def inserir(self, produto):
        self.raiz = self._inserir(self.raiz, produto)

    def _inserir(self, no, produto):
        if no is None:
            return NoAVL(produto)

        if produto.codigo < no.produto.codigo:
            no.esquerda = self._inserir(no.esquerda, produto)
        elif produto.codigo > no.produto.codigo:
            no.direita = self._inserir(no.direita, produto)
        else:
            return no  # O código já existe.

        return self._balancear(no)
    
    def _altura(self, no):
        if no is None:
            return 0
        return no.altura

    def _atualizar_altura(self, no):
        esquerda = self._altura(no.esquerda)
        direita = self._altura(no.direita)
        no.altura = 1 + max(esquerda, direita)

    def _rotacionar_esquerda(self, no):
        nova_raiz = no.direita
        no.direita = nova_raiz.esquerda
        nova_raiz.esquerda = no

        self._atualizar_altura(no)
        self._atualizar_altura(nova_raiz)

        return nova_raiz

    def _rotacionar_direita(self, no):
        nova_raiz = no.esquerda
        no.esquerda = nova_raiz.direita
        nova_raiz.direita = no

        self._atualizar_altura(no)
        self._atualizar_altura(nova_raiz)

        return nova_raiz

    def _balancear(self, no):
        self._atualizar_altura(no)
        fator = self._altura(no.esquerda) - self._altura(no.direita)

        if fator > 1:
            filho = no.esquerda
            if self._altura(filho.direita) > self._altura(filho.esquerda):
                no.esquerda = self._rotacionar_esquerda(filho)
            return self._rotacionar_direita(no)

        if fator < -1:
            filho = no.direita
            if self._altura(filho.esquerda) > self._altura(filho.direita):
                no.direita = self._rotacionar_direita(filho)
            return self._rotacionar_esquerda(no)

        return no

    def remover(self, codigo):
        self.raiz = self._remover(self.raiz, codigo)

    def _remover(self, no, codigo):
        if no is None:
            return None

        if codigo < no.produto.codigo:
            no.esquerda = self._remover(no.esquerda, codigo)

        elif codigo > no.produto.codigo:
            no.direita = self._remover(no.direita, codigo)

        else:
            # Encontramos o produto. Se houver só um filho, ele assume o lugar.
            # Se for uma folha, o retorno será None.
            if no.esquerda is None:
                return no.direita

            if no.direita is None:
                return no.esquerda

            # Com dois filhos, procuramos o menor código do lado direito.
            sucessor = no.direita
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda

            no.produto = sucessor.produto
            no.direita = self._remover(no.direita, sucessor.produto.codigo)

        return self._balancear(no)

    def em_ordem(self):
        produtos = []
        self._em_ordem(self.raiz, produtos)
        return produtos

    def _em_ordem(self, no, produtos):
        if no is None:
            return

        self._em_ordem(no.esquerda, produtos)
        produtos.append(no.produto)
        self._em_ordem(no.direita, produtos)

    def pre_ordem(self):
        produtos = []
        self._pre_ordem(self.raiz, produtos)
        return produtos

    def _pre_ordem(self, no, produtos):
        if no is None:
            return

        produtos.append(no.produto)
        self._pre_ordem(no.esquerda, produtos)
        self._pre_ordem(no.direita, produtos)

    def pos_ordem(self):
        produtos = []
        self._pos_ordem(self.raiz, produtos)
        return produtos

    def _pos_ordem(self, no, produtos):
        if no is None:
            return

        self._pos_ordem(no.esquerda, produtos)
        self._pos_ordem(no.direita, produtos)
        produtos.append(no.produto)

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
produtos = ArvoreAVL()
fornecedores = []
proxima_ordem_cadastro = 1

# Lista usada como Pilha.
historico = []

# Esse objeto representa a fila de prioridade.
fila_prioridade = Prioridade()
fila_desatualizada = True

# BUSCA MANUAL DE PRODUTO
def buscar_produto(codigo):
    return produtos.buscar(codigo)

# BUSCA MANUAL DE FORNECEDOR
def buscar_fornecedor(codigo):
    # Percorre manualmente todos os fornecedores.
    for fornecedor in fornecedores: 
        # Compara os códigos.
        if fornecedor.codigo == codigo:
            return fornecedor
        
    # Retorna None quando não encontrar.
    return None

# VALIDAÇÃO TEXTO
def validar_texto(texto): 
    # strip() remove espaços do começo e do final.
    # Se depois disso a string estiver vazia, significa que o usuário não informou um texto válido.
    if texto.strip() == "":
        return False

    return True

# VALIDAÇÃO DO CÓDIGO
def validar_codigo(texto):
    texto = texto.strip()

    if texto.startswith("-") or texto.startswith("+"):
        texto = texto[1:]

    return texto.isdecimal()

# CADASTRO DE PRODUTO
def cadastrar_produto():
    global proxima_ordem_cadastro
    print("\n--== CADASTRO DE PRODUTO ==--")

    entrada = input("Código: ")
    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)

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

    entrada = input("Preço: ").strip().replace(",", ".")
    if not entrada.replace(".", "", 1).isdecimal():
        print("Digite um preço válido, como 19,90.")
        return

    preco = float(entrada)

    entrada = input("Estoque atual: ").strip()
    if not entrada.isdecimal():
        print("O estoque atual deve ser um inteiro maior ou igual a zero.")
        return

    estoque = int(entrada)

    entrada = input("Estoque mínimo: ").strip()
    if not entrada.isdecimal():
        print("O estoque mínimo deve ser um inteiro maior ou igual a zero.")
        return

    estoque_minimo = int(entrada)

    # Cria um objeto da classe Produto.
    produto = Produto(codigo, nome, categoria, preco, estoque, estoque_minimo)
    produto.ordem_cadastro = proxima_ordem_cadastro
    produtos.inserir(produto)
    proxima_ordem_cadastro += 1
    marcar_fila_desatualizada()

    print("\nProduto cadastrado com sucesso!")

# CADASTRO DE FORNECEDOR
def cadastrar_fornecedor():
    print("\n--== CADASTRO DE FORNECEDOR ==--")

    entrada = input("Código: ")
    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)

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
    fornecedores.append(fornecedor) # Adiciona o fornecedor na lista.

    print("\nFornecedor cadastrado com sucesso!")

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

    if produtos.raiz is None:
        print("Nenhum produto cadastrado.")
        return

    print("1 - Em ordem de código")
    print("2 - Pré-ordem")
    print("3 - Pós-ordem")
    print("0 - Voltar")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        registros = produtos.em_ordem()
    elif opcao == "2":
        registros = produtos.pre_ordem()
    elif opcao == "3":
        registros = produtos.pos_ordem()
    elif opcao == "0":
        return
    else:
        print("Opção inválida.")
        return

    for produto in registros:
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
    entrada = input("Digite o código do produto: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
    else:
        print("\nProduto encontrado:")
        print(produto)

# CONSULTAR FORNECEDOR POR CÓDIGO
def consultar_fornecedor():
    entrada = input("Digite o código do fornecedor: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)
    fornecedor = buscar_fornecedor(codigo)

    if fornecedor is None:
        print("Fornecedor não encontrado.")
    else:
        print("\nFornecedor encontrado:")
        print(fornecedor)

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
    entrada = input("Código do produto: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    print("\nDeixe vazio para manter o valor atual.")

    nome = input(f"Nome [{produto.nome}]: ")
    if nome != "" and not validar_texto(nome):
        print("Digite um nome válido.")
        return

    categoria = input(f"Categoria [{produto.categoria}]: ")
    if categoria != "" and not validar_texto(categoria):
        print("Digite uma categoria válida.")
        return

    preco = input(f"Preço [{produto.preco:.2f}]: ").strip().replace(",", ".")
    if preco != "" and not preco.replace(".", "", 1).isdecimal():
        print("Digite um preço válido, como 19,90.")
        return

    estoque_minimo = input(f"Estoque mínimo [{produto.estoque_minimo}]: ").strip()
    if estoque_minimo != "" and not estoque_minimo.isdecimal():
        print("O estoque mínimo deve ser um inteiro maior ou igual a zero.")
        return

    # Só altera o produto depois de validar todos os campos.
    if nome != "":
        produto.nome = nome

    if categoria != "":
        produto.categoria = categoria

    if preco != "":
        produto.preco = float(preco)

    if estoque_minimo != "":
        produto.estoque_minimo = int(estoque_minimo)
        marcar_fila_desatualizada()

    print("\nProduto alterado com sucesso!")

# ALTERAR FORNECEDOR
def alterar_fornecedor():
    entrada = input("Código do fornecedor: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)
    fornecedor = buscar_fornecedor(codigo)

    if fornecedor is None:
        print("Fornecedor não encontrado.")
        return

    print("\nDeixe vazio para manter o valor atual.")

    nome = input(f"Nome [{fornecedor.nome}]: ")
    if nome != "" and not validar_texto(nome):
        print("Digite um nome válido.")
        return

    telefone = input(f"Telefone [{fornecedor.telefone}]: ")
    if telefone != "" and not validar_texto(telefone):
        print("Digite um telefone válido.")
        return

    # Atualiza o cadastro depois de conferir os dois campos.
    if nome != "":
        fornecedor.nome = nome

    if telefone != "":
        fornecedor.telefone = telefone

    print("\nFornecedor alterado com sucesso!")

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

# REMOVER PRODUTO
def remover_produto():
    entrada = input("Código do produto: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)

    if buscar_produto(codigo) is None:
        print("Produto não encontrado.")
        return

    produtos.remover(codigo)
    marcar_fila_desatualizada()
    print("Produto removido com sucesso!")

# REMOVER FORNECEDOR
def remover_fornecedor():
    entrada = input("Código do fornecedor: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)

    for i in range(len(fornecedores)):
        if fornecedores[i].codigo == codigo:
            fornecedores.pop(i)
            print("Fornecedor removido com sucesso!")
            return

    print("Fornecedor não encontrado.")

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

def marcar_fila_desatualizada():
    global fila_desatualizada
    fila_desatualizada = True

# ATUALIZAR FILA DE PRIORIDADE
def atualizar_fila_prioridade():
    global fila_desatualizada

    if not fila_desatualizada:
        return

    pendentes = []
    for produto in produtos.em_ordem():
        if calcular_prioridade(produto) > 1:
            pendentes.append(produto)

    pendentes = merge_sort_por_estoque(pendentes, por_cadastro=True)

    fila_prioridade.itens = []
    for produto in pendentes:
        prioridade = calcular_prioridade(produto)
        fila_prioridade.inserir(produto, prioridade)

    fila_desatualizada = False

# MOVIMENTAÇÃO DO ESTOQUE
def movimentar_estoque():
    entrada = input("Código do produto: ")

    if not validar_codigo(entrada):
        print("Digite um código válido.")
        return

    codigo = int(entrada)
    produto = buscar_produto(codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    print("\n1 - Entrada de estoque")
    print("2 - Saída de estoque")
    opcao = input("Escolha: ")

    if opcao != "1" and opcao != "2":
        print("Opção inválida.")
        return

    entrada = input("Quantidade: ").strip()

    if not entrada.isdecimal():
        print("Digite uma quantidade inteira maior que zero.")
        return

    quantidade = int(entrada)

    if quantidade == 0:
        print("A quantidade deve ser maior que zero.")
        return

    if opcao == "1":
        produto.estoque += quantidade
        tipo = "entrada"
        print("Entrada registrada!")
    else:
        if quantidade > produto.estoque:
            print("Estoque insuficiente.")
            return

        produto.estoque -= quantidade
        tipo = "saida"
        print("Saída registrada!")

    historico.append({
        "tipo": tipo,
        "produto": produto,
        "quantidade": quantidade
    })

    marcar_fila_desatualizada()

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
    marcar_fila_desatualizada()

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

    for produto in produtos.em_ordem():
        if produto.categoria.lower() == categoria.lower():
            print(produto)
            encontrou = True

    # Caso nenhum produto tenha sido encontrado.
    if not encontrou:
        print("Nenhum produto encontrado nessa categoria.")

def intercalar_por_estoque(esquerda, direita, por_cadastro=False):
    resultado = []
    i = 0
    j = 0

    while i < len(esquerda) and j < len(direita):
        if por_cadastro:
            pegar_esquerda = esquerda[i].ordem_cadastro <= direita[j].ordem_cadastro
        else:
            pegar_esquerda = esquerda[i].estoque <= direita[j].estoque
        if pegar_esquerda:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1
        
    while i < len(esquerda):
        resultado.append(esquerda[i])
        i += 1

    while j < len(direita):
        resultado.append(direita[j])
        j += 1

    return resultado

def merge_sort_por_estoque(lista, por_cadastro=False):
    if len(lista) <= 1:
        return lista

    meio = len(lista) // 2
    esquerda = merge_sort_por_estoque(lista[:meio], por_cadastro)
    direita = merge_sort_por_estoque(lista[meio:], por_cadastro)

    return intercalar_por_estoque(esquerda, direita, por_cadastro)

# ORDENAÇÃO MANUAL
def ordenar_por_estoque():
    registros = produtos.em_ordem()
    lista = merge_sort_por_estoque(registros)

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

    if produtos.raiz is None:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos.em_ordem():
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

    item = fila_prioridade.remover()

    if item is None:
        print("\nNão existem produtos aguardando reposição.")
        return

    marcar_fila_desatualizada()

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