import tkinter as tk
from PIL import ImageTk, Image
from Reaction import *
from constants import *

class User_options(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack()
        self.parent = parent

        self.user_prompt_label = tk.Label(self, text="What do you want to do?")

        self.user_choice = tk.StringVar()
        self.user_choice_update = tk.Radiobutton(self, text="Update", variable=self.user_choice, value="Update", command=self.apply_user_choice)
        self.user_choice_query = tk.Radiobutton(self, text="Query", variable=self.user_choice, value="Query", command=self.apply_user_choice) 
        self.user_choice_delete = tk.Radiobutton(self, text="Delete", variable=self.user_choice, value="Delete", command=self.apply_user_choice)
        
        self.my_update_menu = Update_menu(self.parent)
        self.my_query_menu = Query_menu(self.parent)
        self.my_delete_menu = Delete_menu(self.parent)

        self.current_menu = None

        self.widgets_list = [self.user_prompt_label, 
                            [self.user_choice_update, self.user_choice_query, self.user_choice_delete]]

        show_widgets_in_consecutive_grids(self.widgets_list)        

    def apply_user_choice(self):
        # remove the menu frame if there is one
        if self.current_menu:
                self.current_menu.pack_forget() 

        # set the current menu to according to the user choice
        if self.user_choice.get() == "Update":
            self.current_menu = self.my_update_menu
        elif self.user_choice.get() == "Query":
            self.current_menu = self.my_query_menu
        elif self.user_choice.get() == "Delete":
            self.current_menu = self.my_delete_menu
        else:
            pass
            #self.current_menu = 

        # display the menu, the menu is displayed onto the root, just like User_options
        self.current_menu.pack()

class Delete_menu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.instruction = tk.Label(self, text="Please enter the post id")
        
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.post_id_status = tk.Label(self)
        self.delete_button = tk.Button(self, text="Delete")
        self.widgets_list = [self.instruction,
                            [self.post_id_label, self.post_id_entry],
                            self.post_id_status, self.delete_button]

        show_widgets_in_consecutive_grids(self.widgets_list)

class Query_menu(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.instruction = tk.Label(self, text="Please enter the post id")
        
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.post_id_status = tk.Label(self)
        self.query_button = tk.Button(self, text="Query")
        self.widgets_list = [self.instruction,
                            [self.post_id_label, self.post_id_entry],
                            self.post_id_status, self.query_button]

        # show widgets
        show_widgets_in_consecutive_grids(self.widgets_list)
        
class Update_menu(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent

        self.fb_icon = ImageTk.PhotoImage(Image.open("./icons/fb.png").resize((58, 58)))
        self.twitter_icon = ImageTk.PhotoImage(Image.open("./icons/twitter.png").resize((58, 58)))   
        self.instagram_icon = ImageTk.PhotoImage(Image.open("./icons/instagram.png").resize((58, 58)))

        '''Default widgets'''

        # radiobuttons for platfrom choices
        self.instruction_platform = tk.Label(self, text="Please choose your platform")
        
        self.platform_choice = tk.StringVar()
        
        self.facebook = tk.Radiobutton(self, image=self.fb_icon, variable=self.platform_choice, value="Facebook", command= self.update_reactions_widgets)
        self.twitter = tk.Radiobutton(self, image=self.twitter_icon, variable=self.platform_choice, value="Twitter", command= self.update_reactions_widgets)
        self.instagram = tk.Radiobutton(self, image=self.instagram_icon, variable=self.platform_choice, value="Instagram", command= self.update_reactions_widgets)
        
        # label as instruction for user
        self.post_id_instruction = tk.Label(self, text="Enter your post ID")
        
        # post_id widgets
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.post_id_status = tk.Label(self)

        # name of the poster
        self.poster_label = tk.Label(self, text="Name: ")
        self.poster_entry = tk.Entry(self)
        
        # reaction widgets
        
        self.reactions_widgets = Reaction_frame(self)

        # update button to update data to database
        self.update_button = tk.Button(self, text="Update", command=self.update_engagement_data)
        
        '''Show default widgets'''

        self.default_widgets_list = [self.instruction_platform,
                                    [self.facebook, self.twitter, self.instagram],
                                    self.post_id_instruction,
                                    [self.post_id_label, self.post_id_entry],
                                    self.post_id_status,
                                    [self.poster_label, self.poster_entry],
                                    self.reactions_widgets,
                                    self.update_button]

        show_widgets_in_consecutive_grids(self.default_widgets_list)
        
        # check if post id already exists
        self.update_post_id_status()

    def update_engagement_data(self):
        for reaction in self.reactions_widgets.get_reactions_list():
            print(reaction.get_count())

    def update_post_id_status(self):
        self.post_id_status["text"] = self.post_id_entry.get()
        self.after(100, self.update_post_id_status)
    
    def update_reactions_widgets(self):
        self.reactions_widgets.set_reactions_list(self.platform_choice.get())
        
def main():
    root = tk.Tk()
    
    root.resizable(False, False)
    root.title("Seeding Tracker")
    my_user_options = User_options(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()