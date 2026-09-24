from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("pratos/", views.pratos, name="pratos"),
    path("pratos/novo/", views.novo_prato, name="novo_prato"),
    path("pratos/<int:prato_id>/editar/", views.editar_prato, name="editar_prato"),
    path("pratos/<int:prato_id>/excluir/", views.excluir_prato, name="excluir_prato"),
    path("combos/", views.combos, name="combos"),
    path("combos/novo/", views.novo_combo, name="novo_combo"),
    path("combos/<int:combo_id>/editar/", views.editar_combo, name="editar_combo"),
    path("combos/<int:combo_id>/excluir/", views.excluir_combo, name="excluir_combo"),
    path("categorias/", views.categorias, name="categorias"),
    path("categorias/nova/", views.nova_categoria, name="nova_categoria"),
    path("mesas/", views.mesas, name="mesas"),
    path("mesas/nova/", views.nova_mesa, name="nova_mesa"),
    path("mesas/<int:mesa_id>/editar/", views.editar_mesa, name="editar_mesa"),
    path("mesas/<int:mesa_id>/excluir/", views.excluir_mesa, name="excluir_mesa"),
    path("mesas/<int:mesa_id>/comanda/abrir/", views.abrir_comanda, name="abrir_comanda"),
    path("comandas/<int:comanda_id>/", views.detalhe_comanda, name="detalhe_comanda"),
    path("comandas/<int:comanda_id>/item/novo/", views.novo_item, name="novo_item"),
    path("comandas/<int:comanda_id>/fechar/", views.fechar_comanda, name="fechar_comanda"),
]
