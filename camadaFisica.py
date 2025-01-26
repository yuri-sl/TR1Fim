import gi
import numpy as np
import random
import math

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas


def converterBinario(palavra):
    binarios = []
    for char in palavra:
        valor_binario = format(ord(char), '08b')
        binarios.append([int(bit) for bit in valor_binario])  # Adiciona o valor binário à lista        
    return binarios

def convertNRZ(byteMSG):
    for i in range(0,len(byteMSG)):
        byte = byteMSG[i]
        for j in range(0,len(byte)):
            bit = byte[j]
            if bit== 0:
                byte[j] = -1
            else:
                byte[j] = 1
    return byteMSG



#Simulação de erro no meio fisico
class ErroMeioFisico:
    def __init__(self, lista = [], chance = 0.00011):
        self.lista = lista
        self.chance = chance

    def erro(self):
        nova_lista = []
        for item in self.lista:
            novo_item = []
            for bit in item:  # Itera por cada bit no item (representação binária)
                if random.random() < self.chance:
                    novo_item.append( 1 if bit == 0 else 0)  # Inverte o bit
                else:
                    novo_item.append(bit)  # Mantém o bit
            nova_lista.append(novo_item)
        return nova_lista

#Modulação Digital
def buildNRZ(binWordNRZ):
    x_axis = []

    n = len(binWordNRZ)

    for j in range(0,8*n):
        x_axis.append(j)

    print(binWordNRZ)
    print(x_axis)
    return binWordNRZ,x_axis
    #show_graph(binWordNRZ, x_axis, "Grafico NRZ", "Sinal NRZ")

def convert_Manchester(byteMSG):
    #print("A byteMSG é ",byteMSG)
    print('The byte in ByteMSG is: ',byteMSG)
    manchester = []
    for byte in byteMSG:
        for bit in byte:
            if bit == 0:
                manchester.append([0,1])
            else:
                manchester.append([1,0])
    return manchester

def buildManchester(binWordManchester):
    x_axis = []
    print("A binwordManchester é ",binWordManchester)
    print("")

    n = len(binWordManchester)

    for j in range(0,2*n):
        x_axis.append(j)

    #print(binWordManchester)
    print("O x_axis é ",x_axis)
    return binWordManchester,x_axis

def convertBipolar(byteMSG):
    bipolar = []
    countOnes = 0
    for byte in byteMSG:
        byte_ins = []
        for bit in byte:
            if bit == 0:
                byte_ins.append(0)
            if bit == 1:
                if countOnes %2 == 0:
                    byte_ins.append(1)
                    countOnes += 1
                else:
                    byte_ins.append(-1)
                    countOnes += 1
        bipolar.append(byte_ins)
    return bipolar

def buildBipolar(binWordBipolar):
    x_axis = []
    n = len(binWordBipolar)
    
    for j in range(0,8*n):
        x_axis.append(j)
    
    print("O x_axis é ",x_axis)
    return binWordBipolar,x_axis

#Modulação por portadora
resolucao = 50
frequencia = 1
def convertASK(byteMSG:list[list[float]]) -> list[list[float]]:
    ask = []
    tempo = 0
    for byte in byteMSG:
        byte_ins = []
        for i in byte:
            if i == 0:
                byte_ins.extend([0 for a in range(resolucao)])
                tempo += resolucao
            else:
                for j in range(resolucao):
                    byte_ins.append(math.cos(2*math.pi*frequencia*tempo)) 
                    tempo += 1/resolucao
        ask.append(byte_ins)
        
    return ask

def convertFSK(byteMSG:list[list[float]]) -> list[list[float]]:
    fsk = []
    tempo = 0
    for byte in byteMSG:
        byte_ins = []
        for i in byte:
            if i == 0:
                for j in range(resolucao):
                    byte_ins.append(math.cos(2*math.pi*frequencia*tempo)) 
                    tempo += 1/resolucao
            else:
                for j in range(resolucao):
                    byte_ins.append(math.cos(4*math.pi*frequencia*tempo)) 
                    tempo += 1/resolucao
        fsk.append(byte_ins)

    return fsk

def convert8QAM(byteMSG:list[list[float]]) -> list[list[float]]:
    ''' Um side effect de modular para 8qam é que, é adicionado digitos 0 suficientes para que a entrada seja divisível por 3, dessa forma não tem sentido dividir a saída em bytes, pois há váiros casos em que a saída não é divisivel por 3 e por 8 ao mesmo tempo'''
    bitList = np.array(byteMSG).flatten().tolist()

    # faz com que a lista de binarios tenha um numero de elementos divisiveis por 3, colocando zeros no final caso não tenha
    bitList.extend([0 for a in range(3-len(bitList)%3) if len(bitList)%3 != 0]) 

    qam = []
    tempo = 0
    for i in range(0,len(bitList),3):
        trio = bitList[i:i+3]
        aq = 0;ai = 0
        # associando cada trio de bits a um simbolo eletrico
        # a constelação aqui está baseada em https://commons.wikimedia.org/wiki/File:Circular_8QAM.svg e https://www.researchgate.net/figure/The-best-constellation-diagram-for-8-QAM-signal_fig1_325088797
        # valores em 1/(math.sqrt(3)+1) para manter a amplitude 
        raiz3 = 1/(math.sqrt(3)+1)
        match trio:
            case [0,0,0]: 
                ai = 1
                aq = 0
            case [0,0,1]: 
                ai = raiz3
                aq = raiz3
            case [0,1,0]: 
                ai = -raiz3
                aq = raiz3
            case [0,1,1]: 
                ai = 0
                aq = 1
            case [1,0,0]: 
                ai = raiz3
                aq = -raiz3
            case [1,0,1]: 
                ai = 0
                aq = -1
            case [1,1,0]: 
                ai = -1
                aq = 0
            case [1,1,1]: 
                ai = -raiz3
                aq = -raiz3

        for i in range(resolucao):
            qam.append(ai*math.sin(2*math.pi*frequencia*tempo) + aq*math.cos(2*math.pi*frequencia*tempo)) 
            tempo += 1/resolucao

    return [qam]

def buildPortadora(binWordPortadora:list[list[float]]):
    x_axis = []
    n = len(binWordPortadora)

    tamanho = 0
    for word in binWordPortadora:
        tamanho += len(word)

    x_axis = np.arange(0,tamanho/resolucao,1/resolucao)

    print("O x_axis é ",x_axis)
    return binWordPortadora,x_axis
