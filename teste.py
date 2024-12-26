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
        test_button = Gtk.Button(label="Click here!")
        test_button.connect("clicked", self.display_graph)
        self.grid.add(test_button)

        # Tuna Button
        tuna_button = Gtk.Button(label="TunaButton")
        tuna_button.connect("clicked", self.display_graph)
        self.grid.attach(tuna_button, 1, 0, 1, 1)

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


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
