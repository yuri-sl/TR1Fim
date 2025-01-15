import gi


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk



class MyWindow(Gtk.Window):

    def __init__(self):

        super().__init__(title="Hello World")


        self.box1 = Gtk.Box(spacing=6)
        self.box2 = Gtk.Box(spacing=6)

        self.add(self.box1)
        self.add(self.box2)


        self.button1 = Gtk.Button(label="Hello")

        self.button1.connect("clicked", self.on_button1_clicked)

        self.box1.pack_start(self.button1, True, True, 0)

        self.button3 = Gtk.Button(label="Button3")
        self.box2.pack_end(self.button3,True, True, 0)

        self.button4 = Gtk.Button(label="button 4")
        self.box2.pack_end(self.button4,True,True,0)


        self.button2 = Gtk.Button(label="Goodbye")

        self.button2.connect("clicked", self.on_button2_clicked)

        self.box1.pack_start(self.button2, True, True, 0)


    def on_button1_clicked(self, widget):

        print("Hello")


    def on_button2_clicked(self, widget):

        print("Goodbye")



win = MyWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()