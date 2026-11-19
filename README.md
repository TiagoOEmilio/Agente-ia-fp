# 🛡️ SentinelaLog
 
**Sistema de controle de acesso e monitoramento de segurança para laboratórios de informática, desenvolvido em Python e executado no terminal.**
 
> ⚠️ **Projeto didático.** Todos os dados usados e gerados são **fictícios**. Não cadastre pessoas reais, nem informações de sistemas da escola ou de terceiros.
 
---
 
## 📌 Sobre o projeto
 
Ana é responsável pelo laboratório de informática de uma escola: trinta máquinas, dezenas de usuários e funcionamento das 7h às 22h. Numa madrugada, alguém acessou a conta de um professor e apagou arquivos. Ana só descobriu dois dias depois e não tinha como saber **quem** foi, **de onde** veio, nem se aquilo **já tinha acontecido antes**.
 
O **SentinelaLog** resolve esse problema: registra os acessos ao laboratório, classifica cada um como **normal**, **suspeito** ou **crítico** (sempre explicando o porquê), alerta quando uma mesma máquina é usada por mais de um usuário, mantém uma **auditoria** de tudo o que é feito no próprio sistema e gera um **relatório de segurança**. Um módulo de **IA (Groq)** permite fazer perguntas em linguagem natural sobre os acessos.
 
---
 
## 🚀 Funcionalidades
 
| Área | O que o sistema faz |
|---|---|
| **Usuários (CRUD)** | Cadastrar, listar, editar e excluir usuários com nome, matrícula, perfil (estudante, professor, administrador), horário permitido e observações. |
| **Privacidade** | A matrícula aparece mascarada (`20******`). Existe uma opção específica, só para o administrador, para revelá-la, e cada revelação é registrada no log. |
| **Autenticação** | Login por máquina + matrícula + senha, com senha protegida por hash (PBKDF2), troca obrigatória no primeiro acesso e logout para trocar de conta. |
| **Acessos** | Registro e consulta de acessos (usuário, data/hora, máquina, resultado). Os registros **não podem ser editados** depois de gravados. |
| **Análise de risco** | Cada acesso recebe uma pontuação e uma classificação (normal / suspeito / crítico), com a lista de motivos. |
| **Máquinas bloqueadas** | Lista em `bloqueados.txt`. Máquina bloqueada não permite login e gera aviso ao registrar um acesso. |
| **Máquina compartilhada** | Alerta quando a mesma máquina teve acessos bem-sucedidos de mais de um usuário, dizendo quais. |
| **Auditoria** | Log (`auditoria.csv`) com operação, usuário afetado, autor da ação e data/hora, consultável pelo menu. |
| **Relatório de segurança** | Totais de acessos e falhas, usuários com mais falhas, movimento por horário e contagem de suspeitos/críticos. |
| **Extras** | Bloquear/desbloquear máquinas pelo menu, pedidos de bloqueio feitos por professores, módulo de notas para professores e **IA (Groq)** para análise de segurança e para explicar a situação de um aluno. |
 
---
 
## 📁 Estrutura do projeto
 
```text
Agente-ia-fp/
├── README.md          # Este manual
├── LICENSE            # Licença MIT
├── .gitignore         # Ignora dados gerados, chaves e arquivos temporários
└── main/
    ├── main.py        # Ponto de entrada: login e menus
    ├── funcoes.py     # Regras de negócio, arquivos, autenticação, risco, auditoria
    └── ia.py          # Integração com a IA da Groq
```
 
Os arquivos de dados (`usuarios.csv`, `acessos.csv`, `auditoria.csv`, `bloqueados.txt`, `notas.csv`, `solicitacoes_bloqueio.csv`) são **criados automaticamente** durante o uso e **não vão para o GitHub** (estão no `.gitignore`).
 
---
 
## ▶️ Como executar
 
**Requisitos:** Python 3.8 ou superior (testado com 3.12). Não é necessário `pip install`: só são usadas bibliotecas da biblioteca padrão. A internet só é necessária para os recursos de IA.
 
```bash
git clone https://github.com/TiagoOEmilio/Agente-ia-fp.git
cd Agente-ia-fp/main
python main.py        # ou: python3 main.py
```
 
