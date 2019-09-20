import calendar
from datetime import date

####################### Obtendo as segundas, quartas e sextas ###################

def diasFogaoMicroondas(mes):
    # Listas
    segundas = []
    quartas = []
    sextas = []
    # Defines
    SEG = 0
    QUA = 2
    SEX = 4
    for semana in mes:
        for diaMes, diaSem in semana:
            if diaSem == SEG and diaMes:
                # and diaMes é para excluir os dias 0
                segundas.append(diaMes)
            if diaSem == QUA and diaMes:
                quartas.append(diaMes)
            if diaSem == SEX and diaMes:
                sextas.append(diaMes)
    return segundas, quartas, sextas


####################### Obtendo a segunda e quarta semana ###################
# mes[1] ou mes[2] - a segunda semana do mês

# Verificar se devemos considerar a segunda semana sendo mes[1] ou mes[2]
# Essa diferença se dá quando um mês não começa na segunda-feira, os dias antes da segunda são preenchidos com 0

def diasGeladeira(semana):
    segundaSemana = []
    quartaSemana = []
    QUI = 3
    aux = 0
    for dia in semana[0]:
        if dia[0] == 0:
            aux +=1
    second = 1 if aux <= 4 else 2
    fourth = 3 if second == 1 else 4

    # dia[0] é o dia de forma numérico e dia[1] representa o dia da semana (0 = segunda e 6 = domingo)
    for dia in semana[second]:
        if dia[1] >= QUI:
            segundaSemana.append(dia[0])
            # Quinta a domingo
    for dia in semana[fourth]:
        if dia[1] >= QUI:
            quartaSemana.append(dia[0])
            # Quinta a domingo
    return segundaSemana, quartaSemana


if __name__ == "__main__":
    c = calendar.Calendar(0)
    data_atual = date.today()
    mes = c.monthdays2calendar(data_atual.year, data_atual.month)

    segundas, quartas, sextas = diasFogaoMicroondas(mes)

    print("Segundas: ", segundas)
    print("Quartas: ", quartas)
    print("Sextas: ", sextas)

    segundaSemana, quartaSemana = diasGeladeira(mes)

    print("Quinta a domingo da segunda semana: ", segundaSemana)
    print("Quinta a domingo da quarta semana: ", quartaSemana)
