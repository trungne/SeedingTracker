import tkinter as tk
from PIL import ImageTk, Image

class User_options(tk.Frame):
    
    def __init__(self, parent):
        
        super().__init__(parent)
        
        self.pack()
        self.parent = parent
        self.user_prompt_label = tk.Label(self, text="What do you want to do?")

        self.user_choice = tk.StringVar()
        self.user_choice_update = tk.Radiobutton(self, text="Update", variable=self.user_choice, value="Update", command=self.apply_user_choice)
        self.user_choice_query = tk.Radiobutton(self, text="Query", variable=self.user_choice, value="Query",command=self.apply_user_choice) 
        self.show_widgets()
    def show_widgets(self):
        self.user_prompt_label.grid(row=0, pady=5, columnspan=2)
        self.user_choice_update.grid(row=1, pady=5, column=0)
        self.user_choice_query.grid(row=1, pady=5, column=1)
    
    def apply_user_choice(self, old_menu_frame, menu_frame):
        old_menu_frame.pack_remove()
        menu_frame.pack()
test = User_options(tk.Tk())
print(f"type of user_options = {type(test)}")
def called_class():
    print("Class assignment")
    return 2

class Bar(object):
    y = called_class()

    def __init__(self, x):
        self.x = x

## "Class assignment"

def called_instance():
    print("Instance assignment")
    return 2

class Foo(object):
    def __init__(self, x):
        self.y = called_instance()
        self.x = x

a = Bar(1)
Bar(2)
Foo(1)
## "Instance assignment"
Foo(2)
## "Instance assignment"
print(f"type of bar = {type(a).__name__}")