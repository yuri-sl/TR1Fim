import gi


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,Gdk


servidorAtivo = False

class MyWindow(Gtk.Window):

    def __init__(self):

        super().__init__(title="Simulador SimulNet")

        #Load CSS from file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


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
        ##EntryBox
        entryMessage = Gtk.Entry()
        entryMessage.get_style_context().add_class("entry")
        lblInputText = Gtk.Label(label="Insira a mensagem a ser transmitida")
        entryMessage.set_placeholder_text(lblInputText.get_text())

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




        #Adição dos widgets na tela
        page1.add(lblWelcome)
        page1.add(lblInsertText)
        page1.add(entryMessage)
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
        lblServerStarted = Gtk.Label(label="Server has been started!")
        
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


        ##Ocorreu Erro?
        lblErrorOccur = Gtk.Label(label="Ocorreu erro?")
        lblErrorOccur.get_style_context().add_class("lblSection")

        hboxCheckError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxCheckError.set_halign(Gtk.Align.CENTER)
        rdSimErro = Gtk.RadioButton.new_with_label_from_widget(None,"Sim")
        rdNaoErro = Gtk.RadioButton.new_with_label_from_widget(rdSimErro,"Não")

        hboxCheckError.pack_start(rdSimErro,False,False,0)
        hboxCheckError.pack_start(rdNaoErro,False,False,0)

        #Onde ocorreu erro?
        lblWhereError = Gtk.Label(label="Em qual processo ocorreu o erro?")
        lblWhereError.get_style_context().add_class("lblSection")
        hboxWhereError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
        hboxWhereError.set_halign(Gtk.Align.CENTER)
        rdEnquadramento = Gtk.RadioButton.new_with_label_from_widget(None,"Enquadramento")
        rdPropQuadro = Gtk.RadioButton.new_with_label_from_widget(rdEnquadramento,"Propagação do quadro")

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
            print(servidorAtivo)
            insertWidgets(servidorAtivo)        

        btnStartServer.connect("clicked",activatingServer)
        btnEndServer.connect("clicked",activatingServer)



            

        
win = MyWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()
