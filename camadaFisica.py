import gi
import numpy as np
import random

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


def converterBinario(palavra):
    binarios = []
    for char in palavra:
        valor_binario = format(ord(char), '08b')
        binarios.append(valor_binario)  # Adiciona o valor binário à lista
    return binarios


#Simulação de erro no meio fisico
class ErroMeioFisico:
    def __init__(self, lista = [], chance = 0.01):
        self.lista = lista
        self.chance = chance

    def erro(self):
        nova_lista = []
        for item in self.lista:
            novo_item = ""
            for bit in item:  # Itera por cada bit no item (representação binária)
                if random.random() < self.chance:
                    novo_item += "1" if bit == "0" else "0"  # Inverte o bit
                else:
                    novo_item += bit  # Mantém o bit
            nova_lista.append(novo_item)
        return nova_lista
"""
def teste_erro_meio_fisico():
    palavra = "Test"
    print("Palavra original:", palavra)

    # Converte a palavra para binário
    binarios = converterBinario(palavra)
    print("Binário original:", binarios)

    # Aplica o erro no meio físico
    simulacao_erro = ErroMeioFisico(lista=binarios, chance=0.1)
    binarios_com_erro = simulacao_erro.erro()
    print("Binário com erro:", binarios_com_erro)

    # Verifica se há diferenças
    alteracoes = [
        (original, modificado)
        for original, modificado in zip(binarios, binarios_com_erro)
        if original != modificado
    ]
    print(f"Número de alterações detectadas: {len(alteracoes)}")
    for original, modificado in alteracoes:
        print(f"Original: {original}, Modificado: {modificado}")


# Executa o teste
teste_erro_meio_fisico()
"""


#Modulação Digital
#Gráfico NRZ
class Apper_graph_nrz:
    def __init__(self, a = []):
        self.a = a
        self.apper_new_graph()

    def apper_new_graph(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(len(self.a))

        # Plotando o sinal digital NRZ
        ax.step(t, self.a, where='post', label='Sinal NRZ', linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title("Sinal Digital NRZ")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.legend()
        #Se quiser voltar para o codigo anterior tire as "" e
        #essas duas linhas abaixo
        canvas = FigureCanvas(fig)
        return canvas
   
#Gráfico Manchester
class Apper_graph_manchester:
    def __init__(self, a = []):
        self.a = a
        self.apper_new_graph()

    def apper_new_graph(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(len(self.a))

        # Plotando o sinal digital NRZ
        ax.step(t, self.a, where='post', label='Sinal Manchester', linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title("Sinal Digital Manchester")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.legend()
        #Se quiser voltar para o codigo anterior tire as "" e
        #essas duas linhas abaixo
        canvas = FigureCanvas(fig)
        return canvas 

    def apper_new_graph(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(len(self.a))

        # Plotando o sinal digital NRZ
        ax.step(t, self.a, where='post', label='Sinal NRZ', linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title("Sinal Digital NRZ")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.legend()
        #Se quiser voltar para o codigo anterior tire as "" e
        #essas duas linhas abaixo
        canvas = FigureCanvas(fig)
        return canvas

#Gráfico Bipolar
class Apper_graph_bipolar:
    def __init__(self, a = []):
        self.a = a
        self.apper_new_graph()

    def apper_new_graph(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(len(self.a))

        # Plotando o sinal digital NRZ
        ax.step(t, self.a, where='post', label='Sinal Bipolar', linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title("Sinal Digital Bipolar")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        #essas duas linhas abaixo
        canvas = FigureCanvas(fig)
        return canvas


class Apper_graph:
    """### Classe para criar um gráfico genérico"""

    def __init__(self, dados:list, titulo:str, caption_label:str="", xlabel:str="Tempo", ylabel:str="Amplitude", step:bool=True, resolucao:int=1):
        """### Classe para criar um gráfico genérico 
        ---
        Exemplo de uso: Apper_graph([], "Sinal ASK", "Sinal ASK", "Tempo", "Amplitude", step=false)"""

        self.dados = dados
        self.titulo = titulo
        self.caption_label = caption_label
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.step = step
        self.resolucao = resolucao
        self.apper_graph()

    def apper_graph(self) -> FigureCanvas:
        """Usando as opções do construtor cria um novo FigureCanvas"""

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        t = np.arange(0,len(self.dados)/self.resolucao,1/self.resolucao)

        # Plotando o sinal
        if self.step == False:
            ax.plot(t, self.dados, label=self.caption_label, linewidth=2)
        else:
            ax.step(t, self.dados, where='post', label=self.caption_label, linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title(self.titulo)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)

        canvas = FigureCanvas(fig)
        return canvas