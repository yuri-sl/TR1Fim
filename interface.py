import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class SimulatorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulador transmissores e receptores")
        self.set_border_width(10)

        grid = Gtk.Grid()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.entry = Gtk.Entry()

        button_submit = Gtk.Button(label="Submit Message")
        label_welcome = Gtk.Label(label="Bem vindo ao simulador InfraWeb!")

        grid.add(self.entry)
        grid.attach(label_welcome, 0,1,2,1)
        grid.attach(button_submit, 2,1,2,1)

        self.add(grid)
        self.maximize()




window = SimulatorWindow()
window.connect("destroy",Gtk.main_quit)
window.show_all()
Gtk.main()