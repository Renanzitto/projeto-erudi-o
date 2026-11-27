# Erudição — Projeto Educacional

Plataforma para estudantes pesquisarem **temas de redação do Enem** e encontrarem
**repertórios socioculturais verificados** (leis, dados oficiais, obras e conceitos),
com indicação de como usar cada um na redação e links para as fontes originais.

Colaboradores cadastrados podem sugerir novos repertórios, que passam pela
aprovação de um administrador antes de serem publicados.

## Tecnologias

- **Frontend:** HTML, CSS e JavaScript puro (pasta `frontend/`)
- **Backend:** Python + Flask (pasta `backend/`)
- **Banco de dados:** MySQL

## Como rodar no seu computador

### 1. Pré-requisitos
- Python 3.10 ou mais novo
- MySQL 8

### 2. Banco de dados
Crie o banco executando o script `erudicao_banco.sql` no MySQL
(pelo MySQL Workbench ou pelo terminal).

### 3. Configuração
Crie um arquivo `.env` na raiz do projeto com os dados do seu MySQL:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_do_mysql
DB_NAME=Erudicao
SECRET_KEY=uma_frase_secreta_qualquer
```

> O `.env` não vai para o GitHub (está no `.gitignore`), porque contém senhas.

### 4. Instalar as dependências
Na raiz do projeto:

```
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 5. Criar o administrador e popular os repertórios
Dentro da pasta `backend/`:

```
python criar_admin.py
python seed_repertorios.py
```

### 6. Rodar
Dentro da pasta `backend/`:

```
python app.py
```

Abra **http://127.0.0.1:5000** no navegador. O Flask entrega tanto as páginas
quanto a API.

## Compartilhar com outras pessoas (link temporário)

Com o backend rodando, em outro terminal:

```
cloudflared tunnel --url http://127.0.0.1:5000
```

O terminal mostra um link `https://....trycloudflare.com` que funciona enquanto
o terminal estiver aberto.

## Estrutura

```
backend/
  app.py                 API (temas, login, cadastro, contribuições)
  criar_admin.py         cria um usuário administrador
  seed_repertorios.py    insere os repertórios e materiais verificados
frontend/
  loading.html           tela de abertura
  index.html             página inicial com a busca de temas
  tema.html              repertórios e materiais de um tema
  login.html             login e cadastro
  colaborador.html       envio e aprovação de contribuições
erudicao_banco.sql       criação das tabelas e dos temas
```
