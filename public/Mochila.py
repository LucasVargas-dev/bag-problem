"""O problema da mochila: um problema de otimização combinatória.
O nome dá-se devido ao modelo de uma situação em que é necessário
preencher uma mochila com objetos de diferentes pesos e valores.
O objetivo é que se preencha a mochila com o maior valor possível,
não ultrapassando o peso máximo."""
#RODAR COM PYTHON 3!!!

#import Genetic

from random import getrandbits, randint, random, choice

def individual(n_de_itens):
    """Cria um membro da populacao"""
    return [ getrandbits(1) for x in range(n_de_itens) ]

def population(n_de_individuos, n_de_itens):
    """"Cria a populacao"""
    return [ individual(n_de_itens) for x in range(n_de_individuos) ]

def fitness(individuo, peso_maximo, pesos_e_valores):
    """Faz avaliacao do individuo"""
    peso_total, valor_total = 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * pesos_e_valores[indice][0])
        valor_total += (individuo[indice] * pesos_e_valores[indice][1])

    if (peso_maximo - peso_total) < 0:
        return -1 #retorna -1 no caso de peso excedido
    return valor_total #se for um individuo valido retorna seu valor, sendo maior melhor

def media_fitness(populacao, peso_maximo, pesos_e_valores): #só leva em consideracao os elementos que respeitem o peso maximo da mochila
    """Encontra a avalicao media da populacao"""
    summed = sum(fitness(x, peso_maximo, pesos_e_valores) for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0)
    return summed / (len(populacao) * 1.0)

def selecao_roleta(pais):
    """Seleciona um pai e uma mae baseado nas regras da roleta"""
    def sortear(fitness_total, indice_a_ignorar=-1): #2 parametro garante que não vai selecionar o mesmo elemento
        """Monta roleta para realizar o sorteio"""
        roleta, acumulado, valor_sorteado = [], 0, random()

        if indice_a_ignorar!=-1: #Desconta do total, o valor que sera retirado da roleta
            fitness_total -= valores[0][indice_a_ignorar]

        for indice, i in enumerate(valores[0]):
            if indice_a_ignorar==indice: #ignora o valor ja utilizado na roleta
                continue
            acumulado += i
            roleta.append(acumulado/fitness_total)
            if roleta[-1] >= valor_sorteado:
                return indice
    
    valores = list(zip(*pais)) #cria 2 listas com os valores fitness e os cromossomos
    fitness_total = sum(valores[0])

    indice_pai = sortear(fitness_total) 
    indice_mae = sortear(fitness_total, indice_pai)

    pai = valores[1][indice_pai]
    mae = valores[1][indice_mae]
    
    return pai, mae

def evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos, mutate=0.05): 
    """Tabula cada individuo e o seu fitness"""
    pais = [ [fitness(x, peso_maximo, pesos_e_valores), x] for x in populacao if fitness(x, peso_maximo, pesos_e_valores) >= 0]
    pais.sort(reverse=True)
    
    # REPRODUCAO
    filhos = []
    while len(filhos) < n_de_cromossomos:
        homem, mulher = selecao_roleta(pais)
        meio = len(homem) // 2
        filho = homem[:meio] + mulher[meio:]
        filhos.append(filho)
    
    # MUTACAO
    for individuo in filhos:
        if mutate > random():
            pos_to_mutate = randint(0, len(individuo)-1)
            if individuo[pos_to_mutate] == 1:
                individuo[pos_to_mutate] = 0
            else:
                individuo[pos_to_mutate] = 1

    return filhos

                #[peso,valor]
pesos_e_valores = [[4, 30], [8, 10], [8, 30], [25, 75], \
                   [2, 10], [50, 100], [6, 300], [12, 50], \
                   [100, 400], [8, 300]]
peso_maximo = 100
n_de_cromossomos = 150
geracoes = 80
n_de_itens = len(pesos_e_valores) #Analogo aos pesos e valores

