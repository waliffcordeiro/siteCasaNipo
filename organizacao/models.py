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

    class Meta:
        verbose_name = 'Micro-ondas e Fogão'
        verbose_name_plural = "Micro-ondas e Fogões"


class Pessoas(models.Model):
    nome = models.CharField(max_length=120,
                            help_text='Na inserção de novas pessoas, a prioridade será zero. Caso queira alterar, '
                                      'entre na aba da pessoa e altere o valor manualmente')
    # Com o menor numero de prioridade é quem vai lavar
    prioridadeFogao = models.IntegerField(blank=True, default=0)
    prioridadeGeladeira = models.IntegerField(blank=True, default=0)

    def save(self, *args, **kwargs):
        # Primeira vez
        if not self.pk:
            pessoas = Pessoas.objects.all()
            for pessoa in pessoas:
                pessoa.prioridadeFogao += 1
                pessoa.prioridadeGeladeira += 1
                pessoa.save()
            self.prioridadeGeladeira = 0
            self.prioridadeFogao = 0
            super(Pessoas, self).save(*args, **kwargs)
        else:
            super(Pessoas, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print('vamo simbora')
        pessoas = Pessoas.objects.all()
        for pessoa in pessoas:
            if pessoa.prioridadeFogao > self.prioridadeFogao:
                pessoa.prioridadeFogao -= 1
            if pessoa.prioridadeGeladeira > self.prioridadeGeladeira:
                pessoa.prioridadeGeladeira -= 1

            pessoa.save()
        super(Pessoas, self).delete(*args, **kwargs)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = "Lista de Pessoas"


class TrabalhoGeladeira(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    geladeira = models.ForeignKey(Geladeira, on_delete=models.CASCADE)
    dia = models.DateField('Dia')
    dia_fim = models.DateField('último dia', default="1999-01-01")

    def __str__(self):
        return str(self.pessoa) + " - " + str(self.geladeira) + " - " + " Dia " + str(self.dia.day)

    class Meta:
        verbose_name = 'Relação de Limpeza da Geladeira'
        verbose_name_plural = "Relação de Limpeza das Geladeiras"


class TrabalhoFogao(models.Model):
    pessoa = models.ForeignKey(Pessoas, on_delete=models.CASCADE)
    fogao = models.ForeignKey(MicroEFogao, on_delete=models.CASCADE)
    dia = models.DateField('Dia')

    def __str__(self):
        return str(self.pessoa) + " - " + str(self.fogao) + " - " + " Dia " + str(self.dia.day)

    class Meta:
        verbose_name = 'Relação de Limpeza do Fogão'
        verbose_name_plural = "Relação de Limpeza dos Fogões"
