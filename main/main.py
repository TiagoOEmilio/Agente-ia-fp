import funcoes
import ia
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
    """Menu principal do programa, mostrado depois do login.
    As opções de administrador só aparecem para o administrador."""
    while True:
        opcoes = [("Gerenciar usuários", menu_usuarios),
                  ("Registrar acesso", funcoes.registrar_acesso),
                  ("Consultar acessos", funcoes.consultar_acessos),
                  ("Consultar log de auditoria", funcoes.consultar_log),
                  # Próximas opções (entregas futuras): máquinas compartilhadas,
                  # funcionalidade extra e módulo de IA.
                  ("Relatório de segurança", funcoes.relatorio_seguranca)]
        if funcoes.e_admin():
            opcoes.append(("Bloquear máquina", funcoes.bloquear_maquina))
            opcoes.append(("Desbloquear máquina", funcoes.desbloquear_maquina))
            opcoes.append(("Análise de segurança com IA", ia.analisar_com_ia))
            opcoes.append(("ver solicitações de bloqueio", funcoes.consultar_solicitacoes_bloqueio))
        opcoes.append(("Trocar de usuário (logout)", funcoes.fazer_logout))

        if funcoes.usuario_logado[2] == "professor":
            opcoes.append(("Registrar nota por atividade", funcoes.registrar_nota_atividade))
            opcoes.append(("Consultar boletim individual", funcoes.consultar_boletim_individual))
            opcoes.append(("Solicitar bloqueio de máquina", funcoes.solicitar_bloqueio_maquina))
            opcoes.append(("consultar situação de aluno com IA", ia.consultar_situacao_aluno))
        
        funcoes.limpar_tela()
        print("=== SentinelaLog ===")
        # usuario_logado é lido direto do módulo funcoes: ele é preenchido
        # pelo fazer_login() e, se fosse importado com "from", ficaria None aqui.
        print(f"Logado como: {funcoes.usuario_logado[1]} ({funcoes.usuario_logado[2]})")
        for numero, (nome, _) in enumerate(opcoes, start=1):
            print(f"{numero}. {nome}")
        print("0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            print("Encerrando o SentinelaLog.")
            return False
        elif opcao.isdigit() and 1 <= int(opcao) <= len(opcoes):
            acao = opcoes[int(opcao) - 1][1]

            if acao == funcoes.fazer_logout:
                funcoes.fazer_logout()
                return True  
            if acao == menu_usuarios:
                continue  
            else:
                acao()
        else:
            print("Opção inválida.")
        funcoes.pausar()

if __name__ == "__main__":
    if not funcoes.admin_com_senha():
        funcoes.configurar_primeiro_admin()
    while funcoes.fazer_login():
        if not menu_principal():
            break
