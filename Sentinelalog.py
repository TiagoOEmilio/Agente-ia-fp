# SentinelaLog - sistema de controle de acessos em Python (terminal).
# Cadastro de usuários, registro de acessos e log de auditoria.


import os
from datetime import datetime
import getpass
import hashlib
import secrets

# ---------------------------------------------------------------
# Constantes (nomes dos arquivos e configurações)
# ---------------------------------------------------------------
ARQ_USUARIOS = "usuarios.csv"      # matricula;nome;perfil;hora_inicio;hora_fim;observacoes e senha_hash;senha_salt
ARQ_ACESSOS = "acessos.csv"        # matricula;data_hora;maquina;resultado;classificacao;motivos
ARQ_LOG = "auditoria.csv"          # data_hora;operacao;matricula_afetada
ARQ_BLOQUEADOS = "bloqueados.txt"  # uma máquina bloqueada por linha

SEP = ";"                          # separador dos campos nos arquivos
PERFIS = ["estudante", "professor", "administrador"]
PERFIL_ADMIN = "administrador"      # perfil do adm
CAMPOS_USUARIO = 7                  # qnt de campos em cada linha do usuarios.csv
usuario_logado = None               # variável global para armazenar o usuário logado

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
    """Mostra na tela todos os registros do log de auditoria."""
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
    """Limpa a tela do terminal (cls no Windows, clear nos demais sistemas)."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Espera o usuário apertar Enter antes de continuar."""
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
    """Mostra os perfis disponíveis e devolve o perfil escolhido."""
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

def ler_senha(mensagem):
    """Lê uma senha (sem mostrar na tela) e pede confirmação. Mínimo de 6 caracteres."""
    while True:
        senha = getpass.getpass(mensagem)
        if len(senha) < 6:
            print("A senha precisa ter pelo menos 6 caracteres.")
        elif getpass.getpass("Confirme a senha: ") != senha:
            print("As senhas não conferem.")
        else:
            return senha

#Autenticação e permissoões
def gerar_hash(senha, salt=None):
    """Devolve 'salt$hash'. A senha nunca é guardada em texto puro."""
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), bytes.fromhex(salt), 200_000)
    return f"{salt}${h.hex()}"
def verificar_senha(senha, armazenado):
    """Confere a senha digitada com o 'salt$hash' guardado no arquivo."""
    if "$" not in armazenado:
        return False  # usuário antigo, ainda sem senha definida
    salt = armazenado.split("$", 1)[0]
    return secrets.compare_digest(gerar_hash(senha, salt), armazenado)
def e_admin():
    """Devolve True se o usuário logado tem o perfil de administrador."""
    return usuario_logado is not None and usuario_logado[2] == PERFIL_ADMIN
def exigir_admin():
    """Barreira de segurança: usada no início de toda operação de escrita em usuários."""
    if e_admin():
        return True
    print("Acesso negado: apenas o administrador pode realizar esta operação.")
    return False
def admin_com_senha():
    """Devolve True se já existe algum administrador com senha cadastrada."""
    return any(u[2] == PERFIL_ADMIN and u[6] != "" for u in carregar_usuarios())

def configurar_primeiro_admin():
    """Primeira execução (ou nenhum admin utilizável): cria o administrador inicial."""
    print("\n=== PRIMEIRO ACESSO ===")
    print("Nenhum administrador com senha foi encontrado. Vamos criar o primeiro.")
    while True:
        matricula = ler_texto("Matrícula do administrador (mín. 3 caracteres): ")
        if len(matricula) < 3:
            print("A matrícula precisa ter pelo menos 3 caracteres.")
        elif buscar_usuario(matricula) is not None:
            print("Já existe um usuário com essa matrícula. Use outra.")
        else:
            break
    nome = ler_texto("Nome: ")
    senha = ler_senha("Senha: ")
    adicionar_linha(ARQ_USUARIOS,
                    [matricula, nome, PERFIL_ADMIN, "0", "24", "", gerar_hash(senha)])
    registrar_log("CADASTRAR_ADMIN_INICIAL", matricula)
    print("primeiro Adm criado")
def fazer_login():
    """Pede matrícula e senha (3 tentativas). Devolve True se o login der certo."""
    global usuario_logado
    print("\n=== LOGIN ===")
    for _ in range(3):
        matricula = ler_texto("Matrícula: ")
        senha = getpass.getpass("Senha: ")
        usuario = buscar_usuario(matricula)
        if usuario is not None and verificar_senha(senha, usuario[6]):
            usuario_logado = usuario
            registrar_log("LOGIN", matricula)
            return True
        print("Matrícula ou senha incorretos.")
        registrar_log("LOGIN_FALHA", matricula)
    print("Número máximo de tentativas atingido.")
    return False
# ---------------------------------------------------------------
# TÓPICO 1 - Usuários
# ---------------------------------------------------------------
def mascarar_matricula(matricula):
    """Mostra só os 2 primeiros caracteres. Ex.: 20240001 -> 20******"""
    return matricula[:2] + "*" * (len(matricula) - 2)

