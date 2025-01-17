import matplotlib
matplotlib.use('GTK3Agg')  # Usar 'GTK3Agg' para renderizar com GTK e Matplotlib

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,Gdk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from camadaFisica import *
from camadaEnlace import *



servidorAtivo = False
entryBoxPreenchida = False

def addCSS():
        #Load CSS from file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class erroEnviarMensagem(Gtk.Window):
    def okayBtn(self,widget):
        self.hide()
    def __init__(self):
        super().__init__(title="Erro ao enviar a mensagem")
        self.set_default_size(200,100)
        lblErroMsg = Gtk.Label(label="Servidor não foi iniciado!")

        addCSS()

        btnOk = Gtk.Button()
        lblOk = Gtk.Label(label="Ok")
        btnOk.add(lblOk)
        btnOk.connect("clicked",self.okayBtn)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        vbox.set_name("box-container")
        vbox.pack_start(lblErroMsg,True,True,0)
        vbox.pack_start(btnOk,True,True,0)
        self.add(vbox)
        self.connect("destroy",self.hide)

class mensagemEnviada(Gtk.Window):
    def okayBtn(self,widget):
        self.hide()
    def __init__(self):
        super().__init__(title="Mensagem Enviada!")
        self.set_default_size(200,100)
        wndwLabel = Gtk.Label(label="Mensagem foi enviada com sucesso!")

        addCSS()

        btnOk = Gtk.Button()
        lblOk = Gtk.Label(label="Ok")
        btnOk.add(lblOk)
        btnOk.connect("clicked",self.okayBtn)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        vbox.set_name("box-container")
        vbox.pack_start(wndwLabel,True,True,0)
        vbox.pack_start(btnOk,True,True,0)


        self.add(vbox)


        self.connect("destroy",self.hide)


class textoVazio(Gtk.Window):
    def okayBtn(self,widget):
        self.hide()
    def __init__(self):
        super().__init__(title="Erro")
        self.set_default_size(200,100)
        wndwLabel = Gtk.Label(label="O campo de mensagem está vazio")

        addCSS()

        btnOk = Gtk.Button()
        lblOk = Gtk.Label(label="Ok")
        btnOk.add(lblOk)
        btnOk.connect("clicked",self.okayBtn)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        vbox.set_name("box-container")
        vbox.pack_start(wndwLabel,True,True,0)
        vbox.pack_start(btnOk,True,True,0)


        self.add(vbox)


        self.connect("destroy",self.hide)


