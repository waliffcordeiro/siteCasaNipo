from django.db import models


# Create your models here.

class Geladeira(models.Model):
    # Limpeza na segunda e quarta semana do mẽs
    SEMANA_CHOICES = [
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    # Dia da semana da limpeza
    numGeladeira = models.IntegerField('Número da Geladeira')
    dia_inicial_limpeza = models.IntegerField(choices=SEMANA_CHOICES)
    dia_final_limpeza = models.IntegerField(choices=SEMANA_CHOICES)

    def __str__(self):
        return "Geladeira" + " " + str(self.numGeladeira)


class MicroEFogao(models.Model):
    # Para casa nipo: Toda semana segunda, quarta e sexta
    SEMANA_CHOICES = [
        (0, 'Segunda'),
        (1, 'Terça'),
        (2, 'Quarta'),
        (3, 'Quinta'),
        (4, 'Sexta'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    dia_de_limpeza = models.IntegerField(choices=SEMANA_CHOICES)
    dia_de_limpeza1 = models.IntegerField(choices=SEMANA_CHOICES)
    dia_de_limpeza2 = models.IntegerField(choices=SEMANA_CHOICES)

    def __str__(self):
        return "Microondas e Fogão"


class Pessoas(models.Model):
    nome = models.CharField(max_length=120)
    # Com o menor numero de prioridade é quem vai lavar
    prioridadeFogao = models.IntegerField()
    prioridadeGeladeira = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = "Pessoas"


class TrabalhoGeladeira(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    geladeira = models.ForeignKey(Geladeira, on_delete=models.CASCADE)
    dia = models.DateField('Dia')

    def __str__(self):
        return str(self.pessoa) + " - " + str(self.geladeira) + " - " + " Dia " + str(self.dia.day)


class TrabalhoFogao(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    fogao = models.ForeignKey(MicroEFogao, on_delete=models.CASCADE)
    dia = models.DateField('Dia')
