import gi
import numpy as np

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