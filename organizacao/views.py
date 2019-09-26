from django.shortcuts import render
from .models import Geladeira, Pessoas, TrabalhoFogao, TrabalhoGeladeira, MicroEFogao
from Scripts import getDays

c = getDays.calendar.Calendar(0)
data_atual = getDays.date.today()
mes = c.monthdays2calendar(data_atual.year, data_atual.month)


# Create your views here.

def core(request):
    template_name = 'core.html'
    context = {
        'Geladeira': Geladeira.objects.all()
    }

    return render(request, template_name, context)


def atualiza_lista(request):
    template_name = 'atualiza.html'

    context = {

    }

    lavaGeladeira()
    lavaFogao()

    return render(request, template_name, context)


def lavaGeladeira():
    quantidadeGeladeira = Geladeira.objects.count()
    geladeiras = Geladeira.objects.all()
    segundaSemana, quartaSemana = getDays.diasGeladeira(mes)  # Lista com os dias de trabalho
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
                                             dia=segundaSemana[0])
        else:
            TrabalhoGeladeira.objects.create(pessoa=pessoa, geladeira=geladeiras[idx % quantidadeGeladeira],
                                             dia=quartaSemana[0])
    for pessoa in listpessoasnaoTrabalho:
        print(pessoa)
        # Das pessoas que seguem a lista iremos subtrair a quantidade de pessoas que trabalharam
        pessoa.prioridadeGeladeira -= quantidadePessoas
        pessoa.save()

def lavaFogao():
    quantidadeFogao = MicroEFogao.objects.count()
