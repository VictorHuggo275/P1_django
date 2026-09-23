from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cardapio_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(model_name="prato", name="nome", field=models.CharField(max_length=100, verbose_name="Nome")),
        migrations.AlterField(model_name="prato", name="descricao", field=models.TextField(blank=True, verbose_name="Descrição")),
        migrations.AlterField(model_name="prato", name="preco", field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Preço")),
        migrations.AlterField(model_name="prato", name="disponivel", field=models.BooleanField(default=True, verbose_name="Disponível")),
        migrations.AlterField(model_name="combo", name="nome", field=models.CharField(max_length=100, verbose_name="Nome")),
        migrations.AlterField(model_name="combo", name="descricao", field=models.TextField(blank=True, verbose_name="Descrição")),
        migrations.AlterField(model_name="combo", name="preco", field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Preço")),
        migrations.AlterField(model_name="combo", name="disponivel", field=models.BooleanField(default=True, verbose_name="Disponível")),
        migrations.AlterField(model_name="combo", name="pratos", field=models.ManyToManyField(blank=True, related_name="combos", to="cardapio_app.prato", verbose_name="Pratos")),
        migrations.AlterField(model_name="mesa", name="numero", field=models.PositiveIntegerField(unique=True, verbose_name="Número")),
        migrations.AlterField(model_name="mesa", name="capacidade", field=models.PositiveIntegerField(default=4, verbose_name="Capacidade")),
        migrations.AlterField(model_name="mesa", name="ativa", field=models.BooleanField(default=True, verbose_name="Ativa")),
        migrations.AlterField(model_name="item", name="quantidade", field=models.PositiveIntegerField(default=1, verbose_name="Quantidade")),
        migrations.AlterField(model_name="item", name="preco_unitario", field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Preço unitário")),
    ]