class MyWindow(Gtk.Window):
    def show_graph(self, x_data, y_data, title, label):
        # Criação de uma nova janela GTK para o gráfico
        graph_window = Gtk.Window(title=title)
        graph_window.set_default_size(800, 600)

        # Criando a figura do Matplotlib
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, label=label)
        ax.set_title(title)
        ax.legend()

        # Incorporando a figura no GTK
        canvas = FigureCanvas(fig)

        graph_window.add(canvas)

        # Exibindo a janela do gráfico
        graph_window.show_all()

    # Connect the Dropdown Signal
    def on_combo_changed(self,widget):
        selected = widget.get_active_text()

        msgSize = self.entryMessage.get_text_length()
        if msgSize == 0:
            entryBoxPreenchida = False
            janelaVazio = textoVazio()
            janelaVazio.show_all()
        else:
            entryBoxPreenchida = True

        if entryBoxPreenchida == True:
            if selected == "Grafico NRZ":
                self.show_graph([0, 1, 2, 3], [0, 1, 4, 9], "Grafico NRZ", "Sinal NRZ")

            elif selected == "Grafico Manchester":
                self.show_graph([0, 1, 2, 3], [0, 1, 8, 27], "Gráfico Manchester", "Sinal Manchester")
            elif selected == "Grafico Bipolar":
                self.show_graph([0, 1, 2, 3], [0, 1, 4, 9], "Gráfico Bipolar", "Sinal Bipolar")
            elif selected == "Gráfico ASK":
                self.show_graph([0, 1, 2, 3], [0, 1, 4, 9], "Gráfico ASK", "Sinal ASK")
            elif selected == "Gráfico FSK":
                self.show_graph([0, 1, 2, 3], [0, 1, 4, 9], "Gráfico FSK", "Sinal FSK")
            elif selected == "Gráfico 8-QM":
                self.show_graph([0, 1, 2, 3], [0, 1, 4, 9], "Gráfico 8-QM", "Sinal 8-QM")                
    
    def on_button_clicked(self, widget):
        # Create the pop-up window
        if servidorAtivo == False:
            popup = erroEnviarMensagem()
            popup.show_all()
        else:
            popup = mensagemEnviada()
            popup.show_all()



    def __init__(self):

        super().__init__(title="Simulador SimulNet")

        #Load CSS from file
        addCSS()


        notebook = Gtk.Notebook()
        self.add(notebook)




        #Criação da página do Transmissor
        page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=20)
        page1.set_border_width(10)
        page1.set_name("box-container")

        ##Formatação de Estilos para as abas do Notebook
        tab_label_Transmissor = Gtk.Label(label="Transmissor")
        tab_label_Transmissor.set_name("transmissor-tab")
        notebook.append_page(page1,tab_label_Transmissor)
        #Introdução
        lblWelcome = Gtk.Label(label="SimulNet")
        lblInsertText = Gtk.Label(label="Insira a mensagem")
        lblInsertText.get_style_context().add_class("label-small")

        lblWelcome.set_margin_end(20)
        lblWelcome.get_style_context().add_class("lblTitle")

        # Torne `entryMessage` um atributo da classe
        self.entryMessage = Gtk.Entry()
        self.entryMessage.get_style_context().add_class("entry")
        lblInputText = Gtk.Label(label="Insira a mensagem a ser transmitida")
        self.entryMessage.set_placeholder_text(lblInputText.get_text())

        ##MODULAÇÃO DIGITAL
        lblModDig = Gtk.Label(label="Modulação Digital")
        lblModDig.get_style_context().add_class("lblSection")

        #Criação do dropdown Menu
        comboMod = Gtk.ComboBoxText()
        comboMod.append_text("Selecione um gráfico")
        comboMod.set_active(0)

        graficosDig = [
            "Grafico NRZ",
            "Grafico Manchester",
            "Grafico Bipolar"
        ]
        
        for graph in graficosDig:
            comboMod.append_text(graph)
        
        comboMod.connect("changed", self.on_combo_changed)



        
        #Criação de box horizontais para inserir os radios buttons
        hboxModDig = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing= 10)
        hboxModDig.set_halign(Gtk.Align.CENTER)

        rdNRZ_modDig = Gtk.RadioButton.new_with_label_from_widget(None,"NRZ")
        rdMCH_modDig = Gtk.RadioButton.new_with_label_from_widget(rdNRZ_modDig,"Manchester")
        rdBIP_modDig = Gtk.RadioButton.new_with_label_from_widget(rdNRZ_modDig,"Bipolar")

        hboxModDig.pack_start(rdNRZ_modDig, False,False, 0)
        hboxModDig.pack_start(rdMCH_modDig, False,False, 0)
        hboxModDig.pack_start(rdBIP_modDig, False,False, 0)

        ##MODULAÇÃO POR PORTADORA
        lblModPort = Gtk.Label(label="Modulação por Portadora")
        lblModPort.get_style_context().add_class("lblSection")

        comboPort = Gtk.ComboBoxText()
        comboPort.append_text("Selecione um gráfico de portadora")
        comboPort.set_active(0)

        graficosPort = [
            "Gráfico ASK",
            "Gráfico FSK",
            "Gráfico 8-QM"
        ]
        for graphs in graficosPort:
            comboPort.append_text(graphs)

        comboPort.connect("changed", self.on_combo_changed)

        
        ##Enquadramento
        lblEnq = Gtk.Label(label="Enquadramento")
        lblEnq.get_style_context().add_class("lblSection")


        hboxEnq = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxEnq.set_halign(Gtk.Align.CENTER)
        rdCharCount = Gtk.RadioButton.new_with_label_from_widget(None,"Contagem de Caracteres")
        rdInsByte = Gtk.RadioButton.new_with_label_from_widget(rdCharCount,"Inserção de Bytes")

        hboxEnq.pack_start(rdCharCount, False, False, 0)
        hboxEnq.pack_start(rdInsByte, False, False, 0)

        ##Detecção de Erros
        lblDtError = Gtk.Label(label="Detecção de erros")
        lblDtError.get_style_context().add_class("lblSection")


        hboxDtError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxDtError.set_halign(Gtk.Align.CENTER)
        rdParity = Gtk.RadioButton.new_with_label_from_widget(None,"Paridade par")
        rdCRC = Gtk.RadioButton.new_with_label_from_widget(rdParity,"CRC")

        hboxDtError.pack_start(rdParity,False,False,0)
        hboxDtError.pack_start(rdCRC,False,False,0)


        ##Correção de Erros
        lblCorrError = Gtk.Label(label="Correção de erros")
        lblCorrError.get_style_context().add_class("lblSection")


        hboxCorrError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxCorrError.set_halign(Gtk.Align.CENTER)
        rdHamming = Gtk.RadioButton.new_with_label_from_widget(None,"Hamming")
        
        hboxCorrError.pack_start(rdHamming,False,False,0)

        ##TransmitMessage
        lblWarning = Gtk.Label(label="Obs.: 0,011% de chance de ocorrência de erros")
        lblWarning.set_name("warning")


        lblTransmitMessage = Gtk.Label(label="Transmitir Mensagem")
        lblTransmitMessage.get_style_context().add_class("btnLbl")
        btnTransmitMessage = Gtk.Button()
        btnTransmitMessage.add(lblTransmitMessage)
        btnTransmitMessage.connect("clicked",self.on_button_clicked)




        #Adição dos widgets na tela
        page1.add(lblWelcome)
        page1.add(lblInsertText)
        page1.add(self.entryMessage)
        page1.add(lblModDig)
        page1.pack_start(comboMod,False,False,0)
        page1.pack_start(hboxModDig,False,False,0)
        page1.add(lblModPort)
        page1.pack_start(comboPort,False,False,0)
        page1.add(lblEnq)
        page1.pack_start(hboxEnq,False,False,0)
        page1.add(lblDtError)
        page1.pack_start(hboxDtError,False,False,0)
        page1.add(lblCorrError)
        page1.add(hboxCorrError)
        page1.add(lblWarning)
        page1.add(btnTransmitMessage)








        #Criação da página de Receptor
        page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing= 20)
        page2.set_border_width(20)
        page2.set_name("box-container")
        lblReceptor = Gtk.Label(label="SimulNet")
        lblReceptor.get_style_context().add_class("lblTitle")
        page2.add(lblReceptor)

        tab_label_Receptor = Gtk.Label(label="Receptor")
        tab_label_Receptor.set_name("receptor-tab")
        notebook.append_page(page2,tab_label_Receptor)


        btnStartServer = Gtk.Button(label="Iniciar servidor")
        page2.add(btnStartServer)
        
        ##Receber Sinal - Sem Demodular
        lblSgnBfr = Gtk.Label(label="Sinal Recebido(Antes de Demodular)")
        lblSgnBfr.get_style_context().add_class("lblSection")


        ##Receber Sinal - Depois Demodular
        lblSgnAf = Gtk.Label(label="Sinal Recebido(Depois de demodular)")
        lblSgnAf.get_style_context().add_class("lblSection")

        ##Mensagem Recebida
        lblMsgRec = Gtk.Label(label="Mensagem Recebida")
        lblMsgRec.get_style_context().add_class("lblSection")
        entryMsgRecv = Gtk.Entry()
        entryMsgRecv.get_style_context().add_class("entry")
        lblMsgRcv = Gtk.Label(label="A mensagem recebida irá aparecer aqui")
        entryMsgRecv.set_placeholder_text(lblMsgRcv.get_text())
        entryMsgRecv.set_sensitive(False)


        ##Ocorreu Erro?
        lblErrorOccur = Gtk.Label(label="Ocorreu erro?")
        lblErrorOccur.get_style_context().add_class("lblSection")

        hboxCheckError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxCheckError.set_halign(Gtk.Align.CENTER)
        rdSimErro = Gtk.RadioButton.new_with_label_from_widget(None,"Sim")
        rdNaoErro = Gtk.RadioButton.new_with_label_from_widget(rdSimErro,"Não")
        rdSimErro.set_sensitive(False)
        rdNaoErro.set_sensitive(False)

        hboxCheckError.pack_start(rdSimErro,False,False,0)
        hboxCheckError.pack_start(rdNaoErro,False,False,0)

        #Onde ocorreu erro?
        lblWhereError = Gtk.Label(label="Em qual processo ocorreu o erro?")
        lblWhereError.get_style_context().add_class("lblSection")
        hboxWhereError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxWhereError.set_halign(Gtk.Align.CENTER)
        rdEnquadramento = Gtk.RadioButton.new_with_label_from_widget(None,"Enquadramento")
        rdEnquadramento.set_sensitive(False)
        rdPropQuadro = Gtk.RadioButton.new_with_label_from_widget(rdEnquadramento,"Propagação do quadro")
        rdPropQuadro.set_sensitive(False)

        hboxWhereError.pack_start(rdEnquadramento,False,False,0)
        hboxWhereError.pack_start(rdPropQuadro,False,False,0)

        #Encerrar Servidor
        lblEndServer = Gtk.Label(label="Encerrar Servidor")
        lblEndServer.get_style_context().add_class("lblSection")
        btnEndServer = Gtk.Button()
        btnEndServer.get_style_context().add_class("end-server")
        btnEndServer.add(lblEndServer)

        def insertWidgets(servidorAtivo):
            #print("Dentro da função!")
            #print(servidorAtivo)
                
            if(servidorAtivo==True):

                #Adição de itens na página 2
                page2.remove(btnStartServer)
                page2.add(lblSgnBfr)
                page2.add(lblSgnAf)
                page2.add(lblMsgRec)
                page2.pack_start(entryMsgRecv,False,False,0)
                page2.add(lblErrorOccur)
                page2.pack_start(hboxCheckError,False,False,0)
                page2.add(lblWhereError)
                page2.pack_start(hboxWhereError,False,False,0)
                page2.add(btnEndServer)

                page2.show_all()

            else:
                #Remoção de itens na página 2
                page2.add(btnStartServer)
                page2.remove(lblSgnBfr)
                page2.remove(lblSgnAf)
                page2.remove(lblMsgRec)
                page2.remove(entryMsgRecv)
                page2.remove(lblErrorOccur)
                page2.remove(hboxCheckError)
                page2.remove(lblWhereError)
                page2.remove(hboxWhereError)
                page2.remove(btnEndServer)

            #Atualizar a UI
            page2.show_all()



        def activatingServer(button):
            global servidorAtivo
            servidorAtivo = not servidorAtivo
            #print(servidorAtivo)
            insertWidgets(servidorAtivo)        

        btnStartServer.connect("clicked",activatingServer)
        btnEndServer.connect("clicked",activatingServer)

        def gatherText():
            msgSize = entryMessage.get_text_length()
            if msgSize == 0:
                entryBoxPreenchida = True
                janelaVazio = textoVazio()
                janelaVazio.show_all()
            else:
                entryBoxPreenchida = False




            

        
win = MyWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