> 📌 **Execute sempre de dentro da pasta `main/`.** Os arquivos de dados são criados e lidos na pasta onde o programa é iniciado. Rodar de outra pasta cria outro conjunto de arquivos e parece que "os dados sumiram".
 
### Primeira execução
 
Se não houver nenhum administrador com senha, o sistema abre a tela **PRIMEIRO ACESSO** e pede:
 
1. Matrícula do administrador (mínimo de 3 caracteres);
2. Nome;
3. Senha (mínimo de 6 caracteres, com confirmação).
Depois disso, aparece a tela de login.
 
### Configurar a IA (opcional)
 
1. Crie uma chave em <https://console.groq.com/keys>.
2. Crie o arquivo **`main/api.env`** (na mesma pasta do `ia.py`) com:
```text
GROQ_API_KEY=cole_sua_chave_aqui
GROQ_MODEL=openai/gpt-oss-120b
```
 
   `GROQ_MODEL` é opcional (o padrão é `openai/gpt-oss-120b`). Também é possível definir `GROQ_API_KEY` como variável de ambiente no terminal.
 
3. **Nunca** coloque a chave dentro do código nem faça commit do `api.env` (ele já está no `.gitignore`).
> ⚠️ O programa lê **somente** o arquivo `api.env`. Um arquivo chamado `.env` é ignorado.
 
---
 
## 📖 Manual do usuário
 
### 1. Login
 
O sistema pergunta:
 
1. **Qual computador você está usando** (ex.: `PC-01`; digite `0` para sair). O nome é convertido para maiúsculas;
2. **Matrícula**;
3. **Senha** (não aparece na tela).
Regras do login:
 
- São **3 tentativas**. Ao errar as 3, o programa informa o limite e **encerra**.
- Se a **máquina estiver bloqueada, ninguém entra, nem o administrador**. A tentativa é registrada e o sistema pede outra máquina.
- Todo login (com sucesso ou falha) de uma matrícula **cadastrada** entra no `acessos.csv`, já classificado. Tentativas com matrícula inexistente ficam apenas no log de auditoria.
- Usuários criados (ou com senha redefinida) pelo administrador **precisam trocar a senha no primeiro login**. A nova senha deve ser diferente da atual.
### 2. Menu e permissões
 
O menu é montado conforme o perfil, e a numeração muda de acordo com as opções disponíveis. Além de esconder opções, as funções sensíveis **conferem o perfil novamente** antes de executar.
 
| Opção | Estudante | Professor | Administrador |
|---|:-:|:-:|:-:|
| Gerenciar usuários → Listar | ✅ | ✅ | ✅ |
| Gerenciar usuários → Cadastrar, Editar, Excluir, Revelar matrícula | ❌ | ❌ | ✅ |
| Registrar acesso | ✅ | ✅ | ✅ |
| Consultar acessos | ✅ (sem pontos) | ✅ (sem pontos) | ✅ (com pontos de risco) |
| Consultar log de auditoria | ✅ | ✅ | ✅ |
| Relatório de segurança | ✅ | ✅ | ✅ |
| Bloquear / Desbloquear máquina | ❌ | ❌ | ✅ |
| Ver solicitações de bloqueio | ❌ | ❌ | ✅ |
| Análise de segurança com IA | ❌ | ❌ | ✅ |
| Solicitar bloqueio de máquina | ❌ | ✅ | ❌ |
| Registrar nota, Boletim individual, Situação de aluno com IA | ❌ | ✅ | ❌ |
| Trocar de usuário (logout) | ✅ | ✅ | ✅ |
 
### 3. Gerenciar usuários
 
- **Cadastrar:** matrícula (mín. 3 caracteres, única), nome, perfil, horário permitido (hora inicial de 0 a 23 e final de 1 a 24, sempre com final maior que inicial), observações (opcional) e senha inicial.
- **Listar:** mostra matrícula mascarada, nome, perfil, horário e observações.
- **Editar:** em nome e observações, Enter mantém o valor atual; perfil, horário e senha perguntam antes se você quer alterar (`s/n`). O administrador **não pode remover o próprio perfil de administrador**.
- **Excluir:** pede confirmação. O administrador **não pode excluir a si mesmo**.
- **Revelar matrícula:** mostra a matrícula completa do usuário escolhido e **grava a operação no log**.
Em qualquer campo de texto, o caractere `;` não é aceito (ele separa os campos nos arquivos).
 
