import tkinter as tk


class Credentials():
    def __init__(self, edt):
        self.edt = edt

        self.window = tk.Tk()
        self.window.title("Credentials")
        self.window.attributes('-topmost', True)

        description_text = "Please insert your credentials"
        self.description = tk.Label(self.window, text=description_text)
        self.description.pack(pady=5)

        self.username_frame = tk.Frame(self.window)
        username_text = "Username:"
        self.entry_username = tk.Entry(self.username_frame, width=20)
        self.label_username = tk.Label(
            self.username_frame, anchor='e', width=10, text=username_text)
        self.label_username.pack(padx=5, side=tk.LEFT)
        self.entry_username.focus_set()
        self.entry_username.pack(padx=5, side=tk.RIGHT)
        self.username_frame.pack(pady=5)

        self.password_frame = tk.Frame(self.window)
        password_text = "Password:"
        self.label_password = tk.Label(
            self.password_frame, width=10, anchor='e', text=password_text)
        self.entry_password = tk.Entry(self.password_frame, show='*', width=20)
        self.label_password.pack(padx=5, side=tk.LEFT)
        self.entry_password.pack(padx=5, side=tk.RIGHT)
        self.password_frame.pack(pady=5)

        self.submit_button = tk.Button(
            self.window, text="Submit", command=self.submit)
        self.submit_button.pack(pady=5)

        self.window.bind('<Key>', self.key_pressed)

        self.window.mainloop()

    def key_pressed(self, event):
        if event.char == '\r':
            self.submit()

    def submit(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        self.window.destroy()
        self.edt.pass_credentials(self.username, self.password)


if __name__ == '__main__':
    Credentials('')
