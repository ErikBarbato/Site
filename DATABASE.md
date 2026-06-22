# DATABASE.md

> **INSTRUÇÕES PARA O ESTUDANTE**
>
> Este documento define **como os dados do sistema serão estruturados e armazenados**.
>
> 1. Preencha todos os campos entre `[ ]`.
> 2. Escolha uma opção quando houver alternativas.
> 3. Mantenha consistência com `PRD.md` e `ARCHITECTURE.md`.
> 4. Este arquivo será usado pelo agente para gerar modelos e queries.
> 5. Não misture regras de negócio aqui (isso pertence ao PRD).

---

# Visão Geral do Banco de Dados

Banco escolhido: PostgreSQL

Tipo de Banco de Dados: Relacional

Estratégia de armazenamento: 
Banco relacional com tabelas normalizadas em conformidade com as Formas Normais (1NF, 2NF, 3NF), garantindo a consistência das referências via chaves primárias e secundárias fornecidas nativamente pelo banco de dados.

---

# Modelo de Dados (Entidades)

## Entidade 1
Nome da entidade: user

Descrição:
Representação das contas de usuários do sistema, diferenciadas pelos perfis e níveis de permissão.

Atributos:
| Campo         | Tipo          | Obrigatório | Exemplo                              |
| ------------- | ------------- | ----------- | ------------------------------------ |
| id            | UUID          | Sim         | 550e8400-e29b-41d4-a716-446655440000 |
| name          | VARCHAR(255)  | Sim         | Carlos Eduardo                       |
| email         | VARCHAR(255)  | Sim         | carlos@educacao.com.br               |
| password      | VARCHAR(255)  | Sim         | pbkdf2_sha256$260000$db726as...      |
| role          | VARCHAR(20)   | Sim         | professor                            |
| cadastrado_em | TIMESTAMP     | Sim         | 2026-06-22 08:00:00                  |

Regras de validação:
* O e-mail deve seguir o padrão RFC 5322 e ser obrigatoriamente único na tabela.
* O campo role deve conter estritamente um dos seguintes valores string: 'admin', 'professor', 'aluno'.

---

## Entidade 2
Nome da entidade: tema

Descrição:
Estrutura macro de categorização para as divisões principais das áreas de estudo e conhecimento.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 1                                    |
| nome              | VARCHAR(100)  | Sim         | Matemática Aplicada                  |
| cadastrado_por_id | UUID          | Sim         | 550e8400-e29b-41d4-a716-446655440000 |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:10:00                  |

Regras de validação:
* O nome do tema deve ser único para evitar duplicações na árvore de navegação.
* O campo cadastrado_por_id deve apontar apenas para usuários com perfil 'admin'.

---

## Entidade 3
Nome da entidade: subtema

Descrição:
Subdivisão específica de conhecimento que pertence obrigatoriamente a um tema pai e agrupa os vídeos diretamente.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 12                                   |
| nome              | VARCHAR(100)  | Sim         | Cálculo Diferencial                  |
| tema_id           | BIGINT        | Sim         | 1                                    |
| cadastrado_por_id | UUID          | Sim         | 550e8400-e29b-41d4-a716-446655440000 |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:15:00                  |

Regras de validação:
* A combinação de nome e tema_id deve ser única na tabela.
* O campo tema_id não pode ser nulo (restrição de integridade referencial).

---

## Entidade 4
Nome da entidade: video

Descrição:
Registro de metadados e referências de URLs de streaming dos conteúdos educacionais postados pelos docentes.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | UUID          | Sim         | 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d |
| titulo            | VARCHAR(255)  | Sim         | Introdução a Limites e Derivadas     |
| descricao         | TEXT          | Sim         | Aula teórica conceitual sobre limites|
| url_streaming     | VARCHAR(500)  | Sim         | https://www.youtube.com/watch?v=dQw4|
| ativo             | BOOLEAN       | Sim         | true                                 |
| cadastrado_por_id | UUID          | Sim         | e3084ba4-9725-4cde-a178-5db772183e8b |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:20:00                  |