### 4. Registrar e consultar acessos
 
**Registrar acesso** pede matrícula, máquina de origem, resultado (1-sucesso, 2-falha) e data/hora (`AAAA-MM-DD HH:MM`, ou Enter para usar o momento atual). Em seguida o sistema mostra:
 
- o aviso de máquina bloqueada, se for o caso;
- a **classificação** e o **"Por quê"** (lista de motivos);
- o **alerta de máquina compartilhada**, se houver.
**Consultar acessos** lista data/hora, máquina, matrícula mascarada, classificação, motivos e resultado. O administrador também vê os **pontos de risco**.
 
### 5. Máquinas bloqueadas e solicitações
 
- **Bloquear máquina** (administrador) adiciona o nome ao `bloqueados.txt`. **Desbloquear** remove.
- Professores usam **Solicitar bloqueio de máquina** (máquina + motivo). O administrador vê os pedidos em **Ver solicitações de bloqueio** e então decide se bloqueia.
- As solicitações continuam listadas como `PENDENTE` mesmo depois de a máquina ser bloqueada (o programa não atualiza o status).
### 6. Log de auditoria
 
**Consultar log de auditoria** mostra, para cada registro: data/hora, operação, usuário afetado e autor da ação. Operações registradas:
 
`LOGIN`, `LOGIN_FALHA`, `LOGIN_NEGADO_MAQUINA_BLOQUEADA`, `LOGOUT`, `TROCAR_SENHA`, `CADASTRAR_ADMIN_INICIAL`, `CADASTRAR_USUARIO`, `EDITAR_USUARIO`, `EXCLUIR_USUARIO`, `REVELAR_MATRICULA`, `REGISTRAR_ACESSO`, `BLOQUEAR_MAQUINA`, `DESBLOQUEAR_MAQUINA`, `SOLICITAR_BLOQUEIO_MAQUINA`, `CONSULTAR_RELATORIO_SEGURANCA`, `ANALISE_IA_GROQ`, `REGISTRAR_NOTA_ATIVIDADE`, `CONSULTAR_BOLETIM`, `CONSULTAR_SITUACAO_ALUNO_IA`.
 
### 7. Relatório de segurança
 
Mostra: total de acessos, quantos tiveram sucesso e quantos falharam, quantidade de normais/suspeitos/críticos, usuários com mais falhas (nome + matrícula mascarada) e o movimento por hora (ordenado do horário mais movimentado para o menos).
 
### 8. Módulo de IA (Groq)
 
**Análise de segurança com IA** (administrador):
 
1. O sistema avisa quais dados serão enviados e pede confirmação (`s/n`);
2. Você pode digitar uma **pergunta específica** (até 300 caracteres) ou apertar Enter para uma análise geral;
3. Na análise geral, a IA responde com resumo, pontos de atenção, ações recomendadas e limitações da análise. Com uma pergunta específica, ela responde à pergunta usando os mesmos dados.
O que é enviado à Groq: um **resumo anonimizado** (totais calculados localmente + os últimos 150 eventos), com perfis, horários, nomes de máquinas, resultados, classificações e motivos, além da pergunta digitada. **Nomes e matrículas não são enviados**: cada matrícula vira `USUARIO_n` e só é traduzida de volta no computador do administrador, ao exibir a resposta. A IA **apenas sugere**; quem age é o administrador.
 
**Consultar situação de aluno com IA** (professor): pede a matrícula do aluno e uma pergunta (sem nome nem matrícula). A média ponderada e a situação são **calculadas pelo programa** (média ≥ 7: aprovado; ≥ 4: final; < 4: reprovado) e a IA apenas explica. As notas, os pesos e as descrições das atividades são enviados à Groq **sem pedido de confirmação**, então use apenas dados fictícios.
 
### 9. Notas (professores)
 
- **Registrar nota por atividade:** matrícula do estudante, categoria (projeto, atividade, prova, extra), descrição, nota (0 a 10) e peso (maior que 0).
- **Consultar boletim individual:** lista as notas do estudante e a média ponderada.
---
 
