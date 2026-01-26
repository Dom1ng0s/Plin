# Plin 💸

> **"Registrou, Plin. Controlou."**

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQL](https://img.shields.io/badge/Database-SQL-lightgrey)

O **Plin** é um Chatbot de Gestão Financeira desenvolvido para reduzir a fricção no registro de despesas pessoais. Integrado ao Telegram, ele permite o controle financeiro através de linguagem natural, sem a necessidade de planilhas complexas ou aplicativos pesados.

---

## 📋 Funcionalidades

- [X] **Registro Rápido:** Adição de gastos e receitas via chat.
- [ ] **Categorização:** Organização automática por tipo de despesa.
- [X] **Persistência de Dados:** Histórico salvo em banco de dados relacional (SQL).
- [ ] **Relatórios:** Visualização de saldo e extrato mensal.
- [ ] **Visualização de Dados:** Gráficos gerados automaticamente (Matplotlib).


---

### 🚀 Como Executar o Projeto

O **Plin** já está totalmente containerizado, o que facilita o deploy e a execução em qualquer ambiente.

#### 1. Pré-requisitos

* Ter o **Docker** e o **Docker Compose** instalados.
* Um **Token de Bot** do Telegram (obtido através do @BotFather).

#### 2. Configuração das Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto e adicione o seu token:

```env
TELEGRAM_TOKEN=seu_token_aqui

```

#### 3. Execução com Docker

Para subir o bot, basta rodar o comando:

```bash
docker-compose up -d

```

Isso criará um container chamado `plin_bot`, instalará todas as dependências necessárias e iniciará o serviço automaticamente.

---

### 🛠️ Estrutura Técnica

O projeto foi construído focando em modularidade e boas práticas de persistência:

* **Persistência de Dados:** Utiliza **SQLAlchemy** (ORM) para mapear a tabela de transações, garantindo que os dados persistam em um arquivo `plin.db` mesmo após o reinício dos containers.
* **Lógica de Negócio (CRUD):** As operações de criação, leitura e exclusão são isoladas em um módulo específico, permitindo que a interface do Telegram apenas consuma os resultados.
* **Gestão de Identidade:** O bot gerencia um `id_transacao_user` manual por usuário, permitindo que cada pessoa tenha sua própria sequência numérica para apagar registros, sem expor as chaves primárias globais do banco.



## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para contribuir!

---

Desenvolvido por [Dom1ng0s](https://www.google.com/search?q=https://github.com/Dom1ng0s)


