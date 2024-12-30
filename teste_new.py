import gi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure
from caixa_texto import EntryWindow
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
        def new_a_and_b(button):  # Recebe o botão como argumento
            global a, b  # Usa as variáveis "globais"
            a = [1, 2, 3, 4, 5]
            b = [0, 4, 9, 16, 25]
            ax.clear()
            ax.plot(a, 'ro-', label='easy as 1 2 3')
            ax.plot(b, 'gs--', label='easy as 1 2 3 squared')
            ax.legend()
            fig.canvas.draw() 

        fig, ax = plt.subplots()
        ax.plot(a, 'ro-', label='easy as 1 2 3')
        ax.plot(b, 'gs--', label='easy as 1 2 3 squared')
        ax.legend()

        # you can access the window or vbox attributes this way
        manager = fig.canvas.manager
        toolbar = manager.toolbar
        vbox = manager.vbox


        # now let's add a button to the toolbar

        button1 = Gtk.Button(label='Click me 1')
        button1.show()
        button1.connect('clicked', lambda button: print('hi mom!!!'))


        toolitem1 = Gtk.ToolItem()
        toolitem1.show()
        toolitem1.set_tooltip_text('Click me for fun and profit')
        toolitem1.add(button1)

        pos1 = 11  # where to insert this in the toolbar
        toolbar.insert(toolitem1, pos1)

        button2 = Gtk.Button(label='Click me 2')
        button2.show()
        button2.connect('clicked', new_a_and_b,)


        toolitem2 = Gtk.ToolItem()
        toolitem2.show()
        toolitem2.set_tooltip_text('Click meeeeeee for fun and profit')
        toolitem2.add(button2)


        pos2 = 9  # where to insert this in the toolbar
        toolbar.insert(toolitem2, pos2)

        # now let's add a widget to the vbox
        label = Gtk.Label()
        label.set_markup('Drag mouse over axes for position')
        label.show()
        vbox.pack_start(label, False, False, 0)
        vbox.reorder_child(toolbar, -1)

        def update(event):
            if event.xdata is None:
                label.set_markup('Drag mouse over axes for position')
            else:
                label.set_markup(
                    f'<span color="#ef0000">x,y=({event.xdata}, {event.ydata})</span>')
        fig.canvas.mpl_connect('motion_notify_event', update)
        plt.show()
    
window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()