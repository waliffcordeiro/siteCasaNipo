from django.contrib import admin
from .models import MicroEFogao, Geladeira, Pessoas, TrabalhoGeladeira, TrabalhoFogao

# Register your models here.
admin.site.register(MicroEFogao)
admin.site.register(Geladeira)


class PessoasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'prioridadeFogao', 'prioridadeGeladeira')
    actions = ['multar_pessoa_fogao', 'multar_pessoa_geladeira']
    # exclude = ('prioridadeFogao', 'prioridadeGeladeira', )

    def multar_pessoa_fogao(self, request, queryset):
        for pessoa_multada in queryset:
            pessoas = Pessoas.objects.all()
            for pessoa in pessoas:
                if pessoa.prioridadeFogao < pessoa_multada.prioridadeFogao:
                    pessoa.prioridadeFogao += 1
                pessoa.save()
            pessoa_multada.prioridadeFogao = 0
            pessoa_multada.save()

    multar_pessoa_fogao.short_description = 'Multar pessoa Fogão'

    def multar_pessoa_geladeira(self, request, queryset):
        for pessoa_multada in queryset:
            pessoas = Pessoas.objects.all()
            for pessoa in pessoas:
                if pessoa.prioridadeGeladeira < pessoa_multada.prioridadeGeladeira:
                    pessoa.prioridadeGeladeira += 1
                pessoa.save()
            pessoa_multada.prioridadeGeladeira = 0
            pessoa_multada.save()

    multar_pessoa_geladeira.short_description = 'Multar pessoa Geladeira'

admin.site.register(Pessoas, PessoasAdmin)
admin.site.register(TrabalhoGeladeira)
admin.site.register(TrabalhoFogao)
