from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Mesa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero", models.PositiveIntegerField(unique=True)),
                ("capacidade", models.PositiveIntegerField(default=4)),
                ("ativa", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Prato",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100)),
                ("descricao", models.TextField(blank=True)),
                ("preco", models.DecimalField(decimal_places=2, max_digits=8)),
                ("disponivel", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Combo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100)),
                ("descricao", models.TextField(blank=True)),
                ("preco", models.DecimalField(decimal_places=2, max_digits=8)),
                ("disponivel", models.BooleanField(default=True)),
                ("pratos", models.ManyToManyField(blank=True, related_name="combos", to="cardapio_app.prato")),
            ],
        ),
        migrations.CreateModel(
            name="Comanda",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("ABERTA","Aberta"),("FECHADA","Fechada")], default="ABERTA", max_length=10)),
                ("aberta_em", models.DateTimeField(auto_now_add=True)),
                ("fechada_em", models.DateTimeField(blank=True, null=True)),
                ("total", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=10)),
                ("mesa", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="comandas", to="cardapio_app.mesa")),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantidade", models.PositiveIntegerField(default=1)),
                ("preco_unitario", models.DecimalField(decimal_places=2, max_digits=8)),
                ("combo", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="cardapio_app.combo")),
                ("comanda", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="cardapio_app.comanda")),
                ("prato", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to="cardapio_app.prato")),
            ],
        ),
    ]
