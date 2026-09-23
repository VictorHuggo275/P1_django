from django import forms
from .models import Mesa, Prato


class PratoForm(forms.ModelForm):
    class Meta:
        model = Prato
        fields = ["nome", "descricao", "preco", "disponivel"]


class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ["numero", "capacidade", "ativa"]
