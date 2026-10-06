# 🦅 IcarusBot

[![Versão](https://img.shields.io/badge/vers%C3%A3o-%20v2.0-orange.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4.svg?logo=telegram&logoColor=white)](https://core.telegram.org/bots)

Bot assíncrono para Telegram desenvolvido em Python, com uma interface interativa para consultar informações em tempo real, organizar tarefas e conversar com um modelo de inteligência artificial. Esta é a versão **v2.0**, um release principal do projeto.

## Funcionalidades

- **Consulta de clima por cidade:** o usuário escolhe a opção de clima no menu e informa uma cidade. O bot mantém um estado temporário (`awaiting_city`) para concluir o fluxo interativo.
- **Painel de cotações expandido:** o antigo módulo de dólar foi atualizado para o `money.py`, um painel financeiro completo que exibe Dólar (USD), Euro (EUR) e Bitcoin (BTC) em uma única consulta otimizada à [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas), com valores de compra, venda, máxima e mínima.
- **Notícias em tempo real:** utiliza [Playwright](https://playwright.dev/) com Chromium em modo headless para acessar o [G1](https://g1.globo.com/), coletar as cinco primeiras manchetes e retornar os respectivos links.
- **Bate-papo inteligente:** integra a API do Google Gemini por meio do Google GenAI SDK, mantendo uma sessão de chat por usuário. Falhas HTTP 503 são tratadas com novas tentativas e espera progressiva (*retry/backoff*).
- **Processamento de mensagens de voz:** interpreta áudios por meio da API multimodal do Google Gemini, usando a mesma sessão de chat e o mesmo contexto do usuário.
- **Gestor de tarefas (To-Do List):** organiza tarefas por `chat_id`, permitindo adicionar, alternar entre concluída e pendente e remover tarefas, com persistência local em JSON.
- **Menu interativo reformulado:** oferece navegação aprimorada com botões inline, navegação por estados e o botão **Voltar ao Menu** para facilitar o uso.
- **Persistência relacional com SQLite:** cadastra e gerencia perfis em `src/database/users.db`, usando o `chat_id` como chave primária.
- **Gerenciamento de perfil:** permite consultar e personalizar os dados do usuário com `/perfil`, `/setcidade`, `/setmoeda` e `/settelefone`.
- **Personalização dinâmica da IA:** o Gemini recebe as preferências persistidas do usuário (nome, cidade padrão e moeda) nas instruções do sistema, mantendo as respostas contextualizadas sem reapresentação.
- **Arquitetura modular:** os handlers foram separados por domínio em `src/handlers/` e são registrados centralmente por `__init__.py`.
- **Alertas e triggers:** um worker assíncrono envia diariamente o resumo matinal de clima e finanças; o envio pode ser validado manualmente com `/teste_alerta`.

## Changelog v2.0 🚀

- **Persistência relacional com SQLite:** cadastro e gestão de perfis de usuário em `users.db`, com `chat_id` como chave primária.
- **Gerenciamento de perfil:** novos comandos `/perfil`, `/setcidade`, `/setmoeda` e `/settelefone`.
- **Personalização dinâmica da IA:** as preferências salvas são incorporadas às *System Instructions* do Gemini.
- **Arquitetura modular:** handlers de comandos, menu, tarefas e IA separados em `src/handlers/`.
- **Sistema de alertas:** agendador em segundo plano em `src/services/triggers.py`, com resumo diário de clima e finanças e comando `/teste_alerta`.

## Tecnologias utilizadas

| Tecnologia | Uso |
| --- | --- |
| **Python 3** | Linguagem principal e execução assíncrona |
| **pyTelegramBotAPI (`AsyncTeleBot`)** | Integração com a API do Telegram |
| **Playwright** | Automação do Chromium e scraping das notícias do G1 |
| **Google GenAI SDK (Gemini API)** | Conversas multimodais com o Gemini (texto e áudio), mantendo sessões por usuário |
| **python-dotenv** | Carregamento das variáveis do arquivo `.env` |
| **requests** | Requisições HTTP para serviços externos, como a AwesomeAPI |
| **PyOWM** | Consulta dos dados meteorológicos |
| **SQLite** | Persistência relacional dos perfis de usuário por `chat_id` |
| **JSON local** | Persistência da To-Do List por `chat_id` |

As versões exatas das dependências estão registradas em [`requirements.txt`](./requirements.txt).

## Estrutura do projeto

Na v2.0, o registro dos handlers é centralizado em [`src/handlers/__init__.py`](./src/handlers/__init__.py), enquanto os teclados, serviços e dados persistidos estão organizados em seus respectivos módulos.

```text
.
├── main.py                         # Inicialização do bot e do worker de alertas
├── requirements.txt                # Dependências Python fixadas
├── .env.example                    # Modelo de configuração local
├── .gitignore
└── src/
    ├── __init__.py
    ├── database/
    │   ├── users.db                # Perfis de usuário persistidos no SQLite
    │   └── todo.json               # Persistência local das tarefas por chat_id
    ├── handlers/
    │   ├── __init__.py             # Registro central dos handlers
    │   ├── ai_handler.py           # Mensagens de texto e voz para o Gemini
    │   ├── command_handler.py      # Comandos, perfis e alertas de teste
    │   ├── menu_handler.py         # Menu interativo e consulta de clima
    │   └── todo_handler.py         # Comandos e callbacks da To-Do List
    ├── keyboards/
    │   ├── __init__.py
    │   └── menu.py                 # Menus inline e botões de navegação
    └── services/
        ├── __init__.py
        ├── db.py                   # Cadastro e consulta de perfis no SQLite
        ├── gemini.py               # Sessão Gemini e retry para erros 503
        ├── money.py                # Painel USD, EUR e BTC via AwesomeAPI
        ├── news.py                 # Scraping assíncrono do G1 com Playwright
        ├── todo.py                 # Operações da To-Do List em JSON
        ├── triggers.py             # Agendador e resumo matinal diário
        └── weather.py              # Consulta meteorológica por cidade
```

## Pré-requisitos

- Python 3 instalado (recomenda-se Python 3.10 ou superior).
- Um bot criado no [BotFather](https://t.me/BotFather), com o respectivo token.
- Uma chave de API do [Google AI Studio](https://aistudio.google.com/app/apikey) para usar o Gemini.
- Conexão com a internet para acessar o Telegram, a AwesomeAPI, o G1 e a API do Gemini.

## Instalação e execução

### 1. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd bot-telegram
```

### 2. Crie e ative um ambiente virtual

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Windows usando `cmd`:

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o navegador do Playwright

O scraping de notícias depende do Chromium em modo headless:

```bash
playwright install chromium
```

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo para `.env`:

```powershell
Copy-Item .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Edite o `.env` e preencha os valores reais:

```dotenv
TELEGRAM_BOT_TOKEN=seu_token_do_botfather
GEMINI_API_KEY=sua_chave_da_api_do_google
```

> **Importante:** nunca versione nem compartilhe o arquivo `.env`. As credenciais devem permanecer somente no ambiente local ou no gerenciador de secrets da plataforma de hospedagem.

### 6. Execute o bot

Com o ambiente virtual ativado:

```bash
python main.py
```

Abra a conversa com o bot no Telegram e use `/start` ou `/help`. Em seguida, use `/menu` para acessar clima, painel de cotações e notícias. Mensagens de texto ou voz que não estiverem em um fluxo interativo são encaminhadas ao Gemini.

## Comandos disponíveis

| Comando | Descrição |
| --- | --- |
| `/start` | Apresenta o bot |
| `/help` | Exibe a mensagem de ajuda |
| `/menu` | Abre o menu de funcionalidades |
| `/perfil` | Exibe os dados do perfil persistido |
| `/setcidade <cidade>` | Define a cidade padrão do usuário |
| `/setmoeda <código>` | Define a moeda preferida (por exemplo, `BRL` ou `USD`) |
| `/settelefone <número>` | Salva ou atualiza o telefone do usuário |
| `/teste_alerta` | Envia imediatamente um resumo matinal de teste |
| `/task <descrição>` ou `/tarefa <descrição>` | Adiciona uma tarefa ao chat |
| `/tasks` ou `/tarefas` | Exibe a lista interativa de tarefas |

## Variáveis de ambiente

O arquivo [`.env.example`](./.env.example) contém a estrutura mínima necessária:

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Sim | Token do bot obtido no BotFather |
| `GEMINI_API_KEY` | Sim | Chave para autenticação na Gemini API |

Não coloque chaves, tokens ou outros segredos diretamente no código-fonte. O arquivo `.env` já está ignorado pelo Git.

## Observações da v2.0

- A disponibilidade e o formato das notícias dependem do HTML atual do G1 e podem exigir ajustes caso o site mude seus seletores.
- As cotações, as notícias e a interpretação de áudios dependem de serviços externos e podem sofrer indisponibilidade ou limitação temporária.
- As sessões ativas do Gemini e os estados dos menus são mantidos em memória; reiniciar o processo encerra essas sessões, mas não remove os perfis do SQLite.
- O cadastro de perfil é criado automaticamente no primeiro uso de `/start` e fica persistido em `src/database/users.db`.
- As tarefas são persistidas localmente em `src/database/todo.json` e permanecem associadas ao `chat_id`.
- O resumo matinal é disparado pelo worker em segundo plano às 08:00, no horário local da máquina que executa o bot.
- O bot utiliza `polling`, portanto o processo precisa permanecer em execução para receber atualizações.

## Próximos passos

- [X] **Handlers** Separar os handlers por domínio em `src/handlers/`.
- [ ] **Testes Automatizados** Adicionar testes automatizados para os serviços.
- [X] **Perfis de usuário** Persistir preferências e dados de cadastro em SQLite.
- [ ] **Loggin** Adicionar observabilidade, logging estruturado e uma estratégia de deploy.
- [X] **Sistema de Cadastro e Autenticação:** Persistência e gestão de perfis de utilizadores para personalizar a experiência.
- [X] **Sistema de Alertas e Monitorização (Triggers):** Resumo matinal diário com clima e finanças, além do comando `/teste_alerta`.
- [x] **Gestor de Tarefas (To-Do List por `chat_id`):** Organização de tarefas individuais vinculadas ao ID de cada chat no Telegram.
- [ ] **Contentorização com Docker:** Criação do `Dockerfile` e `docker-compose.yml` para simplificar a implantação e padronizar o ambiente de execução.
- [ ] **Deploy em VPS Linux com Webhooks & API:** Substituição do modo *polling* por uma arquitetura assíncrona orientada a eventos, configurando *Webhooks* no Telegram integrados a um backend em **Flask** ou **FastAPI**.
- [ ] **Expansão de Ferramentas da IA:** Utilização de *Function Calling* no Gemini para permitir que o bot execute comandos do sistema e consultas em APIs externas de forma autónoma.

## Licença

MIT License
