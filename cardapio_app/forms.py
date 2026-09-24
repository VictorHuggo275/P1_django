from django import forms
from django.core.exceptions import ValidationError

from .models import Categoria, Combo, Item, Mesa, Prato


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]


class PratoForm(forms.ModelForm):
    class Meta:
        model = Prato
        fields = ["nome", "descricao", "preco", "categoria", "disponivel"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3})}

    def clean_preco(self):
        # Feature 2 (validação customizada): o preço do prato precisa ser
        # maior que zero, algo além do "campo obrigatório" que o Django
        # já garante sozinho.
        preco = self.cleaned_data["preco"]
        if preco <= 0:
            raise ValidationError("O preço precisa ser maior que zero.")
        return preco


class ComboForm(forms.ModelForm):
    # Campo redefinido explicitamente: usamos checkboxes em vez do <select multiple>
    # padrão do Django, que exigia Ctrl/Cmd + clique para marcar mais de um prato
    # e por isso dava a impressão de que só era possível escolher um prato por combo.
    pratos = forms.ModelMultipleChoiceField(
        queryset=Prato.objects.filter(disponivel=True).order_by("nome"),
        widget=forms.CheckboxSelectMultiple,
        label="Pratos do combo",
        help_text="Selecione 2 ou mais pratos para montar o combo.",
    )

    class Meta:
        model = Combo
        fields = ["nome", "descricao", "preco", "categoria", "disponivel", "pratos"]
        widgets = {"descricao": forms.Textarea(attrs={"rows": 3})}

    def clean_preco(self):
        # Mesma regra de validação customizada aplicada ao combo.
        preco = self.cleaned_data["preco"]
        if preco <= 0:
            raise ValidationError("O preço precisa ser maior que zero.")
        return preco

    def clean_pratos(self):
        pratos = self.cleaned_data["pratos"]
        if pratos.count() < 2:
            raise ValidationError("Um combo precisa ter pelo menos 2 pratos.")
        return pratos


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["numero", "capacidade", "ativa"]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["prato", "combo", "quantidade"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Antes o dropdown listava TODOS os pratos/combos, inclusive os
        # marcados como indisponíveis. Agora só aparece o que pode ser pedido.
        self.fields["prato"].queryset = Prato.objects.filter(disponivel=True).order_by("nome")
        self.fields["combo"].queryset = Combo.objects.filter(disponivel=True).order_by("nome")

    def clean_quantidade(self):
        quantidade = self.cleaned_data["quantidade"]
        if quantidade < 1:
            raise ValidationError("A quantidade precisa ser pelo menos 1.")
        return quantidade

    def clean(self):
        # Essa regra vivia solta dentro da view; trazida para o form, ela passa
        # a valer sempre que o ItemForm for usado, e é reportada como erro do
        # formulário (com form.is_valid() == False) em vez de ser checada "na mão"
        # depois de já considerar o form válido.
        cleaned_data = super().clean()
        prato = cleaned_data.get("prato")
        combo = cleaned_data.get("combo")
        if prato and combo:
            raise ValidationError("Escolha um prato ou um combo, não os dois.")
        if not prato and not combo:
            raise ValidationError("Escolha um prato ou um combo.")
        return cleaned_data