## 🔐 Decisões de segurança
 
### Critérios de classificação de acessos
 
A classificação usa um **sistema de pontos**. Cada critério somado gera uma explicação textual, mostrada junto com o resultado.
 
| Critério | Pontos | Por quê |
|---|:-:|---|
| Acesso com **falha** | +1 | Erro de digitação é comum, então uma falha isolada merece atenção, mas não alarme. |
| **Fora do horário** permitido do usuário | +1 | O horário é definido por usuário. Um acesso de madrugada foi exatamente o incidente que motivou o projeto. |
| Origem em **máquina bloqueada** | +2 | O administrador já declarou a máquina não confiável, então esse critério sozinho já basta para ser crítico. |
 
| Pontuação total | Classificação |
|:-:|---|
| 0 | **normal** |
| 1 | **suspeito** |
| 2 ou mais | **crítico** |
 
Exemplo: uma falha às 3h para um usuário com horário das 7h às 18h soma 1 + 1 = 2 pontos e é **crítica**.
 
Detalhes do cálculo:
 
- A hora é comparada por hora cheia, e o **horário final é exclusivo**: para quem tem 7h às 18h, 17:59 é normal e 18:00 já é fora do horário.
- Escolhemos pontos em vez de uma cadeia de `if`s para que a regra seja **explicável** (cada ponto tem um motivo escrito) e fácil de ajustar.
### Outras decisões
 
- **Senhas:** nunca guardadas em texto puro. São armazenadas como `salt$hash`, com PBKDF2-HMAC-SHA256, salt aleatório de 16 bytes e 200 mil iterações. O salt impede que senhas iguais gerem hashes iguais, e as iterações encarecem ataques de força bruta. A comparação usa `secrets.compare_digest`.
- **Troca obrigatória de senha:** quem define a senha inicial é o administrador, então ela não pode continuar valendo.
- **Matrículas mascaradas:** reduz a exposição acidental de dados (alguém olhando a tela, captura de tela). Revelar é uma ação explícita, restrita ao administrador e auditada.
- **Registros de acesso imutáveis:** o programa só **acrescenta** linhas ao `acessos.csv`; não existe função de edição. Se um registro pudesse ser alterado, quem invadiu poderia apagar seus rastros e a evidência perderia valor.
- **Quem monitora também é monitorado:** o administrador pode revelar matrículas, excluir usuários e bloquear máquinas. Por isso toda operação relevante grava **quem fez** (campo `autor`), em quê e quando. Sem isso, o próprio sistema de segurança seria o ponto cego.
- **Defesa em camadas nos perfis:** o menu esconde opções, e as funções sensíveis (`exigir_admin`, `exigir_professor`) conferem o perfil de novo.
- **Máquina bloqueada nega o login para todos**, inclusive administradores, e a tentativa fica registrada como `falha` crítica.
- **IA com privacidade:** anonimização antes do envio, aviso e confirmação, higienização dos campos dos registros (como o nome da máquina) antes de irem ao prompt, instrução à IA de tratar os dados como dados (e não como ordens), e a IA só recomenda. Erros de rede ou da API são tratados e mostrados como mensagem, sem derrubar o programa.
- **Chaves fora do repositório:** a chave da Groq fica em `api.env`/variável de ambiente, e arquivos de dados e chaves estão no `.gitignore`.
---
 
## ⚠️ Restrições e limitações conhecidas
 
Perguntar "o que este sistema **não** detecta?" é parte do projeto. Hoje o SentinelaLog **não consegue** (ou só consegue parcialmente):
 
