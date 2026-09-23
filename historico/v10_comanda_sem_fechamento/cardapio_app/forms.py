from django import forms
from .models import Item, Prato, Combo, Mesa


class PratoForm(forms.ModelForm):
    class Meta:
        model = Prato
        fields = ["nome", "descricao", "preco", "disponivel"]


class ComboForm(forms.ModelForm):
    class Meta:
        model = Combo
        fields = ["nome", "descricao", "preco", "disponivel", "pratos"]


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["numero", "capacidade", "ativa"]


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["prato", "combo", "quantidade"]
