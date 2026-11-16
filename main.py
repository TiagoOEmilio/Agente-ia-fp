# SentinelaLog - sistema de controle de acessos em Python (terminal).
# Aqui ficam os menus e o início do programa.
# As funções (arquivos, login, usuários, análise de risco...) estão no funcoes.py.


import funcoes
from funcoes import (
    criar_bloqueados_se_nao_existir,
    admin_com_senha,
    configurar_primeiro_admin,
    fazer_login,
    logout,
    e_admin,
    cadastrar_usuario,
    listar_usuarios,
    editar_usuario,
    excluir_usuario,
    revelar_matricula,
    registrar_acesso,
    consultar_acessos,
    consultar_log,
    limpar_tela,
    pausar,
)

# Menus

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
        # usuario_logado é lido direto do módulo funcoes: ele é preenchido
        # pelo fazer_login() e, se fosse importado com "from", ficaria None aqui.
        print(f"Logado como: {funcoes.usuario_logado[1]} ({funcoes.usuario_logado[2]})")
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
# Início do programa

if __name__ == "__main__":
    criar_bloqueados_se_nao_existir()
    if not admin_com_senha():
        configurar_primeiro_admin()
    if fazer_login():
        menu_principal()
