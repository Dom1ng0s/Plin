# Plin 💸

> **"Registrou, Plin. Controlou."**

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![SQL](https://img.shields.io/badge/Database-SQL-lightgrey)

O **Plin** é um Chatbot de Gestão Financeira desenvolvido para reduzir a fricção no registro de despesas pessoais. Integrado ao Telegram, ele permite o controle financeiro através de linguagem natural, sem a necessidade de planilhas complexas ou aplicativos pesados.

---

## 📋 Funcionalidades

- [ ] **Registro Rápido:** Adição de gastos e receitas via chat.
- [ ] **Categorização:** Organização automática por tipo de despesa.
- [ ] **Persistência de Dados:** Histórico salvo em banco de dados relacional (SQL).
- [ ] **Relatórios:** Visualização de saldo e extrato mensal.
- [ ] **Visualização de Dados:** Gráficos gerados automaticamente (Matplotlib).

## 🛠️ Tech Stack

Este projeto foi construído focando em boas práticas de Engenharia de Software e arquitetura limpa.

- **Linguagem:** Python
- **Bot Framework:** `python-telegram-bot`
- **Banco de Dados:** SQLite (Dev) / PostgreSQL (Prod)
- **ORM:** SQLAlchemy
- **Gerenciamento de Dependências:** Pip / Virtualenv

## 📂 Estrutura do Projeto

A arquitetura foi pensada para ser modular e escalável:

```text
plin-bot/
├── src/
│   ├── database/    # Camada de Persistência (Conexão e Models)
│   ├── handlers/    # Lógica de interação com o usuário (Comandos)
│   └── utils/       # Funções auxiliares e geradores de gráficos
├── main.py          # Ponto de entrada da aplicação
└── requirements.txt # Dependências

```

## 🚀 Como Rodar o Projeto

### Pré-requisitos

* Python 3.10 ou superior
* Conta no Telegram (para criar o bot via @BotFather)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone [https://github.com/Dom1ng0s/Plin.git](https://github.com/Dom1ng0s/Plin.git)
cd Plin

```


2. **Crie e ative o ambiente virtual**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

```


3. **Instale as dependências**
```bash
pip install -r requirements.txt

```


4. **Configure as Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto e adicione seu token:
```env
TELEGRAM_TOKEN=seu_token_aqui
DB_NAME=plin.db

```


5. **Execute o Bot**
```bash
python main.py

```



---

## 📝 Licença

Este projeto está sob a licença MIT. Sinta-se livre para contribuir!

---

Desenvolvido por [Domingos](https://www.google.com/search?q=https://github.com/Dom1ng0s)

```

