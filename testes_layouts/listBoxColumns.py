import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class GridColumnWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Grid with Columns")
        self.set_default_size(400, 300)

        # Create a scrolled window for larger data sets
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.add(scrolled_window)

        # Create a Grid for tabular layout
        grid = Gtk.Grid(column_spacing=10, row_spacing=5, margin=10)
        scrolled_window.add(grid)

        # Data for rows
        data = [
            ("Name", "Age", "Occupation"),  # Header row
            ("Alice", "25", "Engineer"),
            ("Bob", "30", "Designer"),
            ("Charlie", "35", "Manager"),
        ]

        # Populate the grid with data
        for row_index, row_data in enumerate(data):
            for col_index, item in enumerate(row_data):
                label = Gtk.Label(label=item, xalign=0)
                # Make the header row bold
                if row_index == 0:
                    label.set_markup(f"<b>{item}</b>")
                grid.attach(label, col_index, row_index, 1, 1)

        # Show all widgets
        self.show_all()


win = GridColumnWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
