import json


usuarios = {}
feedbacks = []

ARQUIVO_JSON = "arquivos.json"
ARQUIVO_TXT = "arquivos.txt"


def carregar_dados():

    global usuarios, feedbacks

    try:
        arquivo = open(ARQUIVO_JSON, "r", encoding="utf-8")
        dados = json.load(arquivo)

        usuarios = dados["usuarios"]
        feedbacks = dados["feedbacks"]

        arquivo.close()

    except FileNotFoundError:
        usuarios = {}
        feedbacks = []

    except Exception:
        print("Erro ao carregar os dados.")
        usuarios = {}
        feedbacks = []


def salvar_dados_json():

    dados = {
        "usuarios": usuarios,
        "feedbacks": feedbacks
    }

    try:
        arquivo = open(ARQUIVO_JSON, "w", encoding="utf-8")
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        arquivo.close()

    except Exception:
        print("Erro ao salvar o arquivo JSON.")


def validar_data(data):

    partes = data.split("/")

    if len(partes) != 3:
        return False

    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])

    except ValueError:
        return False

    if dia < 1 or dia > 31:
        return False

    if mes < 1 or mes > 12:
        return False

    if ano < 1:
        return False

    return True


def cadastrar_usuario():

    print("\n--- CADASTRO DE USUARIO ---")

    id_usuario = input("Digite o ID único do usuário: ")

    if id_usuario == "":
        print("Erro: o ID não pode ser vazio.")
        return

    if id_usuario in usuarios:
        print("Erro: este ID ja está cadastrado.")
        return

    nome = input("Nome: ")

    if nome == "":
        print("Erro: o nome não pode ser vazio.")
        return

    try:
        idade = int(input("Idade: "))

        if idade < 0:
            print("Erro: a idade não pode ser negativa.")
            return

    except ValueError:
        print("Erro: a idade deve ser um número inteiro.")
        return

    profissao = input("Profissão: ")

    if profissao == "":
        print("Erro: a profissão nao pode ser vazia.")
        return

    tipo_usuario = input("Tipo de usuário: ")

    if tipo_usuario == "":
        print("Erro: o tipo de usuário nao pode ser vazio.")
        return

    dados_perfil = (
        nome,
        idade,
        profissao,
        tipo_usuario
    )

    usuarios[id_usuario] = {
        "nome": dados_perfil[0],
        "idade": dados_perfil[1],
        "profissao": dados_perfil[2],
        "tipo": dados_perfil[3]
    }

    salvar_dados_json()

    print("Usuario cadastrado com sucesso!")


def listar_usuarios():

    print("\n--- LISTA DE USUARIOS ---")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for id_usuario in usuarios:
        dados = usuarios[id_usuario]

        print(
            "ID:", id_usuario,
            "- Nome:", dados["nome"],
            "- Tipo:", dados["tipo"]
        )


def registrar_feedback():

    print("\n--- REGISTRAR FEEDBACK ---")

    if not usuarios:
        print("Erro: cadastre um usuario antes de registrar feedbacks.")
        return

    id_usuario = input("Digite o ID do usuario: ")

    if id_usuario not in usuarios:
        print("Erro: usuario nao encontrado.")
        return

    produto = input("Nome do produto: ")

    if produto == "":
        print("Erro: o nome do produto nao pode ser vazio.")
        return

    texto = input("Escreva o feedback: ")

    if texto == "":
        print("Erro: o feedback nao pode ser vazio.")
        return

    try:
        nota = float(input("Nota do produto (0 a 10): "))

        if nota < 0 or nota > 10:
            print("Erro: a nota deve estar entre 0 e 10.")
            return

    except ValueError:
        print("Erro: a nota deve ser um numero valido.")
        return

    data = input("Digite a data (DD/MM/AAAA): ")

    if not validar_data(data):
        print("Erro: a data deve estar no formato DD/MM/AAAA.")
        return

    novo_feedback = {
        "usuario_id": id_usuario,
        "produto": produto,
        "texto": texto,
        "nota": nota,
        "data": data
    }

    feedbacks.append(novo_feedback)

    salvar_dados_json()

    print("Feedback registrado com sucesso!")


