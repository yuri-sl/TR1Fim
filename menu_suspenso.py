import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
