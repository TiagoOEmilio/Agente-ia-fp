

import os
from datetime import datetime

# ---------------------------------------------------------------
# Constantes (nomes dos arquivos e configurações)
# ---------------------------------------------------------------
ARQ_USUARIOS = "usuarios.csv"      # matricula;nome;perfil;hora_inicio;hora_fim;observacoes
ARQ_ACESSOS = "acessos.csv"        # matricula;data_hora;maquina;resultado;classificacao;motivos
ARQ_LOG = "auditoria.csv"          # data_hora;operacao;matricula_afetada
ARQ_BLOQUEADOS = "bloqueados.txt"  # uma máquina bloqueada por linha

SEP = ";"                          # separador dos campos nos arquivos
PERFIS = ["estudante", "professor", "administrador"]


# ---------------------------------------------------------------
# Funções de arquivo (usadas por tudo no programa)
# ---------------------------------------------------------------
def carregar_linhas(arquivo):
    """Lê o arquivo e devolve uma lista de listas (uma lista de campos por linha)."""
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return [linha.strip().split(SEP) for linha in f if linha.strip()]
    except FileNotFoundError:
        return []  # primeira execução: o arquivo ainda não existe
    except OSError as erro:
        print(f"Erro ao ler {arquivo}: {erro}")
        return []


def salvar_linhas(arquivo, linhas):
    """Reescreve o arquivo inteiro (usado ao editar ou excluir)."""
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            for campos in linhas:
                f.write(SEP.join(campos) + "\n")
    except OSError as erro:
        print(f"Erro ao salvar {arquivo}: {erro}")


def adicionar_linha(arquivo, campos):
    """Acrescenta uma linha no final do arquivo (usado em acessos e log)."""
    try:
        with open(arquivo, "a", encoding="utf-8") as f:
            f.write(SEP.join(campos) + "\n")
    except OSError as erro:
        print(f"Erro ao gravar em {arquivo}: {erro}")


def carregar_bloqueadas():
    """Lê o bloqueados.txt e devolve uma lista com os nomes das máquinas."""
    try:
        with open(ARQ_BLOQUEADOS, "r", encoding="utf-8") as f:
            return [linha.strip().upper() for linha in f if linha.strip()]
    except FileNotFoundError:
        return []
    except OSError as erro:
        print(f"Erro ao ler {ARQ_BLOQUEADOS}: {erro}")
        return []


def criar_bloqueados_se_nao_existir():
    """Cria um bloqueados.txt de exemplo (com máquinas fictícias) na primeira execução."""
    if not os.path.exists(ARQ_BLOQUEADOS):
        try:
            with open(ARQ_BLOQUEADOS, "w", encoding="utf-8") as f:
                f.write("PC-13\nPC-99\n")
        except OSError as erro:
            print(f"Não foi possível criar {ARQ_BLOQUEADOS}: {erro}")


# ---------------------------------------------------------------
# Auditoria (log)
# ---------------------------------------------------------------
def registrar_log(operacao, matricula_afetada="-"):
    """Grava no log: data/hora, qual operação e qual usuário foi afetado."""
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    adicionar_linha(ARQ_LOG, [agora, operacao, matricula_afetada])


def consultar_log():
    linhas = carregar_linhas(ARQ_LOG)
    print("\n--- LOG DE AUDITORIA ---")
    if not linhas:
        print("O log está vazio.")
        return
    for campos in linhas:
        print(f"{campos[0]} | {campos[1]} | usuário afetado: {campos[2]}")


# ---------------------------------------------------------------
# Funções de entrada (validam o que o usuário digita)
# ---------------------------------------------------------------
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione Enter para continuar...")


def ler_texto(mensagem, obrigatorio=True):
    """Lê um texto. Não aceita vazio (se obrigatório) nem o caractere ';'."""
    while True:
        texto = input(mensagem).strip()
        if SEP in texto:
            print(f"Não use o caractere '{SEP}'.")
        elif obrigatorio and texto == "":
            print("Este campo não pode ficar vazio.")
        else:
            return texto


