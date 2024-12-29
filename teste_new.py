import gi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulador transmissores e receptores")
        self.set_border_width(10)

        # Create a grid layout
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Button to trigger graph display
        button_add_graph = Gtk.Button(label="Adicione o gráfico aqui!")
        button_add_graph.connect("clicked", self.apper_new_graph)
        self.grid.add(button_add_graph)

        # Atualiza Button
        button_new_graph = Gtk.Button(label="Mudar de gráfico")
        button_new_graph.connect("clicked", self.display_graph)
        self.grid.attach(button_new_graph, 1, 0, 1, 1)

        # Primary Label
        self.label = Gtk.Label(label="Isso é um teste de label")
        self.label.set_halign(Gtk.Align.END)
        self.grid.attach(self.label, 0, 1, 2, 1)

        # Secondary Label (to be dynamically added)
        self.labelTeste = Gtk.Label(label="Label Teste adicionada!")
        self.labelTeste.set_halign(Gtk.Align.CENTER)

        # Placeholder for Matplotlib graph
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvas(self.figure)
        self.grid.attach(self.canvas, 0, 2, 2, 1)

        self.label_added = False  # Control flag for adding label

        self.maximize()

    def display_graph(self, widget):
        button_clicked = widget.get_label()
        if not self.label_added:  # Check if the label has already been added
            self.grid.attach(self.labelTeste, 0, 3, 2, 1)
            self.label_added = True
            self.show_all()  # Refresh the interface to display the new label

        if button_clicked == "TunaButton":
            print("Você clicou no Tuna")
            self.label.set_text("Graph: Tuna")
            self.update_graph([1, 2, 3], [1, 4, 9])
        else:
            print("Você clicou no outro")
            self.label.set_text("Graph: Other")
            self.update_graph([1, 2, 3, 4], [2, 3, 5, 7])

    def update_graph(self, x, y):
        # Clear previous graph
        self.ax.clear()
        self.ax.plot(x, y, label="Updated Graph")
        self.ax.legend()
        self.canvas.draw()
    
    def apper_new_graph(self, widget):
        a = [1, 2, 3, 4]
        b = [0, 4, 9, 16]

        def new_a_and_b(button):  # Recebe o botão como argumento
            global a, b  # Usa as variáveis globais
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
        toolbar1 = manager.toolbar
        vbox = manager.vbox


        # now let's add a button to the toolbar

        button1 = Gtk.Button(label='Click me2')
        button1.show()
        button1.connect('clicked', lambda button: print('hi mom!!!'))


        toolitem1 = Gtk.ToolItem()
        toolitem1.show()
        toolitem1.set_tooltip_text('Click me for fun and profit')
        toolitem1.add(button1)

        pos1 = 9  # where to insert this in the toolbar
        toolbar.insert(toolitem1, pos1)

        button2 = Gtk.Button(label='Click me3')
        button2.show()
        button2.connect('clicked', new_a_and_b,)


        toolitem2 = Gtk.ToolItem()
        toolitem2.show()
        toolitem2.set_tooltip_text('Click meeeeeee for fun and profit')
        toolitem2.add(button2)


        pos2 = 3  # where to insert this in the toolbar
        toolbar1.insert(toolitem2, pos2)

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
