import tkinter as tk


class Nav_button(tk.Button):
    def __init__(self, parent, **options):
        tk.Button.__init__(self, parent, width=10, **options)
        self.visible = False

    def hide(self):
        self.visible = False
        self.grid_forget()


class Prev_button(Nav_button):
    def __init__(self, parent, **options):
        Nav_button.__init__(self, parent, text="Previous", **options)

    def show(self):
        self.visible = True
        self.grid(row=0, column=0, padx=10)


class Next_button(Nav_button):
    def __init__(self, parent, **options):
        Nav_button.__init__(self, parent, text="Next", **options)

    def show(self):
        self.visible = True
        self.grid(row=0, column=1, padx=10)


class Submit_button(Nav_button):
    def __init__(self, parent, **options):
        Nav_button.__init__(self, parent, text="Submit", **options)

    def show(self):
        self.visible = True
        self.grid(row=0, column=2, padx=10)
