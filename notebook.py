import matplotlib                           # Biblioteca para plotar os graficos

from processSignal import processSignal     # Arquivo de processar sinais
matplotlib.use('GTK3Agg')  # Usar 'GTK3Agg' para renderizar com GTK e Matplotlib

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,Gdk           # Repositorio da GUI GTK
import matplotlib.pyplot as plt             # Chamar a biblioteca como PLT
import threading

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from camadaFisica import *                  # Arquivos de
from camadaEnlace import *
from Simulador import *
from clientTCP import *
from configs import *
from convertions import *
from tuple import *


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

class erroEnviarMensagem(Gtk.Window):
    def okayBtn(self, widget):  # Função para esconder a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Erro ao enviar a mensagem")  # Define o título da janela de erro
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela (largura x altura)

        lblErroMsg = Gtk.Label(label="Servidor não foi iniciado!")  # Cria um label com a mensagem de erro

        addCSS()  # Aplica o estilo CSS à janela

        btnOk = Gtk.Button()  # Cria o botão "Ok"
        lblOk = Gtk.Label(label="Ok")  # Cria o label "Ok" para o botão
        btnOk.add(lblOk)  # Adiciona o label ao botão
        btnOk.connect("clicked", self.okayBtn)  # Conecta o clique do botão à função que oculta a janela

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Cria um container vertical com espaçamento
        vbox.set_name("box-container")  # Define o nome para o container (útil para estilização com CSS)
        vbox.pack_start(lblErroMsg, True, True, 0)  # Adiciona o label de erro ao container
        vbox.pack_start(btnOk, True, True, 0)  # Adiciona o botão "Ok" ao container

        self.add(vbox)  # Adiciona o container à janela
        self.connect("destroy", self.hide)  # Conecta o evento de fechamento da janela à função hide

class mensagemEnviada(Gtk.Window):
    def okayBtn(self, widget):  # Função para esconder a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Mensagem Enviada!")  # Define o título da janela de sucesso
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela (largura x altura)

        wndwLabel = Gtk.Label(label="Mensagem foi enviada com sucesso!")  # Cria um label com a mensagem de sucesso

        addCSS()  # Aplica o estilo CSS à janela

        btnOk = Gtk.Button()  # Cria o botão "Ok"
        lblOk = Gtk.Label(label="Ok")  # Cria o label "Ok" para o botão
        btnOk.add(lblOk)  # Adiciona o label ao botão
        btnOk.connect("clicked", self.okayBtn)  # Conecta o clique do botão à função que oculta a janela

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)  # Cria um container vertical com espaçamento
        vbox.set_name("box-container")  # Define o nome para o container (útil para estilização com CSS)
        vbox.pack_start(wndwLabel, True, True, 0)  # Adiciona o label de sucesso ao container
        vbox.pack_start(btnOk, True, True, 0)  # Adiciona o botão "Ok" ao container

        self.add(vbox)  # Adiciona o container à janela

        self.connect("destroy", self.hide)  # Conecta o evento de fechamento da janela à função hide

class textoVazio(Gtk.Window):
    def okayBtn(self, widget):  # Função para esconder a janela ao clicar no botão "Ok"
        self.hide()

    def __init__(self):
        super().__init__(title="Erro")  # Define o título da janela de erro
        self.set_default_size(200, 100)  # Define o tamanho padrão da janela (largura x altura)

        wndwLabel = Gtk.Label(label="O campo de mensagem está vazio")  # Cria um label com a mensagem de erro

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

class MyWindow(Gtk.Window):
    global tuple  # Define a variável 'tuple' como global para poder ser acessada em qualquer lugar da classe

    def show_graph(self, x_data, y_data, title, label, step=True):
        # Criação de uma nova janela GTK para o gráfico
        graph_window = Gtk.Window(title=title)  # Cria a janela do gráfico com o título passado
        graph_window.set_default_size(800, 600)  # Define o tamanho da janela (largura x altura)

        print("The x_data is: ", x_data)  # Exibe os dados de x no terminal
        print("The y_data is: ", y_data)  # Exibe os dados de y no terminal

        unpack_x = []  # Lista que irá armazenar os dados de x descompactados
        unpack_y = []  # Lista que irá armazenar os dados de y descompactados (ainda não é usada neste trecho)

        # Loop para descompactar os dados de x
        for i in range(0, len(x_data)):  # Para cada elemento em x_data
            byte = x_data[i]  # A variável 'byte' armazena cada elemento de x_data
            for j in range(0, len(byte)):  # Para cada bit dentro do byte
                bit = byte[j]  # O bit é extraído
                unpack_x.append(bit)  # O bit é adicionado à lista unpack_x

        print(unpack_x)  # Exibe a lista unpack_x (dados de x descompactados)
        print(unpack_y)  # Exibe a lista unpack_y (ainda vazia)