def gerar_relatorio_analitico():

    print("\n--- GERANDO RELATORIO ANALITICO ---")

    if not feedbacks:
        print("Nenhum feedback registrado.")
        return []

    produtos_analise = {}

    for feedback in feedbacks:
        produto = feedback["produto"]

        if produto not in produtos_analise:
            produtos_analise[produto] = {
                "soma_notas": 0,
                "qtd": 0
            }

        produtos_analise[produto]["soma_notas"] += feedback["nota"]
        produtos_analise[produto]["qtd"] += 1

    matriz_relatorio = []

    for produto in produtos_analise:
        dados = produtos_analise[produto]

        media = dados["soma_notas"] / dados["qtd"]

        linha = [
            produto,
            media,
            dados["qtd"]
        ]

        matriz_relatorio.append(linha)

    print("\nMATRIZ DE DADOS:")

    for linha in matriz_relatorio:
        print(
            "Produto:", linha[0],
            "| Media:", f"{linha[1]:.2f}",
            "| Total Feedbacks:", linha[2]
        )

    print("\n--- FEEDBACKS POR PRODUTO ---")

    for produto in produtos_analise:
        print("\nProduto:", produto)

        for feedback in feedbacks:
            if feedback["produto"] == produto:
                print(
                    "Nota:", feedback["nota"],
                    "| Data:", feedback["data"],
                    "| Feedback:", feedback["texto"]
                )

    try:
        arquivo_txt = open(ARQUIVO_TXT, "w", encoding="utf-8")

        arquivo_txt.write("=== RELATORIO FEEDSMART ===\n\n")

        for linha in matriz_relatorio:
            arquivo_txt.write(
                "Produto: "
                + str(linha[0])
                + " | Media: "
                + f"{linha[1]:.2f}"
                + " | Total: "
                + str(linha[2])
                + "\n"
            )

        arquivo_txt.write("\n=== FEEDBACKS POR PRODUTO ===\n")

        for produto in produtos_analise:
            arquivo_txt.write(
                "\nProduto: "
                + produto
                + "\n"
            )

            for feedback in feedbacks:
                if feedback["produto"] == produto:
                    arquivo_txt.write(
                        "Nota: "
                        + str(feedback["nota"])
                        + " | Data: "
                        + feedback["data"]
                        + " | Feedback: "
                        + feedback["texto"]
                        + "\n"
                    )

        arquivo_txt.close()

        print("Relatorio gravado em arquivos.txt com sucesso.")

    except Exception:
        print("Erro ao gravar o arquivo de texto.")

    return matriz_relatorio


def mostrar_insights(matriz_dados, limite_media=6.0):

    print("\n--- INSIGHTS AUTOMATICOS DE NEGOCIO ---")

    if not matriz_dados:
        print("Sem dados suficientes.")
        return

    for linha in matriz_dados:
        if linha[1] < limite_media:
            print(
                "Produto",
                linha[0],
                "tem media abaixo de",
                limite_media,
                "- precisa de melhorias."
            )

    contagem_usuarios = {}

    for feedback in feedbacks:
        id_usuario = feedback["usuario_id"]

        if id_usuario not in contagem_usuarios:
            contagem_usuarios[id_usuario] = 0

        contagem_usuarios[id_usuario] += 1

    for id_usuario in contagem_usuarios:
        if contagem_usuarios[id_usuario] > 5:
            print(
                "Usuario",
                id_usuario,
                "enviou mais de 5 feedbacks - perfil engajado."
            )


def menu():

    carregar_dados()

    while True:
        print("\n=== MENU FEEDSMART ===")
        print("1. Cadastrar Usuario")
        print("2. Listar Usuarios")
        print("3. Registrar Feedback")
        print("4. Gerar Relatorio")
        print("5. Ver Insights")
        print("0. Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            cadastrar_usuario()

        elif opcao == "2":
            listar_usuarios()

        elif opcao == "3":
            registrar_feedback()

        elif opcao == "4":
            gerar_relatorio_analitico()

        elif opcao == "5":
            matriz_atual = gerar_relatorio_analitico()
            mostrar_insights(matriz_atual)

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    menu()