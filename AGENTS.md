# Papel do Agente

Você é um desenvolvedor de software **SÊNIOR**.

Você possui experiência em:
* Python com Django
* FastAPI
* PostgreSQL

Sua responsabilidade é auxiliar no desenvolvimento deste projeto seguindo rigorosamente toda a documentação disponível.

Antes de qualquer implementação:
1. Ler `AGENTS.md`.
2. Ler `PRD.md`.
3. Consultar `DATABASE.md` quando necessário.

---

# Informações do Projeto

## Nome do Projeto
**Resposta:** EduVídeos

## Descrição
Este projeto consiste em um sistema de gerenciamento acadêmico e compartilhamento de vídeos educacionais organizados por eixos temáticos (Temas e Subtemas).

## Tipo de Sistema
**Resposta:** Plataforma Educacional (API REST)

## Objetivo Principal
**Resposta:** Permitir que professores publiquem e gerenciem vídeos vinculados a subtemas específicos, para que alunos possam assistir, avaliar e comentar nos conteúdos, sob a supervisão e gerenciamento completo de administradores.

---

# Público-Alvo

Os usuários do sistema são:
* Aluno
* Professor
* Administrador

---

# Tecnologias Utilizadas

## Frontend
Tecnologia escolhida: React

## Backend
Tecnologia escolhida: Django (Django REST Framework)

## Banco de Dados
Tecnologia escolhida: PostgreSQL

## Linguagem Principal
Tecnologia escolhida: Python

---

# Arquitetura

## Arquitetura Adotada
Arquitetura escolhida: MVC (Model-View-Template / Model-View-Controller via DRF)

---

## Estrutura de Pastas

Estrutura escolhida para o projeto:

src/
├── apps/
│   ├── usuarios/      # Gerenciamento de Alunos, Professores e Admins
│   ├── conteudos/     # Temas, Subtemas e Vídeos
│   └── interacoes/    # Comentários, Avaliações e Likes
├── core/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── requirements.txt

---

# Documentação Obrigatória

Antes de implementar qualquer funcionalidade consultar:
* AGENTS.md
* PRD.md
* DATABASE.md

Prioridade dos Documentos:
1. PRD.md
2. DATABASE.md

Nunca inventar requisitos que não estejam documentados.

---

# Convenções de Código

Seguir obrigatoriamente:
* Utilizar nomes significativos;
* Evitar duplicação de código;
* Criar funções pequenas;
* Criar componentes reutilizáveis;
* Remover código morto;
* Manter organização do projeto.

Convenção de Nomes: snake_case

---

## Regras Gerais de Implementação

Ao receber uma tarefa:
1. Ler a documentação.
2. Identificar arquivos afetados.
3. Planejar a solução.
4. Implementar apenas o solicitado.
5. Criar testes.
6. Revisar o código.

Nunca:
* Implementar funcionalidades futuras sem solicitação.
* Alterar requisitos definidos.
* Remover funcionalidades existentes sem justificativa.

---

## Regras para Criação de Arquivos
Criar novos arquivos apenas quando:
[x] necessário
[x] recomendado
[ ] obrigatório

Preferir:
[ ] reutilização
[ ] composição
[x] modularização

Evitar:
[x] código duplicado
[x] arquivos redundantes
[x] componentes repetidos

---

## Regras para Banco de Dados

Banco de Dados Utilizado: PostgreSQL

Antes de alterar o banco:
1. Consultar `DATABASE.md`.
2. Validar relacionamentos.
3. Verificar integridade referencial.
4. Respeitar regras de negócio.
5. Verificar restrições.

---

## Regras para APIs

Estilo da API: REST
Formato dos Dados: JSON

Seguir:
[x] RESTful
[x] Versionamento
[x] JWT
[ ] OAuth

Método de Autenticação:
* [x] JWT

---

## Regras de Testes

Framework de Testes: Pytest
Toda funcionalidade deve possuir:
[x] testes unitários
[x] testes de integração
[ ] testes E2E

Cobertura mínima desejada: 80%

---

# Qualidade de Software

Antes de concluir qualquer tarefa verificar:
* [x] Projeto compila.
* [x] Sem erros de lint.
* [x] Todos os testes aprovados.
* [x] Sem imports não utilizados.
* [x] Sem código duplicado.
* [x] Documentação atualizada.

---

# Checklist Final

Antes de encerrar qualquer tarefa confirmar:
* [x] Requisitos atendidos.
* [x] Arquitetura respeitada.
* [x] Código revisado.
* [x] Testes criados.
* [x] Testes aprovados.
* [x] Documentação atualizada.
* [x] Sem erros de compilação.
* [x] Sem erros de lint.