def ler_inteiro(mensagem, minimo, maximo):
    """Lê um número inteiro dentro de um intervalo."""
    while True:
        try:
            numero = int(input(mensagem))
            if minimo <= numero <= maximo:
                return numero
            print(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("Digite apenas números inteiros.")


def ler_perfil():
    print("Perfis: 1-estudante  2-professor  3-administrador")
    escolha = ler_inteiro("Escolha o perfil: ", 1, 3)
    return PERFIS[escolha - 1]


def ler_data_hora():
    """Pede data e hora. Se o usuário apertar Enter, usa o momento atual."""
    while True:
        texto = input("Data e hora (AAAA-MM-DD HH:MM) ou Enter para agora: ").strip()
        if texto == "":
            return datetime.now()
        try:
            return datetime.strptime(texto, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Formato inválido. Exemplo: 2026-11-05 03:00")


# ---------------------------------------------------------------
# TÓPICO 1 - Usuários
# ---------------------------------------------------------------
def mascarar_matricula(matricula):
    """Mostra só os 2 primeiros caracteres. Ex.: 20240001 -> 20******"""
    return matricula[:2] + "*" * (len(matricula) - 2)


def buscar_usuario(matricula):
    """Devolve a lista de campos do usuário, ou None se não existir."""
    for usuario in carregar_linhas(ARQ_USUARIOS):
        if usuario[0] == matricula:
            return usuario
    return None


def cadastrar_usuario():
    print("\n--- CADASTRAR USUÁRIO ---")
    matricula = ler_texto("Matrícula (mín. 3 caracteres): ")
    if len(matricula) < 3:
        print("A matrícula precisa ter pelo menos 3 caracteres.")
        return
    if buscar_usuario(matricula) is not None:
        print("Já existe um usuário com essa matrícula.")
        return

    nome = ler_texto("Nome: ")
    perfil = ler_perfil()
    hora_inicio = ler_inteiro("Horário permitido - início (0 a 23): ", 0, 23)
    hora_fim = ler_inteiro("Horário permitido - fim (1 a 24): ", 1, 24)
    if hora_fim <= hora_inicio:
        print("O horário final precisa ser maior que o inicial.")
        return
    observacoes = ler_texto("Observações (opcional): ", obrigatorio=False)

    adicionar_linha(ARQ_USUARIOS,
                    [matricula, nome, perfil, str(hora_inicio), str(hora_fim), observacoes])
    registrar_log("CADASTRAR_USUARIO", matricula)
    print("Usuário cadastrado com sucesso!")


def listar_usuarios():
    usuarios = carregar_linhas(ARQ_USUARIOS)
    print("\n--- USUÁRIOS CADASTRADOS ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"Matrícula: {mascarar_matricula(u[0])} | Nome: {u[1]} | Perfil: {u[2]} "
              f"| Horário: {u[3]}h às {u[4]}h | Obs: {u[5]}")


def revelar_matricula():
    """Mostra a matrícula completa e registra isso no log."""
    print("\n--- REVELAR MATRÍCULA ---")
    usuarios = carregar_linhas(ARQ_USUARIOS)
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for posicao, u in enumerate(usuarios, start=1):
        print(f"{posicao} - {u[1]} ({mascarar_matricula(u[0])})")

    escolha = ler_inteiro("Número do usuário: ", 1, len(usuarios))
    usuario = usuarios[escolha - 1]
    print(f"Matrícula de {usuario[1]}: {usuario[0]}")
    registrar_log("REVELAR_MATRICULA", usuario[0])


def editar_usuario():
    print("\n--- EDITAR USUÁRIO ---")
    matricula = ler_texto("Matrícula do usuário a editar: ")
    usuarios = carregar_linhas(ARQ_USUARIOS)

    for u in usuarios:
        if u[0] == matricula:
            print("Deixe em branco e aperte Enter para manter o valor atual.")
            novo_nome = ler_texto(f"Nome [{u[1]}]: ", obrigatorio=False)
            novo_obs = ler_texto(f"Observações [{u[5]}]: ", obrigatorio=False)
            print(f"Perfil atual: {u[2]}")
            if input("Alterar perfil? (s/n): ").strip().lower() == "s":
                u[2] = ler_perfil()
            print(f"Horário atual: {u[3]}h às {u[4]}h")
            if input("Alterar horário? (s/n): ").strip().lower() == "s":
                inicio = ler_inteiro("Início (0 a 23): ", 0, 23)
                fim = ler_inteiro("Fim (1 a 24): ", 1, 24)
                if fim <= inicio:
                    print("O horário final precisa ser maior que o inicial. Horário mantido.")
                else:
                    u[3], u[4] = str(inicio), str(fim)

            if novo_nome != "":
                u[1] = novo_nome
            if novo_obs != "":
                u[5] = novo_obs

            salvar_linhas(ARQ_USUARIOS, usuarios)
            registrar_log("EDITAR_USUARIO", matricula)
            print("Usuário atualizado!")
            return

    print("Usuário não encontrado.")


def excluir_usuario():
    print("\n--- EXCLUIR USUÁRIO ---")
    matricula = ler_texto("Matrícula do usuário a excluir: ")
    usuarios = carregar_linhas(ARQ_USUARIOS)

    for u in usuarios:
        if u[0] == matricula:
            confirma = input(f"Excluir {u[1]}? (s/n): ").strip().lower()
            if confirma == "s":
                usuarios.remove(u)
                salvar_linhas(ARQ_USUARIOS, usuarios)
                registrar_log("EXCLUIR_USUARIO", matricula)
                print("Usuário excluído.")
            else:
                print("Exclusão cancelada.")
            return

    print("Usuário não encontrado.")


# ---------------------------------------------------------------
# TÓPICO 2 - Análise de risco
# ---------------------------------------------------------------
def classificar_acesso(usuario, maquina, resultado, data_hora):
    """
    Avalia o acesso e devolve (nivel, motivos).

    Critérios (sistema de pontos):
      - acesso com falha ........................ +1
      - fora do horário permitido do usuário .... +1
      - máquina na lista de bloqueio ............ +2

    Resultado:
      0 pontos -> normal | 1 ponto -> suspeito | 2 ou mais -> critico
    """
    pontos = 0
    motivos = []

    if resultado == "falha":
        pontos += 1
        motivos.append("o acesso falhou")

    hora = data_hora.hour
    inicio = int(usuario[3])
    fim = int(usuario[4])
    if not (inicio <= hora < fim):
        pontos += 1
        motivos.append(f"horário {hora}h fora do permitido ({inicio}h às {fim}h)")

    if maquina in carregar_bloqueadas():
        pontos += 2
        motivos.append(f"a máquina {maquina} está na lista de bloqueio")

    if pontos == 0:
        nivel = "normal"
        motivos.append("nenhum critério de risco foi atingido")
    elif pontos == 1:
        nivel = "suspeito"
    else:
        nivel = "critico"

    return nivel, motivos


def registrar_acesso():
    print("\n--- REGISTRAR ACESSO ---")
    matricula = ler_texto("Matrícula do usuário: ")
    usuario = buscar_usuario(matricula)
    if usuario is None:
        print("Usuário não encontrado. Cadastre-o antes.")
        return

    maquina = ler_texto("Máquina de origem (ex.: PC-01): ").upper()
    print("Resultado: 1-sucesso  2-falha")
    resultado = "sucesso" if ler_inteiro("Escolha: ", 1, 2) == 1 else "falha"
    data_hora = ler_data_hora()

    nivel, motivos = classificar_acesso(usuario, maquina, resultado, data_hora)

    if maquina in carregar_bloqueadas():
        print(f"\n*** AVISO: a máquina {maquina} está BLOQUEADA! ***")

    texto_motivos = " | ".join(motivos)
    adicionar_linha(ARQ_ACESSOS, [matricula, data_hora.strftime("%Y-%m-%d %H:%M"),
                                  maquina, resultado, nivel, texto_motivos])
    registrar_log("REGISTRAR_ACESSO", matricula)

    print(f"\nAcesso registrado. Classificação: {nivel.upper()}")
    print("Por quê:")
    for motivo in motivos:
        print(f"  - {motivo}")


def consultar_acessos():
    acessos = carregar_linhas(ARQ_ACESSOS)
    print("\n--- ACESSOS REGISTRADOS ---")
    if not acessos:
        print("Nenhum acesso registrado.")
        return
    for a in acessos:
        print(f"{a[1]} | {mascarar_matricula(a[0])} | {a[2]} | {a[3]} | "
              f"{a[4].upper()} | motivo: {a[5]}")


# ---------------------------------------------------------------
# Menus
# ---------------------------------------------------------------
def menu_usuarios():
    while True:
        print("\n=== USUÁRIOS ===")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Editar")
        print("4. Excluir")
        print("5. Revelar matrícula")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            editar_usuario()
        elif opcao == "4":
            excluir_usuario()
        elif opcao == "5":
            revelar_matricula()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        pausar()


def menu_principal():
    while True:
        limpar_tela()
        print("=== SentinelaLog ===")
        print("1. Gerenciar usuários")
        print("2. Registrar acesso")
        print("3. Consultar acessos")
        print("4. Consultar log de auditoria")
        # Próximas opções (entregas futuras): máquinas compartilhadas,
        # relatório de segurança, funcionalidade extra e módulo de IA.
        print("0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            menu_usuarios()
            continue
        elif opcao == "2":
            registrar_acesso()
        elif opcao == "3":
            consultar_acessos()
        elif opcao == "4":
            consultar_log()
        elif opcao == "0":
            print("Encerrando o SentinelaLog.")
            break
        else:
            print("Opção inválida.")
        pausar()


# ---------------------------------------------------------------
# Início do programa
# ---------------------------------------------------------------
if __name__ == "__main__":
    criar_bloqueados_se_nao_existir()
    menu_principal()