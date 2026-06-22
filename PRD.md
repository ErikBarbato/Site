# PRD.md (Product Requirements Document)



# Escopo do Sistema

## Funcionalidades Principais

O sistema deverá permitir:
* Autenticação segura e controle de acessos baseado em três perfis distintos de usuários: Aluno, Professor e Administrador.
* Criação e organização hierárquica das trilhas curriculares divididas estritamente em Temas e Subtemas.
* Cadastro, edição, listagem detalhada e desativação de links de conteúdos em vídeo por parte dos professores.
* Navegação fluida pelas árvores de conhecimento, permitindo aos alunos filtrar, buscar e reproduzir as mídias disponíveis.
* Inserção de comentários textuais cronológicos, atribuição de notas de avaliação para os vídeos e registro de curtidas (likes) nos comentários.

---

## Funcionalidades Fora do Escopo

Liste o que o sistema NÃO deve fazer:

* Hospedagem direta e armazenamento nativo de arquivos pesados de mídia de vídeo (como formatos MP4 ou MKV), utilizando apenas links externos.
* Transmissões ao vivo ou qualquer modalidade de streaming e chat em tempo real.
* Sistema de chat por mensagens privadas ou canais fechados de comunicação individual entre os usuários.

---


# Regras de Negócio

Defina regras importantes do sistema.
* Um subtema deve obrigatoriamente estar associado a um tema pai, e nenhum vídeo pode ser cadastrado sem estar vinculado a pelo menos um subtema válido.
* Apenas usuários autenticados com privilégios de Administrador possuem permissão para criar, alterar ou remover estruturas de Temas e Subtemas.
* O perfil Professor herda todas as capacidades de consumo e interação do perfil Aluno, adicionando as permissões exclusivas para gerenciar seus próprios vídeos publicados.
* Toda operação de persistência de registros no banco de dados deve capturar automaticamente o ID do usuário autor e o timestamp atual do servidor.

---

# Requisitos Funcionais

Os requisitos funcionais descrevem o que o sistema faz.

## RF01 - Autenticação e Controle de Acesso
Descrição: O sistema deve permitir o login seguro de usuários e controlar o acesso às rotas privadas com base no perfil logado.
Ator: Usuário Geral
Pré-condições:
* O usuário deve possuir credenciais pré-cadastradas válidas no sistema.
Fluxo principal:
1. O usuário informa o e-mail e a senha na tela de login.
2. O sistema valida as credenciais fornecidas consultando o banco de dados.
3. O sistema gera e retorna um Token JWT válido contendo as informações e os escopos do perfil.
4. O sistema concede acesso às rotas e recursos restritos adequados ao nível de permissão.
Fluxos alternativos:
- Credenciais inválidas ou não encontradas → O sistema bloqueia o acesso e retorna erro de autenticação.
Pós-condições:
Sessão segura de usuário estabelecida no ecossistema com Token JWT ativo.

---

## RF02 - Gerenciamento de Vídeos Educacionais
Descrição: O sistema deve permitir que os professores publiquem e gerenciem mídias digitais na plataforma, exigindo que cada conteúdo seja obrigatoriamente acoplado a pelo menos um subtema cadastrado.
Ator: Professor
Pré-condições:
* O professor deve estar autenticado no sistema com um token JWT válido.
Fluxo principal:
1. O professor preenche o formulário com o título, a descrição didática e a URL externa do vídeo hospedado.
2. O professor seleciona pelo menos um subtema de conhecimento correspondente na listagem disponível.
3. O sistema valida a integridade das informações e a existência dos subtemas informados.
4. O sistema salva o vídeo atrelando de forma automática o ID do professor e o timestamp do momento de criação.
Fluxos alternativos:
- Payload enviado sem nenhum subtema selecionado → O sistema rejeita o salvamento e retorna erro de campo obrigatório.
Pós-condições:
Vídeo ativo e indexado com sucesso na árvore de categorias para consumo dos alunos.

---

## RF03 - Visualização de Conteúdo e Envio de Feedback
Descrição: O sistema deve permitir que estudantes assistam a vídeos ativos e deixem interações sociais opcionais como comentários textuais, avaliações em notas ou marcações de curtidas.
Ator: Aluno
Pré-condições:
* O aluno deve estar logado e com acesso liberado ao ambiente de estudos.
Fluxo principal:
1. O aluno navega pelas categorias e clica no card do vídeo ativo que deseja consumir.
2. O sistema renderiza a tela de exibição com o player incorporado correspondente à URL armazenada.
3. O aluno opcionalmente insere um comentário de texto ou seleciona uma nota para avaliar o conteúdo.
4. O sistema processa e grava a interação vinculando-a ao ID do vídeo e ao perfil do estudante.
Fluxos alternativos:
- O vídeo selecionado possui status desativado no sistema → O sistema bloqueia a exibição e retorna erro de conteúdo indisponível.
Pós-condições:
Feedback registrado com sucesso no banco de dados e adicionado cronologicamente na página do vídeo.

---

# Requisitos Não Funcionais

