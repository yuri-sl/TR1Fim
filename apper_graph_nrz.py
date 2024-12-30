import gi
import numpy as np

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
from matplotlib.figure import Figure


class Apper_graph_nrz:
    def __init__(self, a = []):
        self.a = a
        self.apper_new_graph()

    def apper_new_graph(self):
        fig, ax = plt.subplots()
        t = np.arange(len(self.a))

        # Plotando o sinal digital NRZ
        ax.step(t, self.a, where='post', label='Sinal NRZ', linewidth=2)  # 'post' garante que o valor seja mantido após a transição
        ax.set_title("Sinal Digital NRZ")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")
        ax.legend()
        
        def new_a_and_b(button):  # Recebe o botão como argumento
            self.a = [1, 2, 3, 4, 5]
            ax.clear()
            ax.plot(self.a, 'ro-', label='easy as 1 2 3')
            ax.legend()
            fig.canvas.draw() 


        # you can access the window or vbox attributes this way
        manager = fig.canvas.manager
        toolbar = manager.toolbar
        vbox = manager.vbox


        # now let's add a button to the toolbar

        button1 = Gtk.Button(label='Click me 1')
        button1.show()
        button1.connect('clicked', lambda button: print('hi mom!!!'))


        toolitem1 = Gtk.ToolItem()
        toolitem1.show()
        toolitem1.set_tooltip_text('Click me for fun and profit')
        toolitem1.add(button1)

        pos1 = 11  # where to insert this in the toolbar
        toolbar.insert(toolitem1, pos1)

        button2 = Gtk.Button(label='Click me 2')
        button2.show()
        button2.connect('clicked', new_a_and_b,)


        toolitem2 = Gtk.ToolItem()
        toolitem2.show()
        toolitem2.set_tooltip_text('Click meeeeeee for fun and profit')
        toolitem2.add(button2)


        pos2 = 9  # where to insert this in the toolbar
        toolbar.insert(toolitem2, pos2)

        # now let's add a widget to the vbox
        label = Gtk.Label()
        label.set_markup('Drag mouse over axes for position')
        label.show()
        vbox.pack_start(label, False, False, 0)
        vbox.reorder_child(toolbar, -1)

        def update(event):
            if event.xdata is None:
                label.set_markup('Drag mouse over axes for position')
            else:
                label.set_markup(
                    f'<span color="#ef0000">x,y=({event.xdata}, {event.ydata})</span>')
        fig.canvas.mpl_connect('motion_notify_event', update)
        plt.show()
