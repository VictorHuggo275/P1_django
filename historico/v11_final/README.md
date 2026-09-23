# Cardápio Digital - P1

Sistema em Django para cardápio digital com comanda por mesa e fechamento de conta.

## Entidades
- Prato
- Combo
- Mesa
- Comanda
- Item

## P1
O foco é abrir uma comanda vinculada a uma mesa, adicionar pratos/combos como itens, visualizar subtotais e fechar a conta calculando e registrando o total.

## Executar
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

O banco utilizado é o SQLite padrão do Django.

O projeto segue o fluxo apresentado nas aulas: Model → migração → URL → View → Template, com ModelForms para entrada de dados.
