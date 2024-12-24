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
        grid = Gtk.Grid()
        self.add(grid)

        # Button to trigger graph display
        teste_button = Gtk.Button(label="Click here!")
        teste_button.connect("clicked", self.display_graph)
        grid.add(teste_button)

        # Tuna Button
        tuna_button = Gtk.Button(label="TunaButton")
        tuna_button.connect("clicked", self.display_graph)
        grid.attach(tuna_button, 1, 0, 1, 1)

        # Label
        label = Gtk.Label(label="Isso é um teste de label")
        label.set_halign(Gtk.Align.END)
        grid.attach(label, 0, 1, 2, 1)

        # Placeholder for Matplotlib graph
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvas(self.figure)
        grid.attach(self.canvas, 0, 2, 2, 1)

    def display_graph(self, widget):
        botaoClicado = widget.get_label()
        if botaoClicado == "TunaButton":
            print("Você clicou no Tuna")
            self.update_graph([1, 2, 3], [1, 4, 9])
        else:
            print("Você clicou no outro")
            self.update_graph([1, 2, 3, 4], [2, 3, 5, 7])

    def update_graph(self, x, y):
        # Clear previous graph
        self.ax.clear()
        self.ax.plot(x, y, label="Updated Graph")
        self.ax.legend()
        self.canvas.draw()


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
