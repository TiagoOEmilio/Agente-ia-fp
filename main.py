# SentinelaLog - sistema de controle de acessos em Python (terminal).
# Aqui ficam os menus e o início do programa.
# As funções (arquivos, login, usuários, análise de risco...) estão no funcoes.py.


import funcoes

# Menus

def menu_usuarios():
    """Menu de usuários: o administrador tem acesso completo e os demais só visualizam."""
    # Administrador: acesso completo. Demais perfis: somente visualização.
    if funcoes.e_admin():
        opcoes = [("Cadastrar", funcoes.cadastrar_usuario),
                  ("Listar", funcoes.listar_usuarios),
                  ("Editar", funcoes.editar_usuario),
                  ("Excluir", funcoes.excluir_usuario),
                  ("Revelar matrícula", funcoes.revelar_matricula)]
    else:
        opcoes = [("Listar", funcoes.listar_usuarios)]

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
        funcoes.pausar()


def menu_principal():
    """Menu principal do programa, mostrado depois do login."""
    while True:
        funcoes.limpar_tela()
        print("=== SentinelaLog ===")
        # usuario_logado é lido direto do módulo funcoes: ele é preenchido
        # pelo fazer_login() e, se fosse importado com "from", ficaria None aqui.
        print(f"Logado como: {funcoes.usuario_logado[1]} ({funcoes.usuario_logado[2]})")
        print("1. Gerenciar usuários")
        print("2. Registrar acesso")
        print("3. Consultar acessos")
        print("4. Consultar log de auditoria")
        print("5. Trocar de usuário (logout)")
        print("6. Bloquear máquina")
        # Próximas opções (entregas futuras): máquinas compartilhadas,
        # relatório de segurança, funcionalidade extra e módulo de IA.
        print("7. Relatório de segurança")
        print("8. Desbloquear maquina")
        print("0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            menu_usuarios()
            continue
        elif opcao == "2":
            funcoes.registrar_acesso()
        elif opcao == "3":
            funcoes.consultar_acessos()
        elif opcao == "4":
            funcoes.consultar_log()
        elif opcao == "5":
            funcoes.fazer_logout()
            return True
        elif opcao == "6":
            funcoes.bloquear_maquina() # apenas adm 
        elif opcao == "7":
            funcoes.relatorio_seguranca()
        elif opcao == "8":
            funcoes.desbloquear_maquina() # apenas adm
        elif opcao == "0":
            print("Encerrando o SentinelaLog.")
            return False
        else:
            print("Opção inválida.")
        funcoes.pausar()
# Início do programa

if __name__ == "__main__":
    if not funcoes.admin_com_senha():
        funcoes.configurar_primeiro_admin()
    while funcoes.fazer_login():
        if not menu_principal():
            break
