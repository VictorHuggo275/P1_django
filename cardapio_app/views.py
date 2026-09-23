from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import MesaForm, PratoForm
from .models import Combo, Mesa, Prato


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


# TODO (próxima etapa): abrir/fechar comanda e adicionar itens (vem em
# v10_comanda_sem_fechamento).
