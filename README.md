# 🛡️ SentinelaLog

**Sistema de Controle de Acesso e Monitoramento de Segurança desenvolvido em Python.**

## 📌 Sobre o projeto

O **SentinelaLog** é um sistema de controle de acessos desenvolvido em Python, executado diretamente pelo terminal. Seu objetivo é gerenciar usuários, registrar movimentações e auxiliar no monitoramento da segurança de ambientes, como laboratórios de informática.

O sistema permite cadastrar usuários com diferentes níveis de permissão, acompanhar tentativas de acesso e manter registros de auditoria para facilitar a identificação de atividades suspeitas.

## 🚀 Funcionalidades

- **Gerenciamento de usuários:** cadastro, consulta, edição e exclusão de usuários.
- **Perfis de acesso:** estudante, professor e administrador.
- **Controle de horários:** definição dos horários permitidos para cada usuário.
- **Registro de acessos:** armazenamento de data, horário, máquina utilizada e resultado da tentativa.
- **Análise de riscos:** classificação dos acessos como normais, suspeitos ou críticos.
- **Bloqueio de máquinas:** gerenciamento de máquinas bloqueadas.
- **Auditoria:** registro de operações importantes realizadas no sistema.
- **Relatórios de segurança:** apresentação de estatísticas sobre os acessos registrados.

## 🛠️ Tecnologias utilizadas

- **Python 3**
- Bibliotecas nativas:
  - `os`
  - `datetime`
  - `hashlib`
  - `secrets`
  - `getpass`
- Arquivos CSV e TXT para armazenamento dos dados.

## ▶️ Como executar o projeto

1. Instale o Python 3 em seu computador.
2. Faça o download ou clone este repositório:

   ```bash
   git clone https://github.com/TiagoOEmilio/Agente-ia-fp.git
   ```

3. Entre na pasta do projeto:

   ```bash
   cd Agente-ia-fp
   ```

4. Execute o arquivo principal:

   ```bash
   python main.py
   ```

5. Siga as opções apresentadas no menu do terminal.

## 📁 Estrutura do projeto

```text
Agente-ia-fp/
│
├── main.py          # Arquivo principal e menu do sistema
├── funcoes.py       # Funções e regras de funcionamento
├── usuarios.csv     # Dados dos usuários
├── acessos.csv      # Histórico de acessos
├── auditoria.csv    # Registros de auditoria
├── bloqueados.txt   # Lista de máquinas bloqueadas
└── README.md        # Documentação do projeto
```

*Os arquivos de dados podem ser criados automaticamente durante a utilização do sistema.*

## 🎯 Objetivo acadêmico

Este projeto foi desenvolvido como atividade acadêmica da disciplina de **Fundamentos de Programação (FP)**, com o objetivo de aplicar conhecimentos de Python, estruturas condicionais, repetição, funções, manipulação de arquivos e organização de programas.

## 👥 Integrantes do grupo

- Tiago Oliveira Emilio
- Iago Xavier
- Enzo Leal
- Mateus Dias
- Fernando Furlan
- Francisco Bispo

## 📚 Projeto acadêmico

**Disciplina:** Fundamentos de Programação (FP)  
**Linguagem:** Python  
**Instituição:** Cesar School

---

Desenvolvido por estudantes como parte de um projeto acadêmico.