#EXECUCAO DOS PROCEDIMENTOS
populacao = population(n_de_cromossomos, n_de_itens)
historico_de_fitness = [media_fitness(populacao, peso_maximo, pesos_e_valores)]
for i in range(geracoes):
    populacao = evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos)
    historico_de_fitness.append(media_fitness(populacao, peso_maximo, pesos_e_valores))

#PRINTS DO TERMINAL
for indice,dados in enumerate(historico_de_fitness):
   print ("Geracao: ", indice," | Media de valor na mochila: ", dados)

print("\nPeso máximo:",peso_maximo,"g\n\nItens disponíveis:")
for indice,i in enumerate(pesos_e_valores):
    print("Item ",indice+1,": ",i[0],"g | R$",i[1])
    
print("\nExemplos de boas solucoes: ")
for i in range(5):
    print(populacao[i])

#GERADOR DE GRAFICO
#import matplotlib
#import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt
# plt.plot(range(len(historico_de_fitness)), historico_de_fitness)
# plt.grid(True, zorder=0)
# plt.title("Problema da mochila")
# plt.xlabel("Geracao")
# plt.ylabel("Valor medio da mochila")
# plt.show()

import PySimpleGUI as sg

# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
# layout = [  [sg.Text('Digite o peso:'), sg.InputText()] ]

# Create the Window
# window = sg.Window('Problema da Mochila', layout)
# Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
#         break
#     print('You entered ', values[0])

# window.close()

def calculos(pesos_e_valores, peso_maximo):
    # pesos_e_valores = [[4, 30], [8, 10], [8, 30], [25, 75], \
    #                [2, 10], [50, 100], [6, 300], [12, 50], \
    #                [100, 400], [8, 300]]
    # peso_maximo = 100
    n_de_cromossomos = 150
    geracoes = 80
    n_de_itens = len(pesos_e_valores) #Analogo aos pesos e valores

    #EXECUCAO DOS PROCEDIMENTOS
    populacao = population(n_de_cromossomos, n_de_itens)
    historico_de_fitness = [media_fitness(populacao, peso_maximo, pesos_e_valores)]
    for i in range(geracoes):
        populacao = evolve(populacao, peso_maximo, pesos_e_valores, n_de_cromossomos)
        historico_de_fitness.append(media_fitness(populacao, peso_maximo, pesos_e_valores))

    #PRINTS DO TERMINAL
    for indice,dados in enumerate(historico_de_fitness):
        print ("Geracao: ", indice," | Media de valor na mochila: ", dados)

    print("\nPeso máximo:",peso_maximo,"g\n\nItens disponíveis:")
    for indice,i in enumerate(pesos_e_valores):
        print("Item ",indice+1,": ",i[0],"g | R$",i[1])
        
    print("\nExemplos de boas solucoes: ")
    for i in range(5):
        print(populacao[i])


# import Inputs

# class TelaPython: 
#   def __init__(self):
#     sg.theme('DarkAmber') 

#     layout = [
#         [sg.Text('Digite o Valor:', size=(15,-2)), sg.Input(size=(20,-2), key='valor')],
#         [sg.Text('Digite o Peso:', size=(15,-2)), sg.Input(size=(20,-2), key='peso')],
#         [sg.Text('Peso da Mochila:', size=(15,-2)), sg.Input(size=(20,-2), key='mochila')],
#         [sg.Button('Enviar Dados')],
#         [sg.Output(size=(100,50))],
#     ]
#     self.janela = sg.Window("Problema da Mochila", size=(305, 250)).layout(layout)
#     # self.button, self.values = self.janela.Read()
#     #, key='enviar'), sg.Button('Calcular', key='calcular')

#   def Iniciar(self):
#       inputs = []
#       while True:
#         self.button, self.values = self.janela.Read()
#         valor = self.values['valor']
#         peso = self.values['peso']
#         inputs.append(valor, peso)
#         mochila = self.values['mochila'] 
#         print(f'Valor: {valor}')
#         print(f'Peso: {peso}')
#         print(f'Mochila: {mochila}')
#         print(valor, peso)
#         print(inputs)

  

# tela = TelaPython()
# tela.Iniciar()

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
mochila = int(input('Qual o peso da mochila? '))

calculos(matriz, mochila)