def carregar_usuarios():
    """Lê os usuários garantindo CAMPOS_USUARIO campos por linha (compatível com
    arquivos antigos, que não tinham a coluna da senha)."""
    usuarios = carregar_linhas(ARQ_USUARIOS)
    for u in usuarios:
        while len(u) < CAMPOS_USUARIO:
            u.append("")
    return usuarios

def buscar_usuario(matricula):
    """Devolve a lista de campos do usuário, ou None se não existir."""
    for usuario in carregar_usuarios():
        if usuario[0] == matricula:
            return usuario
    return None


def cadastrar_usuario():
    """Cadastra um novo usuário (somente administrador)."""
    if not exigir_admin():
        return
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
    senha = ler_senha("Senha inicial do usuário: ")
    adicionar_linha(ARQ_USUARIOS,
                    [matricula, nome, perfil, str(hora_inicio), str(hora_fim), observacoes, gerar_hash(senha)])
    registrar_log("CADASTRAR_USUARIO", matricula)
    print("Usuário cadastrado com sucesso!")


def listar_usuarios():
    """Mostra na tela os usuários cadastrados."""
    usuarios = carregar_usuarios()
    print("\n--- USUÁRIOS CADASTRADOS ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"Matrícula: {mascarar_matricula(u[0])} | Nome: {u[1]} | Perfil: {u[2]} "
              f"| Horário: {u[3]}h às {u[4]}h | Obs: {u[5]}")


def revelar_matricula():
    """Mostra a matrícula completa e registra isso no log."""
    if not exigir_admin(): 
        return
    print("\n--- REVELAR MATRÍCULA ---")
    usuarios = carregar_usuarios()
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
    """Edita os dados de um usuário já cadastrado (somente administrador)."""
    if not exigir_admin():
        return
    print("\n--- EDITAR USUÁRIO ---")
    matricula = ler_texto("Matrícula do usuário a editar: ")
    usuarios = carregar_usuarios()

    for u in usuarios:
        if u[0] == matricula:
            print("Deixe em branco e aperte Enter para manter o valor atual.")
            novo_nome = ler_texto(f"Nome [{u[1]}]: ", obrigatorio=False)
            novo_obs = ler_texto(f"Observações [{u[5]}]: ", obrigatorio=False)
            print(f"Perfil atual: {u[2]}")
            if input("Alterar perfil? (s/n): ").strip().lower() == "s":
                novo_perfil = ler_perfil()
                if u[0] == usuario_logado[0] and novo_perfil != PERFIL_ADMIN:
                    print("Você não pode remover o seu próprio perfil de administrador. "
                          "Perfil mantido.")
                else:
                    u[2] = novo_perfil
            print(f"Horário atual: {u[3]}h às {u[4]}h")
            if input("Alterar horário? (s/n): ").strip().lower() == "s":
                inicio = ler_inteiro("Início (0 a 23): ", 0, 23)
                fim = ler_inteiro("Fim (1 a 24): ", 1, 24)
                if fim <= inicio:
                    print("O horário final precisa ser maior que o inicial. Horário mantido.")
                else:
                    u[3], u[4] = str(inicio), str(fim)
            if input("Redefinir senha? (s/n): ").strip().lower() == "s":
                u[6] = gerar_hash(ler_senha("Nova senha: "))
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
    """Exclui um usuário cadastrado (somente administrador)."""
    if not exigir_admin():
        return
    print("\n--- EXCLUIR USUÁRIO ---")
    matricula = ler_texto("Matrícula do usuário a excluir: ")
    if matricula == usuario_logado[0]:
        print("Você não pode excluir o seu próprio usuário.")
        return
    usuarios = carregar_usuarios()

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
# ---------------------------------------------------------------=
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
    """Registra o acesso de um usuário a uma máquina e classifica o resultado."""
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
    """Mostra na tela os acessos já registrados."""
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
    """Menu de usuários: o administrador tem acesso completo e os demais só visualizam."""
    # Administrador: acesso completo. Demais perfis: somente visualização.
    if e_admin():
        opcoes = [("Cadastrar", cadastrar_usuario),
                  ("Listar", listar_usuarios),
                  ("Editar", editar_usuario),
                  ("Excluir", excluir_usuario),
                  ("Revelar matrícula", revelar_matricula)]
    else:
        opcoes = [("Listar", listar_usuarios)]

    while True:
        print("\n=== USUÁRIOS ===")
        for numero, (nome, _) in enumerate(opcoes, start=1):
            print(f"{numero}. {nome}")
        print("0. Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            break
        elif opcao.isdigit() and 1 <= int(opcao) <= len(opcoes):
            opcoes[int(opcao) - 1][1]()
        else:
            print("Opção inválida.")
        pausar()
    


def menu_principal():
    """Menu principal do programa, mostrado depois do login."""
    while True:
        limpar_tela()
        print("=== SentinelaLog ===")
        print(f"Logado como: {usuario_logado[1]} ({usuario_logado[2]})")
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
    if not admin_com_senha():
        configurar_primeiro_admin()
    if fazer_login():
        menu_principal()
