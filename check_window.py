from nav_buttons import *
from prompting_frames import *


class User_check():
    def __init__(self, to_insert, to_delete, agenda):
        self.to_insert = to_insert
        self.to_delete = to_delete
        self.agenda = agenda

        self.window = tk.Tk()
        self.window.title('Review events')
        self.insert_frame = Insert_frame(self.to_insert, self.window)
        self.delete_frame = Delete_frame(self.to_delete, self.window)
        self.insert_frame.show()

        self.frame_order = [self.insert_frame, self.delete_frame]
        self.current_page = 0

        self.button_frame = tk.Frame(self.window)
        self.create_nav_buttons()
        self.button_frame.grid(row=1, pady=5)

        self.window.mainloop()

    def create_nav_buttons(self):
        self.previous_button = Prev_button(
            self.button_frame, command=self.prev_page)
        self.next_button = Next_button(
            self.button_frame, command=self.next_page)
        self.submit_button = Submit_button(
            self.button_frame, command=self.submit)
        self.previous_button.show()
        self.next_button.show()
        self.submit_button['state'] = 'disabled'
        self.submit_button.show()

    def prev_page(self):
        if self.current_page > 0:
            self.frame_order[self.current_page].hide()
            self.current_page -= 1
            self.frame_order[self.current_page].show()
            if self.submit_button.visible:
                self.next_button['state'] = 'normal'
                self.submit_button['state'] = 'disabled'
            if self.current_page == 0:
                self.previous_button['state'] = 'disabled'

    def next_page(self):
        if self.current_page < len(self.frame_order) - 1:
            self.frame_order[self.current_page].hide()
            self.current_page += 1
            self.frame_order[self.current_page].show()
            if self.previous_button['state'] != 'normal':
                self.previous_button['state'] = 'normal'
            if self.current_page == len(self.frame_order) - 1:
                self.next_button['state'] = 'disabled'
                self.submit_button['state'] = 'normal'

    def submit(self):
        self.agenda.insert_list_events(self.insert_frame.get_checked_items())
        self.agenda.delete_list_events(self.delete_frame.get_checked_items())
        self.window.destroy()


if __name__ == '__main__':
    User_check(
        [['1', '2 un très long texte vraiment très long', '3'], [5, 6, 7]], [])