- **Confirmar a origem real do acesso.** O nome da máquina é digitado pelo usuário no login; não há endereço de rede nem identificação do hardware. Quem mente sobre a máquina não é pego.
- **Detectar uso de credenciais roubadas** em horário permitido e a partir de uma máquina comum: o acesso será classificado como **normal**.
- **Barrar força bruta:** não há bloqueio automático após N falhas. Depois de 3 erros o programa fecha, mas basta abri-lo de novo.
- **Registrar tentativas com matrícula inexistente** no `acessos.csv` (elas aparecem só no log de auditoria), portanto não entram no relatório nem na análise de IA.
- **Proteger os arquivos:** tudo é CSV/TXT em texto simples. Quem tiver acesso à pasta pode editar, apagar ou forjar registros sem passar pelo programa. Não há assinatura nem verificação de integridade.
- **Distinguir acessos reais de lançados à mão:** qualquer perfil logado pode usar *Registrar acesso* para qualquer matrícula e data. O log registra quem lançou, mas o registro em si parece igual a um acesso real.
- **Limitar o alerta de máquina compartilhada no tempo:** ele considera todo o histórico e só é exibido ao registrar um acesso manualmente (não no login). Com o tempo, quase toda máquina terá "vários usuários".
- **Horários que atravessam a meia-noite** (ex.: das 22h às 6h): o cadastro exige hora final maior que a inicial.
- **Uso simultâneo:** o programa assume um único terminal por vez; não há controle de concorrência nos arquivos.
- **Granularidade:** o horário é avaliado por hora cheia.
- O **log de auditoria e o relatório** podem ser consultados por qualquer perfil, e o log mostra as matrículas completas dos usuários afetados.
---
 
## 🗂️ Formato dos arquivos
 
Todos usam `;` como separador e UTF-8.
 
| Arquivo | Colunas |
|---|---|
| `usuarios.csv` | `matricula;nome;perfil;hora_inicio;hora_fim;observacoes;senha(salt$hash);trocar_senha` |
| `acessos.csv` | `matricula;data_hora;maquina;resultado;classificacao;motivos;pontos` |
| `auditoria.csv` | `data_hora;operacao;matricula_afetada;autor` |
| `bloqueados.txt` | uma máquina por linha |
| `notas.csv` | `matricula_aluno;matricula_professor;categoria;descricao;data;nota;peso` |
| `solicitacoes_bloqueio.csv` | `data_hora;matricula_professor;maquina;motivo;status` |
 
---
 
## 🧪 Roteiro de teste rápido
 
1. Rode `python main.py` dentro de `main/` e crie o administrador (ex.: matrícula `adm01`).
2. Faça login informando `PC-01`, `adm01` e a senha.
3. Em **Gerenciar usuários → Cadastrar**, crie um estudante (ex.: `aluno01`, horário 7 a 18) e um professor (ex.: `prof01`, horário 7 a 22).
4. Em **Registrar acesso**, lance para `aluno01` em `PC-02`: (a) sucesso às 10:00; (b) falha às 03:00. Compare as classificações e os motivos.
5. Registre um acesso **com sucesso** de `prof01` na mesma `PC-02` e veja o **alerta de máquina compartilhada**.
6. Em **Bloquear máquina**, bloqueie `PC-09`, saia (logout) e tente logar nela.
7. Veja **Consultar acessos**, **Relatório de segurança** e **Consultar log de auditoria**.
8. Use **Revelar matrícula** e confirme que a operação apareceu no log.
---
 
## 🛠️ Tecnologias
 
- **Python 3**, somente biblioteca padrão (nenhum pacote para instalar):
  - `os`, `datetime`: tela e datas;
  - `getpass`, `hashlib`, `secrets`: senha sem eco na tela, hash PBKDF2 e comparação segura;
  - `json`, `re`, `urllib`: comunicação com a API da Groq e higienização de texto;
  - `collections`, `pathlib`: contagens do resumo da IA e localização do `api.env`.
- Arquivos **CSV** e **TXT** para armazenamento.
- **Groq API** (opcional) para os recursos de IA.
---
 
## 🎯 Objetivo acadêmico
 
Projeto desenvolvido na disciplina de **Fundamentos de Programação (FP)**, 2026.2, Turma B, para praticar Python, estruturas condicionais e de repetição, funções, tratamento de exceções, manipulação de arquivos e organização de programas, com foco em **segurança da informação**.
 
**Instituição:** Cesar School
 
## 👥 Integrantes do grupo
 
- Tiago Oliveira
- Iago Xavier
- Enzo Leal
- Mateus Dias
- Fernando Furlan
- Francisco Bispo
---
 
Licença [MIT](LICENSE). Desenvolvido por estudantes como parte de um projeto acadêmico.