## RNF01 - Performance
Descrição: O sistema deve responder requisições de listagem e buscas com rapidez para garantir fluidez nas trilhas de aprendizado.
Métrica: 
- Tempo máximo de resposta: 2 segundos
Condição de carga:
- Até 1000 usuários simultâneos acessando as consultas
Critério de aceitação:
- 95% das requisições de renderização de listas de vídeos devem responder abaixo de 2 segundos.

---

## RNF02 - Segurança
Descrição: Os dados sensíveis dos usuários e as rotas de modificação devem ser protegidos contra acessos maliciosos.
* Autenticação baseada obrigatoriamente em cabeçalhos com tokens JWT válidos para requisições privadas.
* Armazenamento de senhas no banco de dados protegido por algoritmos de criptografia de hash seguro.

---

## RNF03 - Usabilidade
Descrição: A interface com o usuário deve ser limpa, intuitiva e acessível em múltiplos dispositivos.
* Interface gráfica construída sob o padrão web responsivo, adaptando-se perfeitamente para monitores desktop, tablets e smartphones.

---

## RNF04 - Escalabilidade
Descrição: A arquitetura do banco deve prever crescimento contínuo de dados sem comprometer a performance geral do ecossistema.
* Uso de índices explícitos nas colunas relacionais mais consultadas das tabelas (`video_id`, `subtema_id`) para mitigar gargalos à medida que o volume de interações crescer.

---

## RNF05 - Confiabilidade
Descrição: Resiliência contra falhas e garantia de consistência relacional de dados.
* O sistema de banco de dados PostgreSQL deve manter restrições (`CONSTRAINTS`) rígidas com comportamento em cascata (*CASCADE*) para que a remoção de um vídeo exclua as interações dependentes.
* Manutenção de uma taxa mínima de 99% de disponibilidade para a API de backend.

---

## RNF06 - Manutenibilidade
Descrição: O código do ecossistema backend deve ser claro, modular e devidamente testado para mitigar regressões de software.
* Separação estrita de responsabilidades no padrão Django por meio do isolamento de funcionalidades em aplicações separadas (`apps/`).
* Cobertura de testes automatizados com Pytest contendo no mínimo 80% do código testado.

---

## RNF07 - Compatibilidade
Descrição: Uniformidade operacional da aplicação web nos ecossistemas modernos do mercado.
* O sistema deve renderizar e operar de forma idêntica e sem quebras visuais nos navegadores Google Chrome, Mozilla Firefox, Safari e Microsoft Edge.

---


# Casos de Uso

## UC01 - Publicar Vídeo Educacional

Ator: Professor

Fluxo principal:
1. O professor acessa o painel de gerenciamento de conteúdo e clica em "Novo Vídeo".
2. Insere o título, a descrição didática e o link URL do vídeo hospedado externamente.
3. Seleciona o subtema de conhecimento correspondente na árvore de categorias.
4. Confirma a publicação e o sistema grava o registro inserindo os dados automáticos de auditoria.

---

## UC02 - Assistir Vídeo e Emitir Nota de Avaliação

Ator: Aluno

Fluxo principal:
1. O aluno navega pelos eixos temáticos e clica no card do vídeo ativo que deseja assistir.
2. O sistema inicia a reprodução do player de mídia na página correspondente.
3. O aluno seleciona a nota numérica desejada no painel de feedback.
4. Confirma o envio e o sistema recalcula instantaneamente a média e registra a avaliação.

---



# Dados do Sistema (Visão Geral)

Entidades principais
* User (Usuário)
* Tema
* Subtema
* Video (Vídeo)
* Comentario
* Avaliacao
* Like

---

# Critérios de Aceitação

Para considerar o sistema correto, ele deve:
* Bloquear terminantemente o salvamento ou a modificação de qualquer vídeo cujo payload não informe ao menos um subtema válido.
* Rejeitar chamadas de modificação, criação ou deleção em Temas e Subtemas originadas por tokens JWT que não possuam a role de Administrador.
* Garantir que todas as interações sociais (comentários, avaliações e likes) exijam validação de token de uma conta autenticada e ativa.

---

# Restrições do Projeto

* O desenvolvimento do ecossistema backend deve obedecer estritamente ao uso da linguagem Python utilizando o framework Django (Django REST Framework).
* O sistema gerenciador de banco de dados relacional para persistência de dados estruturados deve ser obrigatoriamente o PostgreSQL.
* Toda a nomenclatura de pastas, arquivos, tabelas do banco e variáveis de código deve seguir estritamente o padrão de convenção `snake_case`.

---

# Premissas

* Os usuários finais possuem computadores ou dispositivos eletrônicos com navegadores modernos e acesso à internet estável com banda suficiente para carregar players externos.
* Os links externos de vídeos configurados pelos professores apontam para mídias públicas e funcionais hospedadas em provedores de terceiros confiáveis.

---

# CHECK FINAL (para o estudante)

Antes de finalizar, revise:
* [x] Requisitos funcionais completos
* [x] Regras de negócio claras
* [x] Casos de uso definidos
* [x] Critérios de aceitação objetivos
* [x] Escopo bem delimitado