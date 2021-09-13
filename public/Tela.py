import tkinter
from tkinter import messagebox
import numpy as np
from random import getrandbits, randint, random, choice

def individual(n_de_itens):
    # Cria apenas um membro da população, faz o for para o número de itens
    return [ getrandbits(1) for x in range(n_de_itens) ]

def population(n_de_individuos, n_de_itens):
    # Cria a populacao 
    return [ individual(n_de_itens) for x in range(n_de_individuos) ]

def fitness(individuo, peso_maximo, pesos_e_valores):
    # Faz avaliacao do individuo, o fitness são os indivíduos de melhor performance
    peso_total, valor_total = 0, 0
    for indice, valor in enumerate(individuo):
        peso_total += (individuo[indice] * pesos_e_valores[indice][0])
        valor_total += (individuo[indice] * pesos_e_valores[indice][1])

    if (peso_maximo - peso_total) < 0: # filtra os válidos
        return -1 # em caso de peso exceder o peso da mochila retorna -1
    return valor_total # se for um individuo válido retorna seu valor, sendo maior melhor

def media_fitness(populacao, peso_maximo, pesos_e_valores): #só leva em consideracao os elementos que respeitem o peso maximo da mochila
    # Encontra a avalicao media da populacao, summed é como se refizesse os fitness e realizasse a soma, para no final dividir e obter a média
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
    # Monta a tabela de cada individuo e o seu fitness, método principal
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

def calculos(pesos_e_valores, peso_maximo):
    # pesos_e_valores = [[6, 31], [9, 11], [8, 30], [29, 73], \
    #                [26, 140], [50, 102], [5, 301], [18, 50], \
    #                [19, 48], [81, 200]]
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

    from matplotlib import pyplot as plt

    plt.plot(range(len(historico_de_fitness)), historico_de_fitness)
    plt.grid(True, zorder=0)
    plt.title("Problema da mochila")
    plt.xlabel("Geracao")
    plt.ylabel("Valor medio da mochila")
    plt.show()

def list_to_string(lista, func=lambda x:    (x), separador='\n'):
    result = ''
    for element in lista:
        result += func(element)
        result += separador
    return result


class Resultados:
    def __init__(self, resultados):
        self.tela = tkinter.Tk()

        self.frame = tkinter.Frame(self.tela, width=100, height=100)
        self.label_resultados = tkinter.Label(self.frame, text=list_to_string(resultados))
        self.label_resultados.pack()
        self.frame.pack()

        tkinter.mainloop()

class Tela:
    def __init__(self):
        self.mochila = []
        self.main_window = tkinter.Tk()
        
        # formulário
        self.formulario = tkinter.Frame(self.main_window)
        self.label_valor = tkinter.Label(self.formulario, text="Valor")
        self.label_peso = tkinter.Label(self.formulario, text="Peso")
        self.label_quantidade = tkinter.Label(self.formulario, text="quantidade")

        self.campo_valor = tkinter.Entry(self.formulario, width=30)
        self.campo_peso = tkinter.Entry(self.formulario, width=30)
        self.campo_quantidade = tkinter.Entry(self.formulario, width=30)

        self.label_valor.pack()
        self.campo_valor.pack()
        self.label_peso.pack()
        self.campo_peso.pack()
        self.label_quantidade.pack()
        self.campo_quantidade.pack()
        self.formulario.pack()

        # ações
        self.acoes = tkinter.Frame(self.main_window)
        self.btn_adicionar_mochila = tkinter.Button(self.acoes, text="adicionar mochila", command=self.adicionar_mochila)
        self.btn_exibir = tkinter.Button(self.acoes, text="exibir resultado", command=self.exibir)

        self.btn_adicionar_mochila.pack(side='left')
        self.btn_exibir.pack(side='left')
        self.acoes.pack()
    
        tkinter.mainloop()
    
    def adicionar_mochila(self):
        validacao = self.valida_formulario()

        if validacao == False:
            messagebox.showerror('Erro de validação', message='Todos os campos precisam estar preenchidos')
            return

        valor = float(self.campo_valor.get())
        peso = float(self.campo_peso.get())
        self.quantidade = int(self.campo_quantidade.get())
        mochila = [valor, peso]
        self.mochila.append(mochila)

    def exibir(self):
        # print(self.mochila)
        # print(self.quantidade)
        resultados_mostrar = calculos(self.mochila, self.quantidade)
        # resultados_mostrar = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]] # troque pelo retorno dos resultados
        # tela_resultados = Resultados(resultados_mostrar)

    def valida_formulario(self):
        if self.campo_valor.get() == '' or self.campo_peso.get() == '':
            return False
        return True

minha_tela = Tela()
