import tkinter as tk
from PIL import ImageTk, Image
from constants import *

def show_widgets_in_consecutive_grids(list_of_widgets, row=0):
    total_rows = len(list_of_widgets) + row

    index = 0
    for each_row in range(row, total_rows):
        if type(list_of_widgets[index]) == list: # if an item is a list
            for i in range(len(list_of_widgets[index])): # display the list in ONE ROW
                list_of_widgets[index][i].grid(row=each_row, sticky="nsew", column=i, pady=DEFAULT_PAD_Y)
        
        elif type(list_of_widgets[index]).__name__ == "Reaction":
            list_of_widgets[index].display_reaction(each_row)
        # sticky="nsew"
        else:
            list_of_widgets[index].grid(row=each_row, sticky="nsew", columnspan=MAX_COLUMN_RANGE, pady=DEFAULT_PAD_Y)
        index += 1
    return total_rows + row

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

class Reaction:
    def __init__(self, name, root):
        # a string
        self.name = name

        # tk.Entry object
        self.entry = tk.Entry(root, validate="key")
        self.entry['validatecommand'] = (self.entry.register(testVal),'%P','%d') # set constraint to only int

        # tk.Label object
        self.label_image = ImageTk.PhotoImage(Image.open(f"./icons/{self.name}.png").resize((58, 58)))
        self.label = tk.Label(root, image=self.label_image)

    def get_count(self):
        print(f"{self.name}: ", end= '')
        return self.entry.get()

    def display_reaction(self, cur_row, column=0):
        self.label.grid(row=cur_row, column=column, padx=29.5, sticky="nsew", pady=DEFAULT_PAD_Y)
        self.entry.grid(row=cur_row, column=column+1,sticky="nsew", pady=DEFAULT_PAD_Y)

    def destroy_reaction(self):
        self.label.grid_forget()
        self.entry.grid_forget()


class Reaction_frame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.fb_reactions_list = [Reaction("fb_like", self), Reaction("fb_heart", self), Reaction("fb_care", self), 
                                Reaction("fb_haha", self), Reaction("fb_wow", self), Reaction("fb_sad", self), 
                                Reaction("fb_angry", self), Reaction("fb_comment", self), Reaction("fb_share", self)]
 
        self.twitter_reactions_list = [Reaction("twitter_cmt", self), Reaction("twitter_retweet", self), Reaction("twitter_heart", self)]

        self.instagram_reactions_list = [Reaction("instagram_cmt", self), Reaction("instagram_heart", self)]

        self.current_reactions = {
            "Facebook": self.fb_reactions_list,
            "Twitter": self.twitter_reactions_list,
            "Instagram": self.instagram_reactions_list
        }

        self.current_platform = None
        
    def destroy_current_reactions_list(self, platform):
        pass
        

    def set_reactions_list(self, platform):
        if not self.current_platform:
            pass
        elif platform != self.current_platform:
            for reaction in self.current_reactions[self.current_platform]:
                reaction.destroy_reaction()

        self.current_platform = platform

        show_widgets_in_consecutive_grids(self.current_reactions[self.current_platform])

    def get_reactions_list(self):
        return self.current_reactions[self.current_platform]