Regras de validação:
* A url_streaming deve ser uma URL estruturalmente válida contendo o protocolo HTTP ou HTTPS.
* O campo cadastrado_por_id deve referenciar um usuário cujo atributo role seja 'professor'.

---

## Entidade 5
Nome da entidade: video_subtemas

Descrição:
Tabela relacional intermediária responsável por gerenciar o relacionamento muitos-para-muitos (N:N) entre Vídeos e Subtemas.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 550                                  |
| video_id          | UUID          | Sim         | 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d |
| subtema_id        | BIGINT        | Sim         | 12                                   |

Regras de validação:
* A combinação do par video_id e subtema_id deve ser estritamente única, impedindo a redundância de vínculos idênticos.

---

## Entidade 6
Nome da entidade: comentario

Descrição:
Interações e registros em formato textual deixados pelos usuários na página de exibição de um vídeo específico.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 9811                                 |
| texto             | TEXT          | Sim         | Excelente didática nesta explicação! |
| video_id          | UUID          | Sim         | 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d |
| cadastrado_por_id | UUID          | Sim         | a578a12e-147c-48be-814d-9a99fe4260f1 |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:25:00                  |

Regras de validação:
* O campo texto não pode conter strings vazias ou compostas puramente por espaços em branco.

---

## Entidade 7
Nome da entidade: avaliacao

Descrição:
Registro de notas numéricas pontuais dadas pelos discentes e docentes para qualificar os vídeos.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 4321                                 |
| nota              | SMALLINT      | Sim         | 5                                    |
| video_id          | UUID          | Sim         | 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d |
| cadastrado_por_id | UUID          | Sim         | a578a12e-147c-48be-814d-9a99fe4260f1 |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:30:00                  |

Regras de validação:
* A nota deve obrigatoriamente respeitar a restrição numérica inteira do intervalo entre 1 e 5.
* Um usuário só pode registrar uma única linha por video_id (restrição UNIQUE composta entre `cadastrado_por_id` e `video_id`).

---

## Entidade 8
Nome da entidade: curtida_comentario

Descrição:
Interações pontuais de gostei (likes) direcionadas unicamente para sinalizar engajamento em comentários.

Atributos:
| Campo             | Tipo          | Obrigatório | Exemplo                              |
| ----------------- | ------------- | ----------- | ------------------------------------ |
| id                | BIGINT        | Sim         | 76543                                |
| comentario_id     | BIGINT        | Sim         | 9811                                 |
| cadastrado_por_id | UUID          | Sim         | e3084ba4-9725-4cde-a178-5db772183e8b |
| cadastrado_em     | TIMESTAMP     | Sim         | 2026-06-22 08:32:00                  |

Regras de validação:
* Deve haver unicidade relacional estrita contendo a chave composta pelos campos comentario_id e cadastrado_por_id para evitar curtidas duplicadas do mesmo autor no mesmo comentário.

---

# Relacionamentos

## Relação 1

tema → subtema

Tipo de relação: 1:N

Descrição: Um Tema macro contém e ramifica-se em múltiplos Subtemas secundários, mas cada Subtema aponta e está contido estritamente em um único Tema pai.

---

## Relação 2

video → subtema

Tipo de relação: N:N

Descrição: Um Vídeo pode abranger múltiplos Subtemas integrados, e um Subtema do ecossistema educacional pode estar presente e indexado em múltiplos Vídeos publicados. A relação é intermediada por video_subtemas.

---

## Relação 3

video → comentario

Tipo de relação: 1:N

Descrição: Um Vídeo centralizado recebe e exibe múltiplos comentários textuais históricos enviados pela comunidade discente e docente.

---

## Relação 4

video → avaliacao

Tipo de relação: 1:N

Descrição: Um Vídeo consolida e acumula múltiplas notas de Avaliação, respeitando a limitação de uma nota exclusiva por usuário em cada vídeo.

---

## Relação 5

comentario → curtida_comentario

Tipo de relação: 1:N

Descrição: Um Comentário pode receber múltiplos registros independentes de curtidas de usuários diferentes.

---

# Regras de Integridade

