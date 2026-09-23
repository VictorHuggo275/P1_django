from django.contrib import admin
from .models import Prato, Combo, Mesa, Comanda, Item

admin.site.register(Prato)
admin.site.register(Combo)
admin.site.register(Mesa)
admin.site.register(Comanda)
admin.site.register(Item)
