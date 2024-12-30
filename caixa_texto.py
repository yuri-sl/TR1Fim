import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class EntryWindow(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Criação da entrada de texto
        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")  # Texto inicial
        self.pack_start(self.entry, True, True, 0)

    def get_text(self):
        # Método para obter o texto da entrada
        return self.entry.get_text()
    