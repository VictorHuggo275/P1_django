from decimal import Decimal
from django.db import models


class Categoria(models.Model):
    # Categoria compartilhada entre Pratos e Combos, usada para organizar o
    # cardápio e alimentar o filtro da Feature 1 (busca e filtro na listagem).
    nome = models.CharField("Nome", max_length=60, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Prato(models.Model):
    nome = models.CharField("Nome", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    preco = models.DecimalField("Preço", max_digits=8, decimal_places=2)
    disponivel = models.BooleanField("Disponível", default=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="pratos", verbose_name="Categoria",
    )

    def __str__(self):
        return self.nome


class Combo(models.Model):
    nome = models.CharField("Nome", max_length=100)
    descricao = models.TextField("Descrição", blank=True)
    preco = models.DecimalField("Preço", max_digits=8, decimal_places=2)
    disponivel = models.BooleanField("Disponível", default=True)
    pratos = models.ManyToManyField(Prato, blank=True, related_name="combos", verbose_name="Pratos")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="combos", verbose_name="Categoria",
    )

    def __str__(self):
        return self.nome


class Mesa(models.Model):
    numero = models.PositiveIntegerField("Número", unique=True)
    capacidade = models.PositiveIntegerField("Capacidade", default=4)
    ativa = models.BooleanField("Ativa", default=True)

    def __str__(self):
        return f"Mesa {self.numero}"


class Comanda(models.Model):
    ABERTA = "ABERTA"
    FECHADA = "FECHADA"
    STATUS_CHOICES = [(ABERTA, "Aberta"), (FECHADA, "Fechada")]

    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name="comandas")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ABERTA)
    aberta_em = models.DateTimeField(auto_now_add=True)
    fechada_em = models.DateTimeField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"Comanda #{self.id} - Mesa {self.mesa.numero}"


class Item(models.Model):
    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name="itens")
    prato = models.ForeignKey(Prato, on_delete=models.PROTECT, null=True, blank=True)
    combo = models.ForeignKey(Combo, on_delete=models.PROTECT, null=True, blank=True)
    quantidade = models.PositiveIntegerField("Quantidade", default=1)
    preco_unitario = models.DecimalField("Preço unitário", max_digits=8, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        nome = self.prato.nome if self.prato else self.combo.nome
        return f"{self.quantidade}x {nome}"
