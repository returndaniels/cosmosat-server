## Estrutura de Pastas e Nomeação de Arquivos:

```
├── api
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── app
│   ├── __init__.py
│   └── main.py
├── db
│   └── __init__.py
├── templates
│   └── index.html
├── static
│   └── style.css
└── venv
    └── ... (bibliotecas Python)
```

**Explicação:**

- `api`: Contém os arquivos Python que definem a API RESTful e o streamer de dados.
- `app`: Contém os arquivos Python que configuram o FastAPI e servem a página web.
- `db`: Comtém os arquivos de configuração do banco de dados.
- `templates`: Comtém arquivos de páginas html.
- `static`: Contém arquivos estáticos como CSS.
- `venv`: Ambiente virtual Python com as bibliotecas necessárias.

**Nomeação de Arquivos:**

- `__init__.py`: Arquivos de inicialização para cada pacote.
- `crud.py`: Implementa operações CRUD (Create, Read, Update, Delete) no banco de dados.
- `database.py`: Define a conexão com o banco de dados SQLite.
- `main.py`: Ponto de entrada do servidor, configura o FastAPI e inicia a detecção de raios.
- `models.py`: Define os modelos de dados para raios e registros de detecção.
- `routes.py`: Define as rotas da API RESTful e do streamer de dados.
- `index.html`: Página web com interface para o usuário.
- `style.css`: Arquivo CSS para estilizar a página web.

## Implementação Detalhada:

**1. Detecção de Raios:**

- Um script Python externo é responsável por detectar raios e enviar dados para o servidor.
- O servidor inicia a detecção de raios através de uma mensagem.
- A câmera do Raspberry Pi Zero é ativada antes da detecção, se necessário.
- Cada detecção gera um registro no banco de dados com data e hora.
- Os dados dos raios detectados são associados ao registro e enviados ao cliente via websockets.

**2. API RESTful:**

- A API RESTful permite:
  - Recuperar todos os registros de detecção.
  - Recuperar um registro específico por ID.
  - Apagar um registro específico por ID.

**3. Streamer de Dados:**

- O streamer de dados usa websockets para enviar dados dos raios detectados em tempo real para o cliente.
- O cliente pode se conectar ao streamer e receber atualizações sobre cada nova detecção.

**4. Página Web:**

- A página web exibe:
  - Lista de registros de detecção anteriores.
  - Botão para iniciar a detecção de raios.
  - Botão para parar a detecção de raios.
  - Status da câmera (ativada/desativada).
  - Botão para ativar/desativar a câmera.
  - Monitor com dados da detecção atual, se houver.
- Ao clicar em um registro de detecção, o cliente pode visualizar as informações dos raios detectados.

**5. Considerações Adicionais:**

- Utiliza bibliotecas Python como `sqlite3`, `FastAPI`, `uvicorn` e `websockets` para implementar o servidor.
- Previsão de implementação de autenticação e autorização para proteger a API e o streamer de dados.
- Os dados de detecção são armazenados em um banco de dados SQLite.

## Criando e ativando o ambiente virtual Python (venv):

**Garanta que as dependências GTK estejam instaladas**

```bash
sudo apt install libgtk-3-dev
export DISPLAY=:0
```

**Passo 1:** Instalar o módulo venv (se ainda não estiver instalado):

```bash
python -m pip install venv
```

**Passo 2:** Criar o ambiente virtual:

```bash
python -m venv venv
```

**Passo 3:** Ativar o ambiente virtual:

- **Linux/macOS:**

```bash
source venv/bin/activate
```

- **Windows:**

```bash
source venv\Scripts\activate
```

**Verificação:**

Após ativar o ambiente virtual, o nome do ambiente deve aparecer entre parênteses no prompt do seu terminal.

## Instalando as bibliotecas do requirements.txt:

**Passo 4:** Instalar as bibliotecas:

```bash
pip install -r requirements.txt
```

**Verificação:**

Após a instalação, você pode verificar se as bibliotecas foram instaladas corretamente usando o comando:

```bash
pip list
```

## Executar aplicação

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Caso o processo não encerre corretamente

```bash
sudo lsof -ti tcp:8000 | xargs kill -9
```

## Como fazer stream de video

```bash
sudo apt update
sudo apt upgrade
sudo apt install subversion libjpeg8-dev imagemagick libav-tools cmake
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
make
make install
```

Se não houver candidato para a biblioteca `libjpeg8-dev`, ela pode ser subistituido por `libjpeg62-turbo-dev`

## Recursos Adicionais:

- Documentação do FastAPI: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- Documentação do SQLite: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- Tutoriais sobre websockets: [https://www.websocket.org/](https://www.websocket.org/)