# Criando a figura do Matplotlib
        fig, ax = plt.subplots()  # Cria uma figura e um conjunto de eixos para o gráfico

        if step == True:  # Verifica se o parâmetro 'step' é True
            ax.step(y_data, unpack_x, label=label)  # Cria um gráfico de passos (step plot) com os dados de y e unpack_x
        else:  # Caso o parâmetro 'step' seja False
            ax.plot(y_data, unpack_x, label=label)  # Cria um gráfico contínuo (line plot) com os dados de y e unpack_x

        ax.set_title(title)  # Define o título do gráfico
        ax.axhline(0, color='red', linestyle='--', linewidth=2, label='y = 0')  # Adiciona uma linha horizontal no valor y=0
        ax.legend()  # Adiciona a legenda ao gráfico

        # Incorporando a figura no GTK
        canvas = FigureCanvas(fig)  # Cria um canvas do Matplotlib para incorporar o gráfico no GTK

        graph_window.add(canvas)  # Adiciona o canvas à janela do gráfico

        # Exibindo a janela do gráfico
        graph_window.show_all()  # Exibe a janela do gráfico com o conteúdo completo
    def showGraphBfr(self, x_data, y_data, title, label, step=True):
        # Criação de uma nova janela GTK para o gráfico
        graph_window = Gtk.Window(title=title)  # Cria a janela do gráfico com o título passado
        graph_window.set_default_size(800, 600)  # Define o tamanho da janela (largura x altura)

        print("The x_data is: ", x_data)  # Exibe os dados de x no terminal
        print("The y_data is: ", y_data)  # Exibe os dados de y no terminal

        # Criando a figura do Matplotlib
        fig, ax = plt.subplots()  # Cria uma figura e um conjunto de eixos para o gráfico

        if step == True:  # Verifica se o parâmetro 'step' é True
            ax.step(y_data, x_data, label=label)  # Cria um gráfico de passos (step plot) com os dados de y e x_data
        else:  # Caso o parâmetro 'step' seja False
            ax.plot(y_data, x_data, label=label)  # Cria um gráfico contínuo (line plot) com os dados de y e x_data

        ax.set_title(title)  # Define o título do gráfico
        ax.axhline(0, color='red', linestyle='--', linewidth=2, label='y = 0')  # Adiciona uma linha horizontal no valor y=0
        ax.legend()  # Adiciona a legenda ao gráfico

        # Incorporando a figura no GTK
        canvas = FigureCanvas(fig)  # Cria um canvas do Matplotlib para incorporar o gráfico no GTK

        graph_window.add(canvas)  # Adiciona o canvas à janela do gráfico

        # Exibindo a janela do gráfico
        graph_window.show_all()  # Exibe a janela do gráfico com o conteúdo completo

    def on_combo_changed(self, widget):
        global entryBoxPreenchida  # Variável global para indicar se a caixa de mensagem está preenchida
        selected = widget.get_active_text()  # Obtém o texto da opção selecionada no combo box

        msgSize = self.entryMessage.get_text_length()  # Obtém o comprimento do texto inserido na caixa de mensagem
        msg = self.entryMessage.get_text()  # Obtém o texto inserido na caixa de mensagem

        if msgSize == 0:  # Verifica se o comprimento da mensagem é 0 (ou seja, a caixa está vazia)
            entryBoxPreenchida = False  # Define que a caixa de mensagem não está preenchida
            janelaVazio = textoVazio()  # Cria uma janela de erro (campo de mensagem vazio)
            janelaVazio.show_all()  # Exibe a janela de erro
        else:
            entryBoxPreenchida = True  # Define que a caixa de mensagem está preenchida

        if entryBoxPreenchida == True:  # Verifica se a caixa de mensagem está preenchida
            binWord = converterBinario(msg)  # Converte a mensagem para formato binário
            print("Antes de ser processada, a binWord é ", binWord)

            # Processa a binWord de acordo com a seleção do combo box
            if selected == "Gráfico NRZ":  # Se a opção NRZ for selecionada
                binWordNRZ = convertNRZ(binWord)  # Converte para formato NRZ
                print("A entrada do buildNRZ é: ", binWordNRZ)
                binWordNRZ, x_axis = buildNRZ(binWordNRZ)  # Gera os dados do gráfico NRZ
                self.show_graph(binWordNRZ, x_axis, "Gráfico NRZ", "Sinal NRZ")  # Exibe o gráfico NRZ
            elif selected == "Gráfico Manchester":  # Se a opção Manchester for selecionada
                binWordManchester = convert_Manchester(binWord)  # Converte para formato Manchester
                binWordManchester, x_axis = buildManchester(binWordManchester)  # Gera os dados do gráfico Manchester
                self.show_graph(binWordManchester, x_axis, "Gráfico Manchester", "Sinal Manchester")  # Exibe o gráfico Manchester
            elif selected == "Gráfico Bipolar":  # Se a opção Bipolar for selecionada
                binWordBipolar = convertBipolar(binWord)  # Converte para formato Bipolar
                binWordBipolar, x_axis = buildBipolar(binWordBipolar)  # Gera os dados do gráfico Bipolar
                self.show_graph(binWordBipolar, x_axis, "Gráfico Bipolar", "Sinal Bipolar")  # Exibe o gráfico Bipolar
            elif selected == "Gráfico ASK":  # Se a opção ASK for selecionada
                binWordASK = convertASK(binWord)  # Converte para formato ASK
                binWordASK, x_axis = buildPortadora(binWordASK)  # Gera os dados do gráfico ASK
                self.show_graph(binWordASK, x_axis, "Gráfico ASK", "Sinal ASK", step=False)  # Exibe o gráfico ASK
            elif selected == "Gráfico FSK":  # Se a opção FSK for selecionada
                binWordFSK = convertFSK(binWord)  # Converte para formato FSK
                binWordFSK, x_axis = buildPortadora(binWordFSK)  # Gera os dados do gráfico FSK
                self.show_graph(binWordFSK, x_axis, "Gráfico FSK", "Sinal FSK", step=False)  # Exibe o gráfico FSK
            elif selected == "Gráfico 8-QAM":  # Se a opção 8-QAM for selecionada
                binWord8QAM = convert8QAM(binWord)  # Converte para formato 8-QAM
                binWord8QAM, x_axis = buildPortadora(binWord8QAM)  # Gera os dados do gráfico 8-QAM
                self.show_graph(binWord8QAM, x_axis, "Gráfico 8-QAM", "Sinal 8-QAM", step=False)  # Exibe o gráfico 8-QAM
    def on_button_clicked(self, widget):
        # Criação da janela pop-up
        global sentText  # Variável global que armazena o texto enviado
        global ocorreuErro  # Variável global que indica se ocorreu um erro
        global erroEnquad  # Variável global para erro no enquadramento
        global erroTransmit  # Variável global para erro na transmissão
        global size  # Variável global para o tamanho da mensagem
        global length  # Variável global para o comprimento da mensagem
        global tamanho  # Variável global para o tamanho da mensagem

        # Verifica se o comprimento da mensagem é maior que 0
        if self.entryMessage.get_text_length() > 0:
            entryBoxPreenchida = True  # Marca que a caixa de mensagem está preenchida

        # Se a caixa de mensagem está preenchida e o servidor está ativo, inicia a transmissão
        if entryBoxPreenchida == True and servidorAtivo == True:
            print("INICIO DA TRANSMISSÃO------")
            sentText = ''  # Limpa o texto enviado
            sentText = self.entryMessage.get_text()  # Obtém o texto inserido na caixa de mensagem
            print("O SENTTEXT É: ", sentText)

            # Processa o sinal de acordo com as configurações e prepara para envio
            utfWord, tupla = processSignal(sentText)  # Processa o sinal
            print("A UTFWORD É: ", utfWord)
            tuple.clear()  # Limpa a tupla global
            tuple.extend(tupla)  # Adiciona os dados processados à tupla
            saved_message.clear()  # Limpa a mensagem salva
            print(tuple)
            print(sendMessage(utfWord))  # Envia a mensagem
            print(saved_message)

            # Aqui, a comunicação é feita e o resultado pode ser exibido ou processado

        # Se o servidor não está ativo, exibe uma janela de erro
        if servidorAtivo == False:
            popup = erroEnviarMensagem()  # Cria a janela de erro
            popup.show_all()  # Exibe a janela de erro
        else:
            popup = mensagemEnviada()  # Caso contrário, exibe uma janela de confirmação de envio
            popup.show_all()  # Exibe a janela de confirmação
    def graphBfr(self, widget):
        # Exibe o gráfico do sinal recebido antes de ser demodulado

        print("Graph Bfr-> saved_message_puro", saved_message)  # Imprime o conteúdo da variável global saved_message

        # Verifica se há mensagens armazenadas na variável saved_message
        if len(saved_message) > 0:
            binWord, x_axis = receberSinal()  # Recebe o sinal processado e as coordenadas do gráfico
            self.showGraphBfr(binWord, x_axis, "Sinal recebido antes de demodular", "Sinal recebido")  # Exibe o gráfico
        else:
            popUp = noSignal()  # Se não houver sinal, exibe uma mensagem informando a falta de sinal
            popUp.show_all()  # Exibe a janela de erro

    def graphAftr(self, widget):
        global saved_message
        global size

        # Imprime o conteúdo de saved_message para depuração
        print("A saved_message é ", saved_message)

        # Chama a função para demodular o sinal recebido
        sinalProcessado = demodularSinal()

        # Verifica se o sinal foi demodulado corretamente
        if len(sinalProcessado) > 0:
            print("O sinal processado é", sinalProcessado)

            # Realiza o processamento preliminar para criar o gráfico NRZ
            sinalProcessado, x_axis = buildNRZ(sinalProcessado)

            # Exibe o gráfico do sinal após a demodulação
            self.show_graph(sinalProcessado, x_axis, "Sinal recebido e que sofreu demodulação", "Sinal após demodular")
        else:
            # Se não houver sinal processado, exibe uma janela informando a falta de sinal
            popUp = noSignal()
            popUp.show_all()

    # Função chamada quando o botão de radio de modulação é alternado
    def on_radio_toggled_dig(self, button, modulation):
        # Verifica se o botão está ativo (selecionado)
        if button.get_active():
            # Atualiza o valor da modulação na configuração global
            config["modulacao"] = modulation

    # Função chamada quando o botão de radio de enquadramento é alternado
    def on_radio_enq(self, button, enq):
        # Verifica se o botão está ativo (selecionado)
        if button.get_active():
            # Atualiza o valor do enquadramento na configuração global
            config["enquadramento"] = enq

    # Função chamada quando o botão de radio de detecção de erro é alternado
    def on_radio_error(self, button, error):
        # Verifica se o botão está ativo (selecionado)
        if button.get_active():
            # Atualiza o valor da detecção de erro na configuração global
            config["deteccao_erro"] = error

    # Construtor da classe
    def __init__(self):

        # Chama o construtor da classe pai Gtk.Window com o título "Simulador SimulNet"
        super().__init__(title="Simulador SimulNet")

        # Carrega o CSS do arquivo para estilizar a interface
        addCSS()

        # Cria um Notebook (um componente que permite criar abas ou páginas)
        notebook = Gtk.Notebook()
        # Adiciona o notebook à janela principal
        self.add(notebook)

        # Criação da página do Transmissor
        # Cria uma caixa vertical que será usada como conteúdo da página
        page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        # Define a largura da borda da caixa (espaço entre os elementos e a borda)
        page1.set_border_width(10)
        # Define o nome para a caixa, o que pode ser utilizado no CSS para aplicar estilos
        page1.set_name("box-container")
        
        ##Formatação de Estilos para as abas do Notebook
        # Criação de uma label para a aba "Transmissor" e aplicação de estilo via CSS
        tab_label_Transmissor = Gtk.Label(label="Transmissor")
        tab_label_Transmissor.set_name("transmissor-tab")
        # Adiciona a página ao notebook com a label personalizada
        notebook.append_page(page1, tab_label_Transmissor)

        # Criação de labels para exibir o título e o texto de introdução
        lblWelcome = Gtk.Label(label="SimulNet")
        lblInsertText = Gtk.Label(label="Insira a mensagem")
        lblInsertText.get_style_context().add_class("label-small")

        # Define margens e adiciona classes CSS para estilização
        lblWelcome.set_margin_end(20)
        lblWelcome.get_style_context().add_class("lblTitle")

        # Criação do campo de texto para inserir a mensagem a ser transmitida
        self.entryMessage = Gtk.Entry()
        self.entryMessage.get_style_context().add_class("entry")
        lblInputText = Gtk.Label(label="Insira a mensagem a ser transmitida")
        self.entryMessage.set_placeholder_text(lblInputText.get_text())

        ##MODULAÇÃO DIGITAL
        # Criação de label para seção de modulação digital
        lblModDig = Gtk.Label(label="Modulação Digital")
        lblModDig.get_style_context().add_class("lblSection")

        # Criação de um box horizontal para agrupar o dropdown menu e a label de pré-visualização
        hboxModDigIntro = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxModDigIntro.set_halign(Gtk.Align.CENTER)

        # Criação do dropdown menu (ComboBox) para selecionar o gráfico
        comboMod = Gtk.ComboBoxText()
        comboMod.append_text("Selecione um gráfico")
        comboMod.set_active(0)
        lblPreview = Gtk.Label(label="Pré-Visualização")
        hboxModDigIntro.pack_start(comboMod, False, False, 0)

        # Lista de gráficos de modulação digital para o dropdown
        graficosDig = [
            "Gráfico NRZ",
            "Gráfico Manchester",
            "Gráfico Bipolar"
        ]

        # Adiciona as opções de gráficos ao dropdown menu
        for graph in graficosDig:
            comboMod.append_text(graph)

        # Conecta o evento de mudança do dropdown ao método on_combo_changed
        comboMod.connect("changed", self.on_combo_changed)

        # Criação de box horizontal para os botões de rádio (radio buttons) de modulação digital
        hboxModDig = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxModDig.set_halign(Gtk.Align.CENTER)

        # Criação dos radio buttons para diferentes tipos de modulação digital
        rdNRZ_modDig = Gtk.RadioButton.new_with_label_from_widget(None, "NRZ")
        rdNRZ_modDig.connect("toggled", self.on_radio_toggled_dig, "NRZ")
        rdMCH_modDig = Gtk.RadioButton.new_with_label_from_widget(rdNRZ_modDig, "Manchester")
        rdMCH_modDig.connect("toggled", self.on_radio_toggled_dig, "Manchester")
        rdBIP_modDig = Gtk.RadioButton.new_with_label_from_widget(rdNRZ_modDig, "Bipolar")
        rdBIP_modDig.connect("toggled", self.on_radio_toggled_dig, "Bipolar")

        # Adiciona os radio buttons à caixa horizontal
        hboxModDig.pack_start(rdNRZ_modDig, False, False, 0)
        hboxModDig.pack_start(rdMCH_modDig, False, False, 0)
        hboxModDig.pack_start(rdBIP_modDig, False, False, 0)

        ##MODULAÇÃO POR PORTADORA
        # Criação de label para seção de modulação por portadora
        lblModPort = Gtk.Label(label="Modulação por Portadora")
        lblModPort.get_style_context().add_class("lblSection")

        # Criação de uma caixa horizontal para o dropdown de gráficos de portadora
        hboxModPort = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxModPort.set_halign(Gtk.Align.CENTER)

        # Criação do dropdown menu para selecionar o gráfico de portadora
        comboPort = Gtk.ComboBoxText()
        comboPort.append_text("Selecione um gráfico de portadora")
        comboPort.set_active(0)

        # Label de pré-visualização
        lblPreviewMod = Gtk.Label(label="Pré-Visualização")
        hboxModPort.pack_start(comboPort, False, False, 0)

        # Lista de gráficos de modulação por portadora
        graficosPort = [
            "Gráfico ASK",
            "Gráfico FSK",
            "Gráfico 8-QAM"
        ]

        # Adiciona as opções de gráficos ao dropdown
        for graphs in graficosPort:
            comboPort.append_text(graphs)

        # Conecta o evento de mudança do dropdown ao método on_combo_changed
        comboPort.connect("changed", self.on_combo_changed)

        ##Enquadramento
        # Criação de label para a seção de enquadramento
        lblEnq = Gtk.Label(label="Enquadramento")
        lblEnq.get_style_context().add_class("lblSection")

        # Criação de caixa horizontal para os radio buttons de enquadramento
        hboxEnq = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxEnq.set_halign(Gtk.Align.CENTER)

        # Criação dos radio buttons para diferentes tipos de enquadramento
        rdCharCount = Gtk.RadioButton.new_with_label_from_widget(None, "Contagem de Caracteres")
        rdCharCount.connect("toggled", self.on_radio_enq, "charCount")

        rdInsByte = Gtk.RadioButton.new_with_label_from_widget(rdCharCount, "Inserção de Bytes")
        rdInsByte.connect("toggled", self.on_radio_enq, "insByte")

        # Adiciona os radio buttons à caixa horizontal
        hboxEnq.pack_start(rdCharCount, False, False, 0)
        hboxEnq.pack_start(rdInsByte, False, False, 0)
        
        ##Detecção de Erros
        # Criação de label para a seção de detecção de erros
        lblDtError = Gtk.Label(label="Detecção de erros")
        lblDtError.get_style_context().add_class("lblSection")

        # Criação de caixa horizontal para agrupar os radio buttons de detecção de erros
        hboxDtError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxDtError.set_halign(Gtk.Align.CENTER)

        # Radio buttons para selecionar o tipo de detecção de erro (paridade e CRC)
        rdParity = Gtk.RadioButton.new_with_label_from_widget(None, "Paridade par")
        rdParity.connect("toggled", self.on_radio_error, "paridade")

        rdCRC = Gtk.RadioButton.new_with_label_from_widget(rdParity, "CRC")
        rdCRC.connect("toggled", self.on_radio_error, "CRC")

        # Adiciona os radio buttons à caixa
        hboxDtError.pack_start(rdParity, False, False, 0)
        hboxDtError.pack_start(rdCRC, False, False, 0)

        ##Correção de Erros
        # Criação de label para a seção de correção de erros
        lblCorrError = Gtk.Label(label="Correção de erros")
        lblCorrError.get_style_context().add_class("lblSection")

        # Criação de caixa horizontal para o radio button de correção de erros
        hboxCorrError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxCorrError.set_halign(Gtk.Align.CENTER)

        # Radio button para selecionar a correção de erro (Hamming)
        rdHamming = Gtk.RadioButton.new_with_label_from_widget(None, "Hamming")

        # Adiciona o radio button à caixa
        hboxCorrError.pack_start(rdHamming, False, False, 0)

        ##Transmitir Mensagem
        # Criação de label com aviso sobre a chance de erro
        lblWarning = Gtk.Label(label="Obs.: 0,011% de chance de ocorrência de erros")
        lblWarning.set_name("warning")

        # Criação de label e botão para transmitir a mensagem
        lblTransmitMessage = Gtk.Label(label="Transmitir Mensagem")
        lblTransmitMessage.get_style_context().add_class("btnLbl")
        btnTransmitMessage = Gtk.Button()
        btnTransmitMessage.add(lblTransmitMessage)
        btnTransmitMessage.connect("clicked", self.on_button_clicked)

        # Adição dos widgets à página do transmissor
        page1.add(lblWelcome)
        page1.add(lblInsertText)
        page1.add(self.entryMessage)
        page1.add(lblModDig)
        page1.pack_start(hboxModDigIntro, False, False, 0)
        page1.pack_start(hboxModDig, False, False, 0)
        page1.add(lblModPort)
        page1.pack_start(hboxModPort, False, False, 0)
        page1.add(lblEnq)
        page1.pack_start(hboxEnq, False, False, 0)
        page1.add(lblDtError)
        page1.pack_start(hboxDtError, False, False, 0)
        page1.add(lblCorrError)
        page1.add(hboxCorrError)
        page1.add(lblWarning)
        page1.add(btnTransmitMessage)

        # Criação da página de Receptor
        page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        page2.set_border_width(20)
        page2.set_name("box-container")

        # Criação de label de título para a página de receptor
        lblReceptor = Gtk.Label(label="SimulNet")
        lblReceptor.get_style_context().add_class("lblTitle")
        page2.add(lblReceptor)

        # Criação da aba do receptor
        tab_label_Receptor = Gtk.Label(label="Receptor")
        tab_label_Receptor.set_name("receptor-tab")
        notebook.append_page(page2, tab_label_Receptor)

        # Criação de botão para iniciar o servidor
        lblStartServer = Gtk.Label(label="Iniciar servidor")
        lblStartServer.get_style_context().add_class("lblSection")
        btnStartServer = Gtk.Button()
        btnStartServer.add(lblStartServer)
        page2.add(btnStartServer)

        ##Receber Sinal - Antes de Demodular
        # Criação de label e botão para visualizar o sinal antes da demodulação
        lblSgnBfr = Gtk.Label(label="Sinal Recebido (Antes de Demodular)")
        lblSgnBfr.get_style_context().add_class("lblSection")
        lblViewGraph = Gtk.Label(label="Visualizar Sinal")
        lblViewGraph.get_style_context().add_class("lblSection")
        btnSgnBfr = Gtk.Button()
        btnSgnBfr.get_style_context().add_class("btnLbl")
        btnSgnBfr.add(lblViewGraph)
        btnSgnBfr.connect("clicked", self.graphBfr)

        ##Receber Sinal - Depois de Demodular
        # Criação de label e botão para visualizar o sinal após a demodulação
        lblSgnAf = Gtk.Label(label="Sinal Recebido (Depois de Demodular)")
        lblSgnAf.get_style_context().add_class("lblSection")
        lblViewGraph2 = Gtk.Label(label="Visualizar Sinal")
        lblViewGraph2.get_style_context().add_class("lblSection")
        btnSgnAft = Gtk.Button()
        btnSgnAft.add(lblViewGraph2)
        btnSgnAft.get_style_context().add_class("btnLbl")
        btnSgnAft.connect("clicked", self.graphAftr)

        ##Mensagem Recebida
        # Criação de campo de entrada para exibir a mensagem recebida
        lblMsgRec = Gtk.Label(label="Mensagem Recebida")
        lblMsgRec.get_style_context().add_class("lblSection")
        self.entryMsgRecv = Gtk.Entry()
        self.entryMsgRecv.get_style_context().add_class("entry")
        lblMsgRcv = Gtk.Label(label="A mensagem recebida irá aparecer aqui")
        self.entryMsgRecv.set_placeholder_text(lblMsgRcv.get_text())
        self.entryMsgRecv.set_sensitive(False)

        ##Ocorreu Erro?
        # Criação de radio buttons para verificar se ocorreu erro
        lblErrorOccur = Gtk.Label(label="Ocorreu erro?")
        lblErrorOccur.get_style_context().add_class("lblSection")
        hboxCheckError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxCheckError.set_halign(Gtk.Align.CENTER)
        rdSimErro = Gtk.RadioButton.new_with_label_from_widget(None, "Sim")
        rdNaoErro = Gtk.RadioButton.new_with_label_from_widget(rdSimErro, "Não")
        rdSimErro.set_sensitive(False)
        rdNaoErro.set_sensitive(False)

        # Adiciona os radio buttons à caixa
        hboxCheckError.pack_start(rdSimErro, False, False, 0)
        hboxCheckError.pack_start(rdNaoErro, False, False, 0)

        # Onde ocorreu erro?
        lblWhereError = Gtk.Label(label="Em qual processo ocorreu o erro?")
        lblWhereError.get_style_context().add_class("lblSection")
        hboxWhereError = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hboxWhereError.set_halign(Gtk.Align.CENTER)
        rdEnquadramento = Gtk.RadioButton.new_with_label_from_widget(None, "Enquadramento")
        rdEnquadramento.set_sensitive(False)
        rdPropQuadro = Gtk.RadioButton.new_with_label_from_widget(rdEnquadramento, "Propagação do quadro")
        rdPropQuadro.set_sensitive(False)

        # Adiciona os radio buttons à caixa
        hboxWhereError.pack_start(rdEnquadramento, False, False, 0)
        hboxWhereError.pack_start(rdPropQuadro, False, False, 0)

        # Encerrar Servidor
        # Criação de botão para encerrar o servidor
        lblEndServer = Gtk.Label(label="Encerrar Servidor")
        lblEndServer.get_style_context().add_class("lblSection")
        btnEndServer = Gtk.Button()
        btnEndServer.get_style_context().add_class("end-server")
        btnEndServer.add(lblEndServer)

        def insertWidgets(servidorAtivo):
            # Verifica se o servidor está ativo
            if servidorAtivo == True:
                # Adiciona itens à página 2 quando o servidor está ativo
                page2.remove(btnStartServer)  # Remove o botão de iniciar servidor
                page2.add(lblSgnBfr)  # Adiciona o label do sinal antes da demodulação
                page2.add(btnSgnBfr)  # Adiciona o botão para visualizar o sinal antes da demodulação
                page2.add(lblSgnAf)  # Adiciona o label do sinal após a demodulação
                page2.add(btnSgnAft)  # Adiciona o botão para visualizar o sinal após a demodulação
                page2.add(lblMsgRec)  # Adiciona o label para a mensagem recebida
                page2.pack_start(self.entryMsgRecv, False, False, 0)  # Adiciona o campo de entrada para a mensagem recebida
                page2.add(lblErrorOccur)  # Adiciona o label sobre a ocorrência de erro
                page2.pack_start(hboxCheckError, False, False, 0)  # Adiciona o contêiner de seleção de erro (Sim/Não)
                page2.add(lblWhereError)  # Adiciona o label de onde ocorreu o erro
                page2.pack_start(hboxWhereError, False, False, 0)  # Adiciona o contêiner de seleção de erro no processo
                page2.add(btnEndServer)  # Adiciona o botão para encerrar o servidor

                # Exibe todos os widgets na página
                page2.show_all()

            else:
                # Remove os itens da página 2 quando o servidor não está ativo
                page2.add(btnStartServer)  # Adiciona o botão de iniciar servidor de volta
                page2.remove(lblSgnBfr)  # Remove o label do sinal antes da demodulação
                page2.remove(btnSgnBfr)  # Remove o botão do sinal antes da demodulação
                page2.remove(lblSgnAf)  # Remove o label do sinal após a demodulação
                page2.remove(btnSgnAft)  # Remove o botão do sinal após a demodulação
                page2.remove(lblMsgRec)  # Remove o label de mensagem recebida
                page2.remove(self.entryMsgRecv)  # Remove o campo de entrada da mensagem recebida
                page2.remove(lblErrorOccur)  # Remove o label de ocorrência de erro
                page2.remove(hboxCheckError)  # Remove o contêiner de erro (Sim/Não)
                page2.remove(lblWhereError)  # Remove o label de onde ocorreu o erro
                page2.remove(hboxWhereError)  # Remove o contêiner de onde ocorreu o erro
                page2.remove(btnEndServer)  # Remove o botão de encerrar servidor

            # Atualiza a interface gráfica, garantindo que as mudanças sejam refletidas
            page2.show_all()

        # Função que ativa ou desativa o servidor, dependendo do seu estado atual
        def activatingServer(button):
            # Variável global que indica se o servidor está ativo ou não
            global servidorAtivo

            # Verifica se o servidor está ativo
            if servidorAtivo:
                # Caso o servidor esteja ativo, imprime uma mensagem e fecha o servidor
                print("O servidor será fechado")
                servidorAtivo = False

                # Cria uma janela informando que o servidor foi fechado
                popUp = serverEndedWindow()
                popUp.show_all()

                # Chama a função para parar o servidor
                stop_server()

                # Verifica se a porta 8030 está aberta (comentado)
                #print(is_port_open('localhost',8030))
            else:
                # Caso o servidor não esteja ativo, imprime uma mensagem e inicia o servidor
                print("O servidor será iniciado")
                servidorAtivo = True

                # Cria uma nova thread para iniciar o servidor, sem bloquear o fluxo principal
                thread = threading.Thread(target=start_server, daemon = True)
                thread.start()

                # Cria uma janela informando que o servidor foi iniciado
                popUp = serverStartedWindow()
                popUp.show_all()

                # Verifica se a porta 8030 está aberta (comentado)
                #print(is_port_open('localhost',8030))

            # Atualiza os widgets na interface de acordo com o estado do servidor
            insertWidgets(servidorAtivo)

            # A função start_server() é chamada diretamente no código (comentado)
            #start_server()        

        # Conecta o botão de início do servidor ao evento de clique
        btnStartServer.connect("clicked",activatingServer)

        # Conecta o botão de encerramento do servidor ao evento de clique
        btnEndServer.connect("clicked",activatingServer)

            

        
# Cria uma nova instância da classe MyWindow, que representa a janela principal
win = MyWindow()

# Conecta o evento de destruição da janela (fechar a janela) à função Gtk.main_quit
# Isso garante que a aplicação será encerrada quando a janela for fechada
win.connect("destroy", Gtk.main_quit)

# Exibe todos os widgets dentro da janela
win.show_all()

# Inicia o loop principal da interface gráfica, que mantém a janela aberta e processa eventos
Gtk.main()