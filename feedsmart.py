import json

ARQUIVO_JSON = "arquivos.json"
ARQUIVO_TXT = "arquivos.txt"


def carregar_dados_txt():
    """Carrega usuarios e feedbacks do arquivo TXT."""
    usuarios = {}
    feedbacks = []

    try:
        arquivo = open(ARQUIVO_TXT, "r", encoding="utf-8")

        for linha in arquivo:
            partes = linha.strip().split("|", 1)

            if len(partes) == 2:
                if partes[0] == "USUARIO":
                    dados_usuario = json.loads(partes[1])
                    id_usuario = dados_usuario["id"]

                    usuarios[id_usuario] = {
                        "nome": dados_usuario["nome"],
                        "idade": dados_usuario["idade"],
                        "profissao": dados_usuario["profissao"],
                        "tipo": dados_usuario["tipo"]
                    }

                elif partes[0] == "FEEDBACK":
                    dados_feedback = json.loads(partes[1])
                    feedbacks.append(dados_feedback)

        arquivo.close()

    except FileNotFoundError:
        return {}, []

    except Exception:
        print("Erro ao carregar os dados do arquivo TXT.")
        return {}, []

    return usuarios, feedbacks


def carregar_dados():
    """Carrega usuarios e feedbacks do JSON ou, se necessario, do TXT."""
    try:
        arquivo = open(ARQUIVO_JSON, "r", encoding="utf-8")
        dados = json.load(arquivo)
        arquivo.close()

        return dados["usuarios"], dados["feedbacks"]

    except FileNotFoundError:
        print("Arquivo JSON nao encontrado. Tentando carregar o TXT.")
        return carregar_dados_txt()

    except Exception:
        print("Erro ao carregar o JSON. Tentando carregar o TXT.")
        return carregar_dados_txt()


def salvar_dados_json(usuarios, feedbacks):
    """Salva usuarios e feedbacks no arquivo JSON."""
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


def salvar_dados_txt(usuarios, feedbacks, matriz_relatorio=None):
    """Salva os dados no TXT e, quando solicitado, inclui o relatorio."""
    try:
        arquivo = open(ARQUIVO_TXT, "w", encoding="utf-8")

        arquivo.write("=== DADOS FEEDSMART ===\n")

        for id_usuario in usuarios:
            dados_usuario = {
                "id": id_usuario,
                "nome": usuarios[id_usuario]["nome"],
                "idade": usuarios[id_usuario]["idade"],
                "profissao": usuarios[id_usuario]["profissao"],
                "tipo": usuarios[id_usuario]["tipo"]
            }

            arquivo.write(
                "USUARIO|"
                + json.dumps(dados_usuario, ensure_ascii=False)
                + "\n"
            )

        for feedback in feedbacks:
            arquivo.write(
                "FEEDBACK|"
                + json.dumps(feedback, ensure_ascii=False)
                + "\n"
            )

        if matriz_relatorio is not None:
            arquivo.write("\n=== RELATORIO FEEDSMART ===\n\n")

            for linha in matriz_relatorio:
                arquivo.write(
                    "Produto: "
                    + str(linha[0])
                    + " | Media: "
                    + f"{linha[1]:.2f}"
                    + " | Total: "
                    + str(linha[2])
                    + "\n"
                )

            arquivo.write("\n=== FEEDBACKS POR PRODUTO ===\n")

            for linha in matriz_relatorio:
                produto = linha[0]
                arquivo.write("\nProduto: " + produto + "\n")

                for feedback in feedbacks:
                    if feedback["produto"] == produto:
                        arquivo.write(
                            "Nota: "
                            + str(feedback["nota"])
                            + " | Data: "
                            + feedback["data"]
                            + " | Feedback: "
                            + feedback["texto"]
                            + "\n"
                        )

        arquivo.close()

    except Exception:
        print("Erro ao salvar o arquivo TXT.")


def salvar_dados(usuarios, feedbacks):
    """Salva os dados nos arquivos JSON e TXT."""
    salvar_dados_json(usuarios, feedbacks)
    salvar_dados_txt(usuarios, feedbacks)


def validar_data(data):
    """Verifica se a data e valida no formato DD/MM/AAAA."""
    partes = data.split("/")

    if len(partes) != 3:
        return False

    if len(partes[0]) != 2 or len(partes[1]) != 2 or len(partes[2]) != 4:
        return False

    try:
        dia = int(partes[0])
        mes = int(partes[1])
        ano = int(partes[2])

    except ValueError:
        return False

    if ano < 1 or mes < 1 or mes > 12:
        return False

    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if ano % 400 == 0 or (ano % 4 == 0 and ano % 100 != 0):
        dias_por_mes[1] = 29

    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False

    return True


