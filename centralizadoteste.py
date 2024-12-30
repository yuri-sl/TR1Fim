import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class CentralizarElementosComGrid(Gtk.Window):
    def __init__(self):
        super().__init__(title="Centralizar Elementos com Grid")
        self.set_default_size(400, 300)

        # Cria o grid
        grid = Gtk.Grid()
        grid.set_halign(Gtk.Align.CENTER)  # Centraliza horizontalmente
        grid.set_valign(Gtk.Align.CENTER)  # Centraliza verticalmente
        self.add(grid)

        # Adiciona widgets ao grid
        label = Gtk.Label(label="Este é um texto centralizado.")
        grid.attach(label, 0, 0, 1, 1)  # (widget, coluna, linha, colspan, rowspan)

        button = Gtk.Button(label="Botão Centralizado")
        grid.attach(button, 0, 1, 1, 1)

# Inicia o aplicativo GTK
if __name__ == "__main__":
    app = CentralizarElementosComGrid()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
