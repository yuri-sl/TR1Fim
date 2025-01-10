import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from camadaFisica import *





class MenuSuspenso(Gtk.Box):
    def __init__(self, main_window):  # Recebe a referência para a classe principal
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        self.main_window = main_window  # Armazena a referência da classe principal

        self.menu_suspenso = Gtk.ComboBoxText()

        # Adicionando itens ao combo box
        graficos = [
            "Gráfico NRZ",
            "Gráfico Bipolar",
            "Gráfico Manchester",
            "Gráfico ASK",
            "Gráfico FSK",
            "Gráfico 8-QAM"
        ]
        for graphs in graficos:
            self.menu_suspenso.append_text(graphs)

        #Quando um evento acontecer 
        self.menu_suspenso.connect("changed", self.grafico_escolhido)
        self.pack_start(self.menu_suspenso, False, False, 0)

    def grafico_escolhido(self, widget):
        grafico = self.menu_suspenso.get_active_text()
        print(f"Você escolheu: {grafico}")
        # Chama os métodos da classe principal com base no texto selecionado
        if grafico == "Gráfico NRZ":
            self.main_window.graph_NRZ()
        elif grafico == "Gráfico Bipolar":
            self.main_window.graph_Bipolar()
        elif grafico == "Gráfico Manchester":
            self.main_window.graph_Manchester()
        elif grafico == "Gráfico ASK":
            self.main_window.graph_ASK()
        elif grafico == "Gráfico FSK":
            self.main_window.graph_FSK()
        elif grafico == "Gráfico 8-QAM":
            self.main_window.graph_8QAM()
        return grafico

class EntryWindow(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Criação da entrada de texto
        self.entry = Gtk.Entry()
        self.entry.set_text("a")  # Texto inicial
        self.pack_start(self.entry, True, True, 0)

    def get_text(self):
        # Método para obter o texto da entrada
        return self.entry.get_text()

    def get_text(self):
        # Método para obter o texto da entrada
        return self.entry.get_text()
    
 
class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulador transmissores e receptores")
        self.set_border_width(10)
        self.set_default_size(500,400)

        self.setup_css()


        # Create a grid layout
        self.grid = Gtk.Grid()
        self.grid.set_hexpand(True)
        self.grid.set_vexpand(True)
        self.grid.set_row_spacing(20)   #Espaçamento entre linhas
        self.grid.set_column_spacing(20) #Espaçamento entre colunas
        self.grid.get_style_context().add_class("grid") #Classe CSS


        self.grid.set_halign(Gtk.Align.CENTER)
        
        self.add(self.grid)

        #LabelWelcome
        lblWelcomeTxt = Gtk.Label(label="Bem-vindo ao simulador transmissor!")
        lblWelcomeTxt.get_style_context().add_class("primary-label")
        lblWelcomeTxt.set_halign(Gtk.Align.CENTER)
        self.grid.attach(lblWelcomeTxt,0,0,2,1)

        #BtnCloseApp

        # Criação da instância da EntryWindow (do arquivo caixa_texto.py)
        self.entry_window = EntryWindow()
        self.entry_window.set_halign(Gtk.Align.CENTER)
        self.grid.attach(self.entry_window, 1, 1, 1, 1)


        # Button para aparecer a palavra em binario
        button_add_graph = Gtk.Button(label="Palavra em bin")
        button_add_graph.set_halign(Gtk.Align.CENTER)
        button_add_graph.connect("clicked", self.apper_WordToBin)
        button_add_graph.get_style_context().add_class("grid-button") #Classe CSS
        self.grid.attach(button_add_graph, 0, 2, 1, 1) #Coluna 1 linha 0 ocupando 1x1

        # Primary Label
        self.label = Gtk.Label(label="Irá aparecer o texto em binario aqui")
        self.label.get_style_context().add_class("primary-label") #Add Classe CSS
        self.label.set_halign(Gtk.Align.CENTER)
        self.grid.attach(self.label, 1, 2, 1, 1) #Coluna 0 linha 2 ocupando 2x1

        #Transmitir para o Receptor
        button_submit = Gtk.Button(label="Transmitir mensagem codificada")
        self.grid.attach(button_submit,4,3,1,1)



        # Criação da instância da menu_suspenso (do arquivo menu_suspenso.py)
        self.menu = MenuSuspenso(self)
        self.menu.set_halign(Gtk.Align.CENTER)
        self.grid.attach(self.menu, 0, 3, 2, 1)


        self.label_added = False  # Control flag for adding label
        self.maximize()
        self.grid.show_all()   

    def closeApp(self,button):
        Gtk.main_quit()      

    #Aparece a palavra em binário
    def apper_WordToBin(self, widget):
        palavra = self.entry_window.get_text()
        binarios = converterBinario(palavra)
        self.label.set_text(f"{binarios} = {palavra} em bin")

    def graph_NRZ(self):
        palavra = self.entry_window.get_text()
        binarios = [] 
        for char in palavra:
            valor_binario = format(ord(char), '08b')  # Converte o caractere para binário de 8 bits
            binarios.extend(list(valor_binario))  # Quebra a string binária em uma lista de caracteres e adiciona à lista binarios
        # Agora, binarios conterá todos os bits individuais como 0 e 1
        binarios = [int(bit) for bit in binarios]
        for i in range(len(binarios)):
            if binarios[i] == 0:
                binarios[i] = -1
        binarios.append(binarios[-1])

        canvas = Apper_graph_nrz(binarios).apper_new_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)
        # Adiciona o gráfico ao grid na posição especificada
        self.grid.attach(canvas, 0, 4, 8, 8)  # Coluna 4, linha 4, ocupando 2x2 células
        self.show_all()



    def graph_Bipolar(self):
        palavra = self.entry_window.get_text()
        binarios = []
        count_ones = 0 # Parametro para contar a alternancia entre  +- V
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.extend(list(valor_binario))
        binarios = [int(bit) for bit in binarios]
        for i in range(len(binarios)):
            if binarios[i] == 0:
                binarios[i] = 0
            if binarios[i] == 1:
                if count_ones %2 == 0:
                    binarios[i] = 1
                    count_ones += 1
                else:
                    binarios[i] = -1
                    count_ones += 1
        binarios.append(binarios[-1])

        canvas = Apper_graph_bipolar(binarios).apper_new_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)
        self.grid.attach(canvas, 0, 4, 8, 8)
        self.show_all()

    def graph_Manchester(self):
        palavra = self.entry_window.get_text()
        binarios = []
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.extend(list(valor_binario))

        manchester = []

        for i in binarios:
            if i == '0':
                manchester.extend([0,1])
            else:
                manchester.extend([1,0])
        
        manchester = [int(bit) for bit in manchester]

        canvas = Apper_graph_manchester(manchester).apper_new_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)

        self.grid.attach(canvas, 0,4,8,8)
        self.show_all()


    def graph_ASK(self):
        a = [1, 2, 3, 4]
        b = [0, 4, 9, 16]
        Apper_graph_ask(a,b)
    def graph_FSK(self):
        a = [1, 2, 3, 4]
        b = [0, 4, 9, 16]
        Apper_graph_fsk(a,b)
    def graph_8QAM(self):
        a = [1, 2, 3, 4]
        b = [0, 4, 9, 16]
        Apper_graph_8qam(a,b)
        
    def setup_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        
        #Add o CSS ao contexto padrão
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
