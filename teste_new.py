import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


from caixa_texto import EntryWindow
from graficos import Apper_graph

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulador transmissores e receptores")
        self.set_border_width(10)

        # Create a grid layout
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        # Criação da instância da EntryWindow (do arquivo caixa_texto.py)
        self.entry_window = EntryWindow()
        self.grid.attach(self.entry_window, 0, 0, 1, 1)

        # Button to trigger graph display
        button_add_graph = Gtk.Button(label="Adicione o gráfico aqui!/python bin")
        button_add_graph.connect("clicked", self.apper_new_graph)
        self.grid.attach(button_add_graph, 0, 1, 1, 1)

        # Button para aparecer a palavra em binario
        button_add_graph = Gtk.Button(label="Palavra em bin")
        button_add_graph.connect("clicked", self.apper_WordToBin)
        self.grid.attach(button_add_graph, 1, 0, 1, 1)

        # Atualiza Button
        button_new_graph = Gtk.Button(label="palavra em arabico")
        button_new_graph.connect("clicked", self.display_Word)
        self.grid.attach(button_new_graph, 1, 1, 1, 1)

        # Primary Label
        self.label = Gtk.Label(label="Irá aparecer o texto em binario aqui")
        self.label.set_halign(Gtk.Align.END)
        self.grid.attach(self.label, 0, 2, 2, 1)

        # Secondary Label (to be dynamically added)
        self.labelTeste = Gtk.Label(label="PYTHON!!!")
        self.labelTeste.set_halign(Gtk.Align.CENTER)

        self.label_added = False  # Control flag for adding label

        self.maximize()

    def apper_WordToBin(self, widget):
        palavra = self.entry_window.get_text()
        binarios = []  
        for char in palavra:
            valor_binario = format(ord(char), '08b')
            binarios.append(valor_binario)  # Adiciona o valor binário à lista
        self.label.set_text(f"{binarios} = {palavra} em bin")
    #da pra usar em alguma coisa ainda
    def display_Word(self, widget):
        button_clicked = widget.get_label()
        if not self.label_added:  # Check if the label has already been added
            self.grid.attach(self.labelTeste, 0, 3, 2, 1)
            self.label_added = True
            self.show_all()  # Refresh the interface to display the new label

        if button_clicked == "TunaButton":
            print("Você clicou no python em forma arabica")
            self.label.set_text("Graph: python")
        else:
            print(f"Você clicou no python bin ")
            self.label.set_text("Graph: graph")
    
    def apper_new_graph(self, widget):
        a = [1, 2, 3, 4]
        b = [0, 4, 9, 16]
        Apper_graph(a,b)
    
window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()