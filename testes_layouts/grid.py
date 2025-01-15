import gi


gi.require_version("Gtk", "3.0")

from gi.repository import Gtk,Gdk



class GridWindow(Gtk.Window):

    def __init__(self):


        super().__init__(title="Grid Example")


        button1 = Gtk.Button(label="Button 1")

        button2 = Gtk.Button(label="Button 2")

        button3 = Gtk.Button(label="Button 3")

        button4 = Gtk.Button(label="Button 4")

        button5 = Gtk.Button(label="Button 5")

        button6 = Gtk.Button(label="Button 6")

        label1 = Gtk.Label(label="Welcome!")

        label1.get_style_context().add_class("header-label")
        button1.get_style_context().add_class("styled-button")
        button2.get_style_context().add_class("styled-button")
        button3.get_style_context().add_class("styled-button")
        button4.get_style_context().add_class("styled-button")
        button5.get_style_context().add_class("styled-button")
        button6.get_style_context().add_class("styled-button")




        grid = Gtk.Grid()

        grid.attach(label1,0,0,10,10)

        grid.attach_next_to(button1,label1,Gtk.PositionType.BOTTOM,2,1)

        grid.attach_next_to(button2, label1, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(button3, button1, Gtk.PositionType.BOTTOM, 2, 1)

        grid.attach_next_to(button4, button1, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(button5, button4, Gtk.PositionType.BOTTOM, 2, 1)

        grid.attach_next_to(button6, button5, Gtk.PositionType.RIGHT, 1, 1)


        self.add(grid)
        self.maximize()

        self.apply_css()
    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )



win = GridWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()

Gtk.main()