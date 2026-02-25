<div align="center">

# 💸 Plin

**Chatbot de gestão financeira pessoal via Telegram**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Docker](https://img.shields.io/badge/Docker-Containerizado-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> *"Registrou, Plin. Controlou."*
>
> Controle financeiro sem fricção — sem planilha, sem app pesado, sem login. Só você e o Telegram que você já usa todo dia.

</div>

---

## 💡 O Problema que o Plin Resolve

Apps de finanças têm um problema de adoção: a pessoa precisa abrir o app, fazer login, navegar até "nova despesa" e preencher formulários — tudo isso enquanto ainda está na fila do mercado. Resultado: ela não registra na hora e esquece depois.

O Plin elimina toda essa fricção. Como o Telegram já está aberto, registrar um gasto vira uma conversa de 5 segundos:

```
Você:   gastei 45 reais no mercado
Plin:   ✅ Registrado! Alimentação · R$ 45,00
        Saldo do mês: R$ 1.230,00 disponíveis
```

---

## 🤖 Demonstração

| Registro de gasto | Extrato mensal | Gráfico de categorias |
|:---:|:---:|:---:|
| ![registro](images/registro.png) | ![extrato](images/extrato.png) | ![grafico](images/grafico.png) |

---

## ✨ Funcionalidades

**Registro via linguagem natural**
Entende frases como "gastei 50 no uber" ou "recebi 200 de freela" sem precisar de comandos rígidos.

**Categorização automática**
Classifica despesas por categoria (Alimentação, Transporte, Lazer, etc.) com base no contexto da mensagem.

**Histórico persistente**
Todos os dados ficam salvos em banco SQLite via SQLAlchemy ORM — reiniciar o container não apaga nada.

**Relatórios e gráficos**
Extrato mensal com saldo e gráficos de distribuição por categoria gerados com Matplotlib, direto no chat.

**Multi-usuário com isolamento**
Cada usuário tem sua própria sequência de IDs de transação, permitindo apagar registros pelo número ("apaga o gasto 3") sem expor chaves do banco.

---

## 🏗️ Arquitetura

```
Telegram API
     │
     ▼
  main.py                  ← Handler de mensagens (python-telegram-bot)
     │
     ├── crud.py           ← Operações de banco (criar, listar, deletar transações)
     │
     └── database.py       ← Configuração do SQLAlchemy + modelo de Transação
                                  │
                                  ▼
                             plin.db (SQLite)
                        (persistido via volume Docker)
```

**Decisões técnicas relevantes:**

- **SQLAlchemy ORM** em vez de SQL puro — abstração limpa entre lógica de negócio e banco de dados, facilitando migração futura para PostgreSQL.
- **ID de transação por usuário** — cada usuário tem sua própria sequência numérica (`id_transacao_user`), sem expor PKs globais do banco. Permite `apaga o gasto 3` de forma segura em ambiente multi-tenant.
- **Docker Compose** — bot e banco isolados em container, pronto para deploy em qualquer VPS com um comando.

---

## 🛠️ Stack Tecnológica

| Responsabilidade | Tecnologia |
|---|---|
| **Linguagem** | Python 3.10+ |
| **Bot API** | python-telegram-bot |
| **ORM / Banco** | SQLAlchemy + SQLite |
| **Gráficos** | Matplotlib |
| **Containerização** | Docker + Docker Compose |
| **Config** | python-dotenv |

---

## 🚀 Como Rodar

### Pré-requisitos

- Docker e Docker Compose instalados
- Token de bot do Telegram (obtenha pelo [@BotFather](https://t.me/botfather))

### 1. Clone o repositório

```bash
git clone https://github.com/Dom1ng0s/Plin.git
cd Plin
```

### 2. Configure o token

Crie um arquivo `.env` na raiz:

```env
TELEGRAM_TOKEN=seu_token_aqui
```

### 3. Suba o container

```bash
docker-compose up -d
```

Isso vai construir a imagem, instalar as dependências e iniciar o bot automaticamente. O banco de dados é persistido em volume Docker — os dados sobrevivem a reinicializações.

### 4. Pronto! Abra o Telegram e fale com seu bot 🎉

---

## 💬 Comandos Disponíveis

| Comando | Descrição |
|---|---|
| `/start` | Apresentação e boas-vindas |
| `/extrato` | Extrato de transações do mês atual |
| `/saldo` | Saldo disponível (receitas - despesas) |
| `/grafico` | Gráfico de gastos por categoria (Matplotlib) |
| `/apagar [n]` | Remove a transação de número `n` do seu histórico |
| Mensagem livre | Registra gasto ou receita via linguagem natural |

---

## 📁 Estrutura do Projeto

```
Plin/
├── main.py           # Handlers do Telegram e roteamento de mensagens
├── crud.py           # Operações CRUD isoladas (criar, ler, deletar transações)
├── database.py       # Modelo SQLAlchemy e configuração do banco
├── teste.py          # Testes das operações de banco
├── Dockerfile        # Imagem do bot
├── dockercompose.yml # Orquestração do serviço
├── requirements.txt
└── images/           # Screenshots para documentação
```

---

## 🗺️ Próximas Evoluções

- [ ] Parser de linguagem natural mais robusto (NLP com spaCy ou Gemini)
- [ ] Alertas de limite de gastos por categoria
- [ ] Exportação do extrato em PDF ou planilha
- [ ] Deploy automatizado via GitHub Actions em VPS

---

## 👤 Autor

**Davi Domingos de Oliveira**
Estudante de Ciência da Computação — UFAL | Backend Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidomingosdeoliveira/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Dom1ng0s)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:odomingosdavi@gmail.com)
