# INITIALIZATION.md - Diretrizes de Inicialização do Projeto

> **INSTRUÇÕES DE USO PARA O AGENTE E DESENVOLVEDORES**
>
> Este documento serve como a "fonte da verdade" técnica de inicialização do ecossistema. Ele cruza as definições do `PRD.md` (regras de negócio) com as do `DATABASE.md` (modelo relacional) para fornecer instruções e comandos explícitos que guiarão o agente de IA e os engenheiros de software na criação correta e íntegra do projeto.

---

# 1. Visão Geral do Alinhamento (PRD ↔ DATABASE)

Para que o agente consiga gerar o código sem quebrar regras funcionais, as tabelas do banco de dados PostgreSQL devem responder exatamente às necessidades descritas no PRD. Segue o mapa de correspondência estrita que deve ser lido antes de qualquer linha de código ser escrita:

| Requisito do PRD (Funcionalidade)        | Entidade no DATABASE.md      | Papel Técnico no Sistema                                      |
| ----------------------------------------- | ---------------------------- | ------------------------------------------------------------- |
| Autenticação e Perfis (Admin/Prof/Aluno)  | `auth_user`                  | Utiliza a tabela nativa do Django para gerenciar credenciais. |
| Navegação por Árvore de Categorias        | `tema` ↔ `subtema`           | Organização hierárquica (1:N) das trilhas de conteúdo.        |
| Upload e Streaming de Conteúdo            | `video`                      | Metadados e links convertidos de vídeos educacionais.         |
| Indexação Multitópicos dos Vídeos         | `video_subtemas`             | Relacionamento Muitos-para-Muitos (M2M) entre Vídeos/Subtemas|
| Fórum de Dúvidas e Discussões             | `comentario`                 | Interações textuais atreladas de forma ordenada aos vídeos.   |
| Qualificação do Conteúdo                  | `avaliacao`                  | Registro numérico limitado a uma nota única por usuário.      |
| Engajamento da Comunidade                 | `curtida_comentario`         | Sistema de likes para rankear comentários relevantes.         |

---

# 2. Configuração do Ambiente de Desenvolvimento (Python & Django)

Todas as ferramentas adotadas seguem o padrão arquitetural do Django ORM rodando sobre o banco PostgreSQL. Execute os comandos abaixo na ordem sequencial exata para preparar o esqueleto limpo do projeto:

### Passo 1: Inicialização do Ambiente Virtual e Dependências
```bash
# Criação do ambiente virtual isolado
python -m venv .venv

# Ativação do ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Ativação do ambiente virtual (Windows)
.venv\Scripts\activate

# Atualização do gerenciador de pacotes e instalação de dependências essenciais
pip install --upgrade pip
pip install django psycopg2-binary python-dotenv