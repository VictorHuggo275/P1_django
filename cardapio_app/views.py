from decimal import Decimal
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ItemForm, MesaForm, PratoForm
from .models import Comanda, Combo, Item, Mesa, Prato


def inicio(request):
    return render(request, "cardapio_app/inicio.html", {
        "mesas": Mesa.objects.filter(ativa=True).order_by("numero"),
        "pratos": Prato.objects.filter(disponivel=True).order_by("nome"),
        "combos": Combo.objects.filter(disponivel=True).order_by("nome"),
    })


def pratos(request):
    return render(request, "cardapio_app/pratos.html", {"pratos": Prato.objects.all()})


def novo_prato(request):
    form = PratoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prato cadastrado.")
        return redirect("pratos")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Novo prato"})


def combos(request):
    return render(request, "cardapio_app/combos.html", {"combos": Combo.objects.prefetch_related("pratos")})


def mesas(request):
    mesas = Mesa.objects.all().order_by("numero")
    return render(request, "cardapio_app/mesas.html", {"mesas": mesas})


def nova_mesa(request):
    form = MesaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("mesas")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Nova mesa"})


def abrir_comanda(request, mesa_id):
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
        if item.prato and item.combo:
            form.add_error(None, "Escolha prato ou combo, não os dois.")
        elif not item.prato and not item.combo:
            form.add_error(None, "Escolha um prato ou um combo.")
        else:
            item.preco_unitario = item.prato.preco if item.prato else item.combo.preco
            item.save()
            return redirect("detalhe_comanda", comanda_id=comanda.id)
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Adicionar item"})


# TODO (próxima etapa): implementar fechar_comanda — calcular o total,
# marcar a comanda como FECHADA e registrar fechada_em.
