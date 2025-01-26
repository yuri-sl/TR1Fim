import matplotlib                           # Biblioteca para plotar os graficos

matplotlib.use('GTK3Agg')  # Usar 'GTK3Agg' para renderizar com GTK e Matplotlib

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,Gdk           # Repositorio da GUI GTK

def addCSS():
        #Load CSS from file
        css_provider = Gtk.CssProvider()    # Cria uma instância de `Gtk.CssProvider`.
        css_provider.load_from_path("styles.css") # Carrega os estilos do arquivo `styles.css` para o `CssProvider`.
        Gtk.StyleContext.add_provider_for_screen( 
            Gdk.Screen.get_default(),css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        ) # Aplica o provedor de estilos (`css_provider`) ao contexto global da tela padrão utilizando `Gdk.Screen.get_default()`.



class serverStartedWindow(Gtk.Window):
    def okayBtn(self, widget):  # Oculta a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Servidor iniciado com sucesso!")  # Define o título da janela
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela

        lblSuccMsg = Gtk.Label(label="Servidor Iniciado com sucesso")  # Cria um label com a mensagem de sucesso
        lblDoorMsg = Gtk.Label(label="Endereço: Localhost. Porta: 8030")  # Cria um label com o endereço e porta

        btnOk = Gtk.Button()  # Cria o botão "Ok"
        lblOk = Gtk.Label(label="Ok")  # Cria o label para o botão "Ok"
        btnOk.add(lblOk)  # Adiciona o label ao botão
        btnOk.connect("clicked", self.okayBtn)  # Conecta o clique do botão à função okayBtn

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Cria um container vertical com espaçamento
        vbox.set_name("box-container")  # Define o nome para o container (útil para estilização)
        vbox.pack_start(lblSuccMsg, True, True, 0)  # Adiciona o label de sucesso ao container
        vbox.pack_start(lblDoorMsg, True, True, 0)  # Adiciona o label de endereço ao container
        vbox.pack_start(btnOk, True, True, 0)  # Adiciona o botão "Ok" ao container

        self.add(vbox)  # Adiciona o container à janela
        self.connect("destroy", self.hide)  # Conecta o evento de fechamento da janela à função hide

        addCSS()  # Aplica o estilo CSS à janela

class serverEndedWindow(Gtk.Window):
    def okayBtn(self, widget):  # Oculta a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Encerrar o servidor")  # Define o título da janela
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela

        lblSuccMsg = Gtk.Label(label="Você acabou de fechar o servidor")  # Cria um label com a mensagem de encerramento
        btnOk = Gtk.Button()  # Cria o botão "Ok"
        lblOk = Gtk.Label(label="Ok")  # Cria o label para o botão "Ok"
        btnOk.add(lblOk)  # Adiciona o label ao botão
        btnOk.connect("clicked", self.okayBtn)  # Conecta o clique do botão à função okayBtn

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Cria um container vertical com espaçamento
        vbox.set_name("box-container")  # Define o nome para o container (útil para estilização)
        vbox.pack_start(lblSuccMsg, True, True, 0)  # Adiciona o label de mensagem ao container
        vbox.pack_start(btnOk, True, True, 0)  # Adiciona o botão "Ok" ao container

        self.add(vbox)  # Adiciona o container à janela
        self.connect("destroy", self.hide)  # Conecta o evento de fechamento da janela à função hide

        addCSS()  # Aplica o estilo CSS à janela

class noSignal(Gtk.Window):
    def okayBtn(self, widget):  # Função para esconder a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Erro")  # Define o título da janela de erro
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela (largura x altura)

        wndwLabel = Gtk.Label(label="Nenhum sinal foi recebido ainda")  # Cria um label com a mensagem de erro

        addCSS()  # Aplica o estilo CSS à janela

        btnOk = Gtk.Button()  # Cria o botão "Ok"
        lblOk = Gtk.Label(label="Ok")  # Cria o label "Ok" para o botão
        btnOk.add(lblOk)  # Adiciona o label ao botão
        btnOk.connect("clicked", self.okayBtn)  # Conecta o clique do botão à função que oculta a janela

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Cria um container vertical com espaçamento
        vbox.set_name("box-container")  # Define o nome para o container (útil para estilização com CSS)
        vbox.pack_start(wndwLabel, True, True, 0)  # Adiciona o label de erro ao container
        vbox.pack_start(btnOk, True, True, 0)  # Adiciona o botão "Ok" ao container

        self.add(vbox)  # Adiciona o container à janela

        self.connect("destroy", self.hide)  # Conecta o evento de fechamento da janela à função hide
