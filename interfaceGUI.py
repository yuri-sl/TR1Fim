import math
import gi
import threading
gi.require_version("Gtk", "3.0")
from Simulador import start_server
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

        #Server Status Label
        self.server_status_label = Gtk.Label(label="Server Status: Stopped")
        self.server_status_label.set_halign(Gtk.Align.CENTER)
        self.grid.attach(self.server_status_label,0,5,2,1)

        #Start Server  Btn
        btn_start_server = Gtk.Button(label="Iniciar Servidor do Receptor")
        btn_start_server.set_halign(Gtk.Align.CENTER)
        btn_start_server.connect("clicked",start_server)
        btn_start_server.get_style_context().add_class("grid-button")
        self.grid.attach(btn_start_server,0,4,1,1)
        
        # TextView for Logs
        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textbuffer = self.textview.get_buffer()
        self.grid.attach(self.textview,0,6,4,2)

        
        self.server_running = False
        self.server_thread = None


        


        # Criação da instância da menu_suspenso (do arquivo menu_suspenso.py)
        self.menu = MenuSuspenso(self)
        self.menu.set_halign(Gtk.Align.CENTER)
        self.grid.attach(self.menu, 0, 3, 2, 1)


        self.label_added = False  # Control flag for adding label
        self.maximize()
        self.grid.show_all()   


    def log_message(self, message):
        # Add log messages to the TextView
        def update_textbuffer():
            end_iter = self.textbuffer.get_end_iter()
            self.textbuffer.insert(end_iter, message + "\n")
            return False  # Returning False stops the idle_add
        GLib.idle_add(update_textbuffer)

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
        palavra = self.entry_window.get_text()
        binarios = []
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.extend(list(valor_binario))
    
        ask = []
        tempo = 0
        resolucao = 50
        frequencia = 1
        for i in binarios:
            if i == '0':
                ask.extend([0 for a in range(resolucao)])
                tempo += resolucao
            else:
                for j in range(resolucao):
                   ask.append(math.cos(2*math.pi*frequencia*tempo)) 
                   tempo += 1/resolucao

        canvas = Apper_graph(ask, "Sinal ASK", step=False, resolucao=resolucao).apper_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)

        self.grid.attach(canvas, 0,4,8,8)
        self.show_all()

        return None

    def graph_FSK(self):
        palavra = self.entry_window.get_text()
        binarios = []
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.extend(list(valor_binario))
    
        fsk = []
        tempo = 0
        resolucao = 50
        frequencia = 1
        for i in binarios:
            if i == '0':
                for j in range(resolucao):
                   fsk.append(math.cos(2*math.pi*frequencia*tempo)) 
                   tempo += 1/resolucao
            else:
                for j in range(resolucao):
                   fsk.append(math.cos(4*math.pi*frequencia*tempo)) 
                   tempo += 1/resolucao

        canvas = Apper_graph(fsk, "Sinal FSK", step=False, resolucao=resolucao).apper_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)

        self.grid.attach(canvas, 0,4,8,8)
        self.show_all()
        return None
    
    def graph_8QAM(self):
        palavra = self.entry_window.get_text()
        binarios = []
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.extend(list(valor_binario))

        # faz com que a lista de binarios tenha um numero de elementos divisiveis por 3, colocando zeros no final caso não tenha
        binarios.extend(['0' for a in range(3-len(binarios)%3) if len(binarios)%3 != 0]) 

        qam = []
        tempo = 0
        resolucao = 50
        frequencia = 1
        for i in range(0,len(binarios),3):
            trio = binarios[i:i+3]
            aq = 0;ai = 0
            # associando cada trio de bits a um simbolo eletrico
            # a constelação aqui está baseada em https://weibeld.net/mobcom/psk-qam-modulation.html
            # valores em raiz(2)/2 para manter a amplitude 
            match trio:
                case ['0','0','0']: 
                    ai = -math.sqrt(2)/2
                    aq = -math.sqrt(2)/2
                case ['0','0','1']: 
                    ai = -math.sqrt(2)/2
                    aq = 0
                case ['0','1','0']: 
                    ai = 0
                    aq = math.sqrt(2)/2
                case ['0','1','1']: 
                    ai = -math.sqrt(2)/2
                    aq = math.sqrt(2)/2
                case ['1','0','0']: 
                    ai = -math.sqrt(2)/2
                    aq = 0
                case ['1','0','1']: 
                    ai = math.sqrt(2)/2
                    aq = -math.sqrt(2)/2
                case ['1','1','0']: 
                    ai = math.sqrt(2)/2
                    aq = math.sqrt(2)/2
                case ['1','1','1']: 
                    ai = math.sqrt(2)/2
                    aq = 0

            for i in range(resolucao):
                fase = math.atan2(aq,ai)
                qam.append(math.sqrt(ai*ai+aq*aq)*math.cos(2*math.pi*frequencia*tempo + fase)) 
                tempo += 1/resolucao


        canvas = Apper_graph(qam, "Sinal QAM", step=False, resolucao=resolucao).apper_graph()
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)

        self.grid.attach(canvas, 0,4,8,8)
        self.show_all()
        return None
        
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