def cadastrar_usuario(usuarios, feedbacks):
    """Cadastra um novo usuario e salva os dados."""
    print("\n--- CADASTRO DE USUARIO ---")

    id_usuario = input("Digite o ID unico do usuario: ").strip()

    if id_usuario == "":
        print("Erro: o ID nao pode ser vazio.")
        return

    if id_usuario in usuarios:
        print("Erro: este ID ja esta cadastrado.")
        return

    nome = input("Nome: ").strip()

    if nome == "":
        print("Erro: o nome nao pode ser vazio.")
        return

    try:
        idade = int(input("Idade: "))

        if idade < 0:
            print("Erro: a idade nao pode ser negativa.")
            return

    except ValueError:
        print("Erro: a idade deve ser um numero inteiro.")
        return

    profissao = input("Profissao: ").strip()

    if profissao == "":
        print("Erro: a profissao nao pode ser vazia.")
        return

    tipo_usuario = input("Tipo de usuario: ").strip()

    if tipo_usuario == "":
        print("Erro: o tipo de usuario nao pode ser vazio.")
        return

    dados_perfil = (nome, idade, profissao, tipo_usuario)

    usuarios[id_usuario] = {
        "nome": dados_perfil[0],
        "idade": dados_perfil[1],
        "profissao": dados_perfil[2],
        "tipo": dados_perfil[3]
    }

    salvar_dados(usuarios, feedbacks)
    print("Usuario cadastrado com sucesso!")


def listar_usuarios(usuarios):
    """Lista todos os usuarios cadastrados."""
    print("\n--- LISTA DE USUARIOS ---")

    if not usuarios:
        print("Nenhum usuario cadastrado.")
        return

    for id_usuario in usuarios:
        dados = usuarios[id_usuario]

        print(
            "ID:", id_usuario,
            "- Nome:", dados["nome"],
            "- Tipo:", dados["tipo"]
        )


def registrar_feedback(usuarios, feedbacks):
    """Registra um feedback associado a um usuario existente."""
    print("\n--- REGISTRAR FEEDBACK ---")

    if not usuarios:
        print("Erro: cadastre um usuario antes de registrar feedbacks.")
        return

    id_usuario = input("Digite o ID do usuario: ").strip()

    if id_usuario not in usuarios:
        print("Erro: usuario nao encontrado.")
        return

    produto = input("Nome do produto: ").strip()

    if produto == "":
        print("Erro: o nome do produto nao pode ser vazio.")
        return

    texto = input("Escreva o feedback: ").strip()

    if texto == "":
        print("Erro: o feedback nao pode ser vazio.")
        return

    try:
        nota_texto = input("Nota do produto (0 a 10): ")
        nota = float(nota_texto.replace(",", "."))

        if nota < 0 or nota > 10:
            print("Erro: a nota deve estar entre 0 e 10.")
            return

    except ValueError:
        print("Erro: a nota deve ser um numero valido.")
        return

    data = input("Digite a data (DD/MM/AAAA): ").strip()

    if not validar_data(data):
        print("Erro: informe uma data valida no formato DD/MM/AAAA.")
        return

    novo_feedback = {
        "usuario_id": id_usuario,
        "produto": produto,
        "texto": texto,
        "nota": nota,
        "data": data
    }

    feedbacks.append(novo_feedback)
    salvar_dados(usuarios, feedbacks)
    print("Feedback registrado com sucesso!")


def gerar_relatorio_analitico(usuarios, feedbacks):
    """Calcula medias, conta feedbacks e lista avaliacoes por produto."""
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
        linha = [produto, media, dados["qtd"]]
        matriz_relatorio.append(linha)

    print("\nMATRIZ DE DADOS:")

    for linha in matriz_relatorio:
        print(
            "Produto:", linha[0],
            "| Media:", f"{linha[1]:.2f}",
            "| Total Feedbacks:", linha[2]
        )

    print("\n--- FEEDBACKS POR PRODUTO ---")

    for linha in matriz_relatorio:
        produto = linha[0]
        print("\nProduto:", produto)

        for feedback in feedbacks:
            if feedback["produto"] == produto:
                print(
                    "Nota:", feedback["nota"],
                    "| Data:", feedback["data"],
                    "| Feedback:", feedback["texto"]
                )

    salvar_dados_txt(usuarios, feedbacks, matriz_relatorio)
    print("Relatorio gravado em arquivos.txt com sucesso.")

    return matriz_relatorio


def mostrar_insights(matriz_dados, feedbacks, limite_media=6.0):
    """Mostra insights automaticos sobre produtos e usuarios."""
    print("\n--- INSIGHTS AUTOMATICOS DE NEGOCIO ---")

    if not matriz_dados:
        print("Sem dados suficientes.")
        return

    for linha in matriz_dados:
        if linha[1] < limite_media:
            print(
                "Produto", linha[0],
                "tem media abaixo de", limite_media,
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
                "Usuario", id_usuario,
                "enviou mais de 5 feedbacks - perfil engajado."
            )


def menu():
    """Exibe o menu principal e controla a navegacao do sistema."""
    usuarios, feedbacks = carregar_dados()

    while True:
        print("\n=== MENU FEEDSMART ===")
        print("1. Cadastrar Usuario")
        print("2. Listar Usuarios")
        print("3. Registrar Feedback")
        print("4. Gerar Relatorio")
        print("5. Ver Insights")
        print("0. Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_usuario(usuarios, feedbacks)

        elif opcao == "2":
            listar_usuarios(usuarios)

        elif opcao == "3":
            registrar_feedback(usuarios, feedbacks)

        elif opcao == "4":
            gerar_relatorio_analitico(usuarios, feedbacks)

        elif opcao == "5":
            matriz_atual = gerar_relatorio_analitico(usuarios, feedbacks)
            mostrar_insights(matriz_atual, feedbacks)

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opcao invalida. Escolha uma opcao do menu.")


if __name__ == "__main__":
    menu()
