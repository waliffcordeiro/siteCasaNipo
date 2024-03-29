from django.shortcuts import render
from .models import Geladeira, Pessoas, TrabalhoFogao, TrabalhoGeladeira, MicroEFogao
from Scripts import getDays
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .forms import MesForm


# Create your views here.

def core(request):
    template_name = 'core.html'
    context = {
        'Geladeira': Geladeira.objects.all(),
        'TrabalhoGeladeira': TrabalhoGeladeira.objects.all(),
        'TrabalhoFogao': TrabalhoFogao.objects.all()
    }

    return render(request, template_name, context)


@login_required
def atualiza_lista(request):
    template_name = 'atualiza.html'
    form = MesForm(request.POST or None)
    context = {}
    # Se o forms for válido
    if form.is_valid():
        # Coleta a opção
        mes = form.cleaned_data.get('field')
        mes = int(mes)
        # Mostra somente daquele tipo especifico
        c = getDays.calendar.Calendar(0)
        data_atual = getDays.date.today()
        mes_aux = c.monthdays2calendar(data_atual.year, mes)
        trabalho_no_mes = TrabalhoFogao.objects.filter(dia__month=mes)
        if len(trabalho_no_mes) > 0:
            context["Erro"] = "Já foi atualizada a lista deste mês!"
        else:
            lavaGeladeira(mes_aux, mes)
            lavaFogao(mes_aux, mes)
            context["Sucesso"] = "A lista do mês foi atualizada!"
    context["form"] = form
    return render(request, template_name, context)


def lavaGeladeira(semana, mes):
    quantidadeGeladeira = Geladeira.objects.count()
    geladeiras = Geladeira.objects.all()
    segundaSemana, quartaSemana = getDays.diasGeladeira(semana,mes)  # Lista com os dias de trabalho
    quantidadePessoas = (quantidadeGeladeira * 2)
    listpessoasTrabalho = Pessoas.objects.order_by('prioridadeGeladeira')[:quantidadePessoas]
    listpessoasnaoTrabalho = Pessoas.objects.order_by('prioridadeGeladeira')[quantidadePessoas:]
    pessoasTotal = (len(listpessoasTrabalho) + len(listpessoasnaoTrabalho))
    for idx, pessoa in enumerate(listpessoasTrabalho):
        # Das pessoas que trabalharem, iremos aumentar sua prioridade
        # Aumento proporcional ao número de pessoas
        pessoa.prioridadeGeladeira += (pessoasTotal - quantidadePessoas)
        pessoa.save()
        if idx < (quantidadePessoas / 2):
            TrabalhoGeladeira.objects.create(pessoa=pessoa, geladeira=geladeiras[idx % quantidadeGeladeira],
                                             dia=segundaSemana[0], dia_fim=segundaSemana[3] + timedelta(days=1))
        else:
            TrabalhoGeladeira.objects.create(pessoa=pessoa, geladeira=geladeiras[idx % quantidadeGeladeira],
                                             dia=quartaSemana[0], dia_fim=quartaSemana[3] + timedelta(days=1))
    for pessoa in listpessoasnaoTrabalho:
        print(pessoa)
        # Das pessoas que seguem a lista iremos subtrair a quantidade de pessoas que trabalharam
        pessoa.prioridadeGeladeira -= quantidadePessoas
        pessoa.save()


def lavaFogao(semana, mes):
    quantidadeFogao = MicroEFogao.objects.count()
    fogoeos = MicroEFogao.objects.all()
    segundas, quartas, sextas = getDays.diasFogaoMicroondas(semana, mes)
    diaLimpeza = segundas + quartas + sextas
    quantidadePessoas = (len(segundas) + len(quartas) + len(sextas)) * quantidadeFogao
    listPessoastrabalho = Pessoas.objects.order_by('prioridadeFogao')[:quantidadePessoas]
    listpessoasnaoTrabalho = Pessoas.objects.order_by('prioridadeFogao')[quantidadePessoas:]
    pessoasTotal = (len(listPessoastrabalho) + len(listpessoasnaoTrabalho))
    for idx, pessoa in enumerate(listPessoastrabalho):
        # Das pessoas que trabalharem, iremos aumentar sua prioridade
        # Aumento proporcional ao número de pessoas
        pessoa.prioridadeFogao += (pessoasTotal - quantidadePessoas)
        pessoa.save()
        TrabalhoFogao.objects.create(pessoa=pessoa, fogao=fogoeos[idx % quantidadeFogao],
                                     dia=diaLimpeza[idx])
    for pessoa in listpessoasnaoTrabalho:
        print(pessoa)
        # Das pessoas que seguem a lista iremos subtrair a quantidade de pessoas que trabalharam
        pessoa.prioridadeFogao -= quantidadePessoas
        pessoa.save()
