# 🦅 IcarusBot

[![Versão](https://img.shields.io/badge/vers%C3%A3o-%20v1.5-orange.svg)](https://github.com/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4.svg?logo=telegram&logoColor=white)](https://core.telegram.org/bots)

Bot assíncrono para Telegram desenvolvido em Python, com uma interface interativa para consultar informações em tempo real, organizar tarefas e conversar com um modelo de inteligência artificial. Esta é a versão **v1.5** do projeto.

## Funcionalidades

- **Consulta de clima por cidade:** o usuário escolhe a opção de clima no menu e informa uma cidade. O bot mantém um estado temporário (`awaiting_city`) para concluir o fluxo interativo.
- **Painel de cotações expandido:** o antigo módulo de dólar foi atualizado para o `money.py`, um painel financeiro completo que exibe Dólar (USD), Euro (EUR) e Bitcoin (BTC) em uma única consulta otimizada à [AwesomeAPI](https://docs.awesomeapi.com.br/api-de-moedas), com valores de compra, venda, máxima e mínima.
- **Notícias em tempo real:** utiliza [Playwright](https://playwright.dev/) com Chromium em modo headless para acessar o [G1](https://g1.globo.com/), coletar as cinco primeiras manchetes e retornar os respectivos links.
- **Bate-papo inteligente:** integra a API do Google Gemini por meio do Google GenAI SDK, mantendo uma sessão de chat por usuário. Falhas HTTP 503 são tratadas com novas tentativas e espera progressiva (*retry/backoff*).
- **Processamento de mensagens de voz:** interpreta áudios por meio da API multimodal do Google Gemini, usando a mesma sessão de chat e o mesmo contexto do usuário.
- **Gestor de tarefas (To-Do List):** organiza tarefas por `chat_id`, permitindo adicionar, alternar entre concluída e pendente e remover tarefas, com persistência local em JSON.
- **Menu interativo reformulado:** oferece navegação aprimorada com botões inline, navegação por estados e o botão **Voltar ao Menu** para facilitar o uso.

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
| **JSON local** | Persistência da To-Do List por `chat_id` |

As versões exatas das dependências estão registradas em [`requirements.txt`](./requirements.txt).

## Estrutura do projeto

Na v1.5, os handlers do Telegram permanecem centralizados em [`main.py`](./main.py), enquanto os teclados e serviços estão organizados em seus respectivos módulos.

```text
.
├── main.py                         # Inicialização do bot, comandos e handlers
├── requirements.txt                # Dependências Python fixadas
├── .env.example                    # Modelo de configuração local
├── .gitignore
└── src/
    ├── __init__.py
    ├── database/
    │   └── todo.json               # Persistência local das tarefas por chat_id
    ├── keyboards/
    │   ├── __init__.py
    │   └── menu.py                 # Menus inline e botões de navegação
    └── services/
        ├── __init__.py
        ├── gemini.py               # Sessão Gemini e retry para erros 503
        ├── money.py                # Painel USD, EUR e BTC via AwesomeAPI
        ├── news.py                 # Scraping assíncrono do G1 com Playwright
        ├── todo.py                 # Operações da To-Do List em JSON
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
| `/task <descrição>` ou `/tarefa <descrição>` | Adiciona uma tarefa ao chat |
| `/tasks` ou `/tarefas` | Exibe a lista interativa de tarefas |

## Variáveis de ambiente

O arquivo [`.env.example`](./.env.example) contém a estrutura mínima necessária:

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Sim | Token do bot obtido no BotFather |
| `GEMINI_API_KEY` | Sim | Chave para autenticação na Gemini API |

Não coloque chaves, tokens ou outros segredos diretamente no código-fonte. O arquivo `.env` já está ignorado pelo Git.

## Observações da v1.5

- A disponibilidade e o formato das notícias dependem do HTML atual do G1 e podem exigir ajustes caso o site mude seus seletores.
- As cotações, as notícias e a interpretação de áudios dependem de serviços externos e podem sofrer indisponibilidade ou limitação temporária.
- O estado e as sessões de chat são mantidos em memória; reiniciar o processo remove esses dados.
- As tarefas são persistidas localmente em `src/database/todo.json` e permanecem associadas ao `chat_id`.
- O bot utiliza `polling`, portanto o processo precisa permanecer em execução para receber atualizações.

## Próximos passos

- [ ] **Handlers** Separar os handlers por domínio em `src/handlers/`.
- [ ] **Testes Automatizados** Adicionar testes automatizados para os serviços.
- [ ] **Sessões** Persistir estados e sessões quando necessário.
- [ ] **Loggin** Adicionar observabilidade, logging estruturado e uma estratégia de deploy.
- [ ] **Sistema de Cadastro e Autenticação:** Persistência e gestão de perfis de utilizadores para personalizar a experiência.
- [ ] **Sistema de Alertas e Monitorização (Triggers):** Notificações automáticas para avisar o utilizador quando ocorrerem eventos específicos no banco de dados ou em serviços de rede.
- [x] **Gestor de Tarefas (To-Do List por `chat_id`):** Organização de tarefas individuais vinculadas ao ID de cada chat no Telegram.
- [ ] **Contentorização com Docker:** Criação do `Dockerfile` e `docker-compose.yml` para simplificar a implantação e padronizar o ambiente de execução.
- [ ] **Deploy em VPS Linux com Webhooks & API:** Substituição do modo *polling* por uma arquitetura assíncrona orientada a eventos, configurando *Webhooks* no Telegram integrados a um backend em **Flask** ou **FastAPI**.
- [ ] **Expansão de Ferramentas da IA:** Utilização de *Function Calling* no Gemini para permitir que o bot execute comandos do sistema e consultas em APIs externas de forma autónoma.

## Licença

MIT License
