from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CategoriaForm, ComboForm, ItemForm, MesaForm, PratoForm
from .models import Categoria, Comanda, Combo, Item, Mesa, Prato


def inicio(request):
    return render(request, "cardapio_app/inicio.html", {
        "mesas": Mesa.objects.filter(ativa=True).order_by("numero"),
        "pratos": Prato.objects.filter(disponivel=True).order_by("nome"),
        "combos": Combo.objects.filter(disponivel=True).prefetch_related("pratos").order_by("nome"),
    })


def pratos(request):
    # Feature 1 (busca e filtro na listagem): lê os parâmetros da URL e aplica
    # busca textual pelo nome + filtro por categoria, podendo ser usados juntos
    # ou separadamente. O desafio extra usa Q() para combinar os dois na mesma
    # consulta em vez de encadear dois .filter() (o resultado é equivalente,
    # mas Q() deixa explícito que as condições podem ser combinadas com AND/OR).
    termo = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()

    lista = Prato.objects.all().order_by("nome")
    filtros = Q()
    if termo:
        filtros &= Q(nome__icontains=termo)
    if categoria_id:
        filtros &= Q(categoria_id=categoria_id)
    if filtros:
        lista = lista.filter(filtros)

    return render(request, "cardapio_app/pratos.html", {
        "pratos": lista,
        "categorias": Categoria.objects.all(),
        "categoria_selecionada": categoria_id,
    })


def novo_prato(request):
    form = PratoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prato cadastrado.")
        return redirect("pratos")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Novo prato"})


def editar_prato(request, prato_id):
    prato = get_object_or_404(Prato, pk=prato_id)
    form = PratoForm(request.POST or None, instance=prato)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Prato atualizado.")
        return redirect("pratos")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": f"Editar prato — {prato.nome}"})


@require_POST
def excluir_prato(request, prato_id):
    # Só aceita POST pelo mesmo motivo de abrir_comanda/fechar_comanda: excluir
    # é uma alteração no banco e não pode acontecer por um simples GET.
    prato = get_object_or_404(Prato, pk=prato_id)
    try:
        prato.delete()
        messages.success(request, "Prato excluído.")
    except ProtectedError:
        # O prato já foi usado em algum item de comanda (on_delete=PROTECT),
        # então apagar quebraria o histórico de pedidos. Em vez de deixar o
        # Django estourar um erro 500, avisamos o usuário com uma alternativa.
        messages.error(request, "Não é possível excluir: este prato já foi usado em algum pedido. "
                                 "Marque-o como indisponível em vez de excluir.")
    return redirect("pratos")


def combos(request):
    # Mesma ideia da Feature 1 aplicada à listagem de combos: busca por nome
    # e filtro por categoria, combinados com Q() e usáveis juntos ou separados.
    termo = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()

    lista = Combo.objects.prefetch_related("pratos").order_by("nome")
    filtros = Q()
    if termo:
        filtros &= Q(nome__icontains=termo)
    if categoria_id:
        filtros &= Q(categoria_id=categoria_id)
    if filtros:
        lista = lista.filter(filtros)

    return render(request, "cardapio_app/combos.html", {
        "combos": lista,
        "categorias": Categoria.objects.all(),
        "categoria_selecionada": categoria_id,
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


def editar_combo(request, combo_id):
    combo = get_object_or_404(Combo, pk=combo_id)
    form = ComboForm(request.POST or None, instance=combo)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Combo atualizado.")
        return redirect("combos")
    return render(request, "cardapio_app/combo_form.html", {"form": form, "titulo": f"Editar combo — {combo.nome}"})


@require_POST
def excluir_combo(request, combo_id):
    combo = get_object_or_404(Combo, pk=combo_id)
    try:
        combo.delete()
        messages.success(request, "Combo excluído.")
    except ProtectedError:
        messages.error(request, "Não é possível excluir: este combo já foi usado em algum pedido. "
                                 "Marque-o como indisponível em vez de excluir.")
    return redirect("combos")


def categorias(request):
    return render(request, "cardapio_app/categorias.html", {
        "categorias": Categoria.objects.all(),
    })


def nova_categoria(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Categoria cadastrada.")
        return redirect("categorias")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": "Nova categoria"})


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


def editar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, pk=mesa_id)
    form = MesaForm(request.POST or None, instance=mesa)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mesa atualizada.")
        return redirect("mesas")
    return render(request, "cardapio_app/form.html", {"form": form, "titulo": f"Editar mesa — {mesa.numero}"})


@require_POST
def excluir_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, pk=mesa_id)
    try:
        mesa.delete()
        messages.success(request, "Mesa excluída.")
    except ProtectedError:
        # A mesa já tem comandas associadas (on_delete=PROTECT em Comanda.mesa),
        # então excluir apagaria o histórico de contas dessa mesa.
        messages.error(request, "Não é possível excluir: esta mesa já tem comandas registradas. "
                                 "Marque-a como inativa em vez de excluir.")
    return redirect("mesas")


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
