import numpy as np

m = 2

while True:
    try:
        n = int(input('Quantos elementos terão em cada vetor? '))
        if n < 1:
            print('\033[31mValor INVÁLIDO! Digite apenas valores maiores que "0"!\033[m')
        else:
            break
    except ValueError:
        print('\033[31mValor INVÁLIDO! Digite apenas valores inteiros!\033[m')

listaA = list()
for i in range(1, m + 1):
    vetor = list(42)
    for j in range(1, n + 1):
        while True:
            try:
                v = int(input(f'Digite o {j}º valor da {i}ª lista: '))
                break
            except ValueError:
                print('\033[31mValor INVÁLIDO! Digite apenas valores inteiros!\033[m')
        vetor.append(v)
    listaA.append(vetor)

matriz = np.array(listaA)
print(f'\033[32mA matriz gerada foi:\n{matriz}\033[m')