from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ComboForm, ItemForm, MesaForm, PratoForm
from .models import Comanda, Combo, Item, Mesa, Prato


def inicio(request):
    return render(request, "cardapio_app/inicio.html", {
        "mesas": Mesa.objects.filter(ativa=True).order_by("numero"),
        "pratos": Prato.objects.filter(disponivel=True).order_by("nome"),
        "combos": Combo.objects.filter(disponivel=True).prefetch_related("pratos").order_by("nome"),
    })


def pratos(request):
    return render(request, "cardapio_app/pratos.html", {"pratos": Prato.objects.all().order_by("nome")})


def novo_prato(request):
    form = PratoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prato cadastrado.")
        return redirect("pratos")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Novo prato"})


def combos(request):
    return render(request, "cardapio_app/combos.html", {
        "combos": Combo.objects.prefetch_related("pratos").order_by("nome"),
    })


def novo_combo(request):
    # Esta view não existia: não havia nenhuma rota nem página para cadastrar um
    # combo, então era literalmente impossível juntar pratos em um combo pela
    # interface (o único jeito seria pelo /admin/).
    form = ComboForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Combo cadastrado.")
        return redirect("combos")
    return render(request, "cardapio_app/combo_form.html", {"form": form, "titulo": "Novo combo"})


def mesas(request):
    mesas = Mesa.objects.all().order_by("numero")
    return render(request, "cardapio_app/mesas.html", {"mesas": mesas})


def nova_mesa(request):
    form = MesaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mesa cadastrada.")
        return redirect("mesas")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Nova mesa"})


@require_POST
def abrir_comanda(request, mesa_id):
    # Criar/abrir uma comanda altera o banco de dados, então essa ação não deveria
    # responder a um GET simples (um link clicado, um crawler ou até o próprio
    # navegador pré-carregando a página podiam disparar a criação sem querer).
    mesa = get_object_or_404(Mesa, pk=mesa_id)
    comanda = Comanda.objects.filter(mesa=mesa, status=Comanda.ABERTA).first()
    if not comanda:
        comanda = Comanda.objects.create(mesa=mesa)
    return redirect("detalhe_comanda", comanda_id=comanda.id)


def detalhe_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda.objects.select_related("mesa"), pk=comanda_id)
    itens = comanda.itens.select_related("prato", "combo")
    total = sum((item.subtotal for item in itens), Decimal("0.00"))
    return render(request, "cardapio_app/comanda.html", {"comanda": comanda, "itens": itens, "total": total})


def novo_item(request, comanda_id):
    comanda = get_object_or_404(Comanda, pk=comanda_id, status=Comanda.ABERTA)
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.comanda = comanda
        item.preco_unitario = item.prato.preco if item.prato else item.combo.preco
        item.save()
        messages.success(request, "Item adicionado à comanda.")
        return redirect("detalhe_comanda", comanda_id=comanda.id)
    return render(request, "cardapio_app/form.html", {
        "form": form,
        "titulo": "Adicionar item",
        "ajuda": "Escolha um prato OU um combo (não os dois) e informe a quantidade.",
    })


@require_POST
@transaction.atomic
def fechar_comanda(request, comanda_id):
    comanda = get_object_or_404(Comanda, pk=comanda_id, status=Comanda.ABERTA)
    itens = list(comanda.itens.all())
    total = sum((item.subtotal for item in itens), Decimal("0.00"))
    comanda.total = total
    comanda.status = Comanda.FECHADA
    comanda.fechada_em = timezone.now()
    comanda.save(update_fields=["total", "status", "fechada_em"])
    messages.success(request, f"Conta fechada: R$ {total:.2f}.")
    return redirect("detalhe_comanda", comanda_id=comanda.id)
