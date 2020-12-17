import tkinter as tk
from constants import *
import sys


class Login_page(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack()

        # main widgets
        self.instruction = tk.Label(self, text="Please enter your id and password!")

        self.login_id_label = tk.Label(self, text="ID: ")
        self.login_id = tk.Entry(self)
        self.login_id.focus()
        self.password_label = tk.Label(self, text="Password: ")
        self.password = tk.Entry(self, show="*")

        self.login_button = tk.Button(self, text="Login", command=self.login)

        self.login_status = tk.Label(self)

        self.widgets_list = [self.instruction,
                            [self.login_id_label, self.login_id],
                            [self.password_label, self.password],
                            self.login_button,
                            self.login_status]

        show_widgets_in_consecutive_grids(self.widgets_list)
        self.parent.bind('<Return>', self.login)

    def login(self, event=None):
        _id = self.login_id.get()
        password = self.password.get()
        if _id in login_info and password == login_info[_id]:
            self.login_status["text"] = "Successful"
        else:
            self.login_status["text"] = "Wrong ID or Password!"

def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Login")
    login = Login_page(root)

    root.mainloop()

if __name__ == "__main__":
    main()