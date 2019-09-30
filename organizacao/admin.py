from django.contrib import admin
from .models import MicroEFogao, Geladeira, Pessoas, TrabalhoGeladeira, TrabalhoFogao

# Register your models here.
admin.site.register(MicroEFogao)
admin.site.register(Geladeira)


class PessoasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prioridadeFogao', 'prioridadeGeladeira')
    #exclude = ('prioridadeFogao', 'prioridadeGeladeira', )

admin.site.register(Pessoas, PessoasAdmin)
admin.site.register(TrabalhoGeladeira)
admin.site.register(TrabalhoFogao)
