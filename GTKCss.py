import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class EstilizarFundo(Gtk.Window):
    def __init__(self):
        super().__init__(title="Estilizar Fundo")
        self.set_default_size(400, 300)

        # Aplica um ID ao widget
        self.set_name("minha-janela")

        # Configura o CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            #minha-janela {
                background: linear-gradient(to right, #ff7e5f, #feb47b);
            }
        """)

        # Conecta o CSS ao estilo da aplicação
        style_context = self.get_style_context()
        style_context.add_provider(
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Adiciona um conteúdo como exemplo
        label = Gtk.Label(label="Este é um fundo estilizado.")
        self.add(label)

# Inicia o aplicativo GTK
if __name__ == "__main__":
    app = EstilizarFundo()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
