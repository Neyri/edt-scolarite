from tkinter import ttk
import tkinter as tk


class Prompting_frame():
    def __init__(self, parent):
        self.parent = parent

        self.main_frame = tk.Frame(
            parent, width=500, height=400)

        self.instruction_label = tk.Label(self.main_frame, text="Hello world!")
        self.instruction_label.pack(pady=5)

        self.data_frame = tk.Frame(
            self.main_frame, width=450, height=300)
        self.data_frame.pack(pady=5, padx=5)
        self.create_data_table()

    def show(self):
        self.main_frame.grid(row=0)

    def hide(self):
        self.main_frame.grid_forget()

    def create_data_table(self):
        self.headers = ('validate', 'Day', 'Hour', 'Title')
        self.headers_width = (50, 150, 80, 250)
        self.table = ttk.Treeview(
            self.data_frame, columns=self.headers, show='headings')
        self.table.grid(column=0, row=0, rowspan=2)

        ysb = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL,
                            command=self.table.yview)
        self.table['yscroll'] = ysb.set
        ysb.grid(row=0, rowspan=2, column=1, sticky=tk.NS)

        self.table.bind('<<TreeviewSelect>>', self.check_box)

        for i, head in enumerate(self.headers):
            self.table.heading(head, text=head)
            self.table.column(
                head, width=self.headers_width[i], anchor=tk.CENTER)

    def set_data(self, table_data):
        self.id_event_table = {}
        for event in table_data:
            row = self.format_event(event)
            row = ['\u2611'] + row  # 2610
            id = self.table.insert('', 'end', values=row)
            self.id_event_table[id] = event

    def format_event(self, event):
        # Day , start_h - end_h , title
        day = event.start_datetime.strftime('%A %d %B')
        hour = event.start_datetime.strftime(
            '%H:%M') + ' - ' + event.end_datetime.strftime('%H:%M')
        return [day, hour, event.title]

    def check_box(self, event):
        selection = self.table.selection()
        for item in selection:
            values = self.table.set(item)
            values['validate'] = '\u2610' if values['validate'] == '\u2611' else '\u2611'
            values = [val for key, val in values.items()]
            self.table.item(item, values=values)

    def get_checked_items(self):
        checked_items = []
        for item in self.id_event_table.keys():
            content = self.table.set(item)
            if content['validate'] == '\u2611':
                event = self.id_event_table[item]
                checked_items.append(event)
        return checked_items


class Insert_frame(Prompting_frame):
    def __init__(self, to_insert, parent):
        self.to_insert = to_insert
        Prompting_frame.__init__(self, parent)
        self.set_data(self.to_insert)
        self.instruction_label['text'] = 'Please uncheck from the list all the events you DON\'T want to be inserted'


class Delete_frame(Prompting_frame):
    def __init__(self, to_delete, parent):
        self.to_delete = to_delete
        Prompting_frame.__init__(self, parent)
        self.instruction_label['text'] = 'Please uncheck from the list all the events you DON\'T want to be deleted'
        self.set_data(self.to_delete)
