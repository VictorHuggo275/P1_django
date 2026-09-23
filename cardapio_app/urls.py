from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("pratos/", views.pratos, name="pratos"),
    path("pratos/novo/", views.novo_prato, name="novo_prato"),
    path("combos/", views.combos, name="combos"),
    path("combos/novo/", views.novo_combo, name="novo_combo"),
    path("mesas/", views.mesas, name="mesas"),
    path("mesas/nova/", views.nova_mesa, name="nova_mesa"),
    path("mesas/<int:mesa_id>/comanda/abrir/", views.abrir_comanda, name="abrir_comanda"),
    path("comandas/<int:comanda_id>/", views.detalhe_comanda, name="detalhe_comanda"),
    path("comandas/<int:comanda_id>/item/novo/", views.novo_item, name="novo_item"),
    path("comandas/<int:comanda_id>/fechar/", views.fechar_comanda, name="fechar_comanda"),
]
