# Cardápio Digital

## Como executar o projeto

### 1. Abrir o terminal na pasta do projeto

Abra o terminal do VS Code e entre na pasta do projeto:

```bash
cd CardapioDigital_P1
```

### 2. Criar a máquina virtual

Crie uma máquina virtual Python para o projeto:

```bash
python -m venv venv
```

### 3. Ativar a máquina virtual

No Windows, utilizando o CMD:

```cmd
venv\Scripts\activate
```

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Quando a máquina virtual estiver ativada, aparecerá `(venv)` no início do terminal.

### 4. Instalar as dependências

Com a `venv` ativada, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 5. Criar o banco de dados

Execute as migrações do Django:

```bash
python manage.py migrate
```

### 6. Criar um usuário administrador

Para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Preencha o nome de usuário, e-mail e senha solicitados.

### 7. Iniciar o servidor

Execute:

```bash
python manage.py runserver
```

O projeto estará disponível em:

```text
http://127.0.0.1:8000/
```

Para acessar o painel administrativo:

```text
http://127.0.0.1:8000/admin/
```

---

## Sobre o projeto

O **Cardápio Digital** é um sistema web desenvolvido com Django para gerenciamento de um restaurante.

O sistema permite:

* Visualizar pratos disponíveis;
* Cadastrar pratos;
* Cadastrar combos;
* Visualizar combos;
* Cadastrar mesas;
* Abrir comandas;
* Adicionar pratos ou combos às comandas;
* Definir a quantidade dos itens;
* Calcular subtotais;
* Fechar comandas;
* Registrar o valor total da comanda.

## Tecnologias utilizadas

* Python
* Django 5
* SQLite
* HTML
* CSS
* Django Templates

## Estrutura do projeto

```text
CardapioDigital_P1/
│
├── cardapio/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── cardapio_app/
│   ├── migrations/
│   ├── static/
│   │   └── cardapio_app/
│   │       └── style.css
│   │
│   ├── templates/
│   │   └── cardapio_app/
│   │       ├── base.html
│   │       ├── inicio.html
│   │       ├── pratos.html
│   │       ├── combos.html
│   │       ├── combo_form.html
│   │       ├── mesas.html
│   │       ├── comanda.html
│   │       └── form.html
│   │
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
└── README.md
```

## Modelos

### Prato

Representa os itens individuais do cardápio.

Possui:

* Nome;
* Descrição;
* Preço;
* Disponibilidade.

### Combo

Representa um conjunto de pratos.

Possui:

* Nome;
* Descrição;
* Preço;
* Disponibilidade;
* Lista de pratos que fazem parte do combo.

Um combo precisa possuir pelo menos dois pratos.

### Mesa

Representa as mesas do restaurante.

Possui:

* Número;
* Capacidade;
* Status de atividade.

### Comanda

Representa uma conta aberta para uma mesa.

Possui:

* Mesa relacionada;
* Status da comanda;
* Data de abertura;
* Data de fechamento;
* Valor total.

Uma comanda pode estar aberta ou fechada.

### Item

Representa um produto adicionado a uma comanda.

Pode ser:

* Um prato; ou
* Um combo.

Também possui:

* Quantidade;
* Preço unitário;
* Subtotal.

O sistema impede que um item seja simultaneamente um prato e um combo.

## Funcionamento

O fluxo principal do sistema é:

```text
Mesa
  ↓
Abrir comanda
  ↓
Adicionar prato ou combo
  ↓
Definir quantidade
  ↓
Calcular subtotal
  ↓
Fechar comanda
  ↓
Registrar valor total
```

Ao adicionar um item, o preço utilizado é obtido automaticamente a partir do prato ou combo selecionado.

Ao fechar uma comanda, o sistema soma os subtotais de todos os itens e registra o resultado como o total da conta.

## Validações

O sistema possui validações para:

* Impedir preços menores ou iguais a zero;
* Exigir pelo menos dois pratos em um combo;
* Impedir quantidade menor que 1;
* Exigir que um item possua um prato ou um combo;
* Impedir que um item possua prato e combo ao mesmo tempo;
* Permitir somente pratos e combos disponíveis em uma comanda.

## Banco de dados

O projeto utiliza **SQLite** durante o desenvolvimento.

O banco de dados é criado após executar:

```bash
python manage.py migrate
```

O arquivo gerado é:

```text
db.sqlite3
```

## Comandos úteis

### Ativar a venv

```bash
venv\Scripts\activate
```

### Criar migrações

```bash
python manage.py makemigrations
```

### Aplicar migrações

```bash
python manage.py migrate
```

### Criar administrador

```bash
python manage.py createsuperuser
```

### Iniciar o servidor

```bash
python manage.py runserver
```

### Desativar a venv

Quando terminar de utilizar o projeto:

```bash
deactivate
```

## Objetivo

O projeto foi desenvolvido como uma aplicação prática de gerenciamento de restaurante, utilizando conceitos de desenvolvimento web, banco de dados, modelos, formulários, validações e operações CRUD com Django.
