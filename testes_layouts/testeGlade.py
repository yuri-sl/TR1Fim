import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GladeApp(Gtk.Window):
    def __init__(self):
        super().__init__()

        # Carrega o arquivo .glade
        builder = Gtk.Builder()
        builder.add_from_file("teste.glade")

        # Obtém a janela principal do arquivo
        self.window = builder.get_object("main_window")
        if not self.window:
            print("Erro: Não foi possível encontrar 'main_window' no arquivo Glade.")
            exit(1)

        # Conecta sinais definidos no Glade
        builder.connect_signals(self)

        # Mostra a janela
        self.window.show_all()

    def on_button_clicked(self, button):
        print(f"Botão '{button.get_label()}' clicado!")


# Inicializa a aplicação
app = GladeApp()
Gtk.main()