* O endereço eletrônico contido em `user.email` deve possuir restrição de unicidade (UNIQUE) ativa em nível de engine do banco de dados.
* Nenhuma linha pode ser mantida de forma órfã no banco de dados, sendo obrigatória a presença de Chaves Primárias válidas e Chaves Estrangeiras apontando para registros reais existentes nas tabelas correspondentes.
* Chaves compostas de unicidade aplicadas em `avaliacao` (`cadastrado_por_id`, `video_id`) e `curtida_comentario` (`cadastrado_por_id`, `comentario_id`) garantem a não-duplicação de interações pelo mesmo indivíduo.

---

# Índices e Performance

Índices necessários:
* B-Tree index na coluna `email` dentro da tabela `user` para otimizar o processo de autenticação de usuários.
* B-Tree index composto nas colunas `video_id` e `subtema_id` na tabela pivô `video_subtemas` para acelerar filtros de busca por eixos e trilhas.
* B-Tree index na coluna `video_id` nas tabelas `comentario` e `avaliacao` visando otimizar o tempo de carregamento das telas de exibição.

---

# Estratégia de performance

* Indexação de campos de busca frequentes, como chaves estrangeiras e campos de filtro comuns.
* Paginação obrigatória em nível de query (através de LIMIT e OFFSET ou paginação baseada em cursor) para todas as listagens volumosas de mídias e comentários.
* Utilização de queries otimizadas em nível de ORM via `select_related` e `prefetch_related` para mitigar o problema clássico de gargalo de performance N+1 nas entidades relacionadas.

---

# Migrations

## Estratégia de versionamento
ORM gerenciado (Prisma, TypeORM, Django ORM)

---

## Ferramenta de migrations
Django ORM

---

# Regras de Exclusão e Atualização

## Exclusão
* Hard delete com comportamento controlado via restrições `ON DELETE CASCADE` para que a exclusão programada de entidades pai (como um Vídeo ou um Comentário) limpe automaticamente as tabelas de interações dependentes (`comentario`, `avaliacao`, `curtida_comentario`).
* Bloqueio preventivo (`ON DELETE PROTECT`) na exclusão de Temas e Subtemas caso existam vídeos ativamente vinculados a essas estruturas.

---

## Atualização
* Atualização parcial via requisições HTTP do tipo PATCH totalmente permitida para a flexibilidade de dados do sistema, exceto sobre atributos identificadores.
* O campo identificador primário universal (`id`), as chaves de auditoria (`cadastrado_por_id`) e os campos timestamps de criação (`cadastrado_em`) são imutáveis e protegidos contra mutações pós-inserção.

---

# Segurança de Dados

* Criptografia irreversível das credenciais de acesso via algoritmo PBKDF2 com hash SHA256 (padrão robusto e nativo do Django), impedindo o armazenamento de senhas textuais limpas.
* Limpeza e sanitização completa de campos sensíveis para evitar vazamentos acidentais em logs da aplicação, omitindo dados de autenticação nas saídas do sistema.

---

# Backup e Recuperação

Estratégia de backup:
* Rotina de backup diário automático (Snapshot completo do PostgreSQL lógico).
* Política de retenção cíclica estipulada para os últimos 7 dias.
* Armazenamento dos arquivos de despejo (`.sql` compactados) criptografados e enviados para um serviço seguro de cloud storage.

---

Recuperação:
* Restore completo do banco de dados a partir do arquivo de dump mais recente em ambiente de homologação antes de apontar para a produção em cenários de desastre recovery.

---

# Restrições do Banco

* Proibido criar tabelas, campos ou associações relacionais que desrespeitem as definições de escopo estabelecidas no `PRD.md`.
* Todos os nomes de tabelas, colunas, chaves e constraints devem adotar rigorosamente a padronização de nomenclatura tipográfica em formato `snake_case`.

---

# CHECK FINAL
Antes de finalizar, verificar:
* [x] Todas as entidades do PRD estão representadas
* [x] Relacionamentos coerentes
* [x] Tipos de dados definidos corretamente
* [x] Regras de integridade claras
* [x] Compatível com arquitetura definida