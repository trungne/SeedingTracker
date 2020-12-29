# libraries
import tkinter as tk
from PIL import ImageTk, Image

# other python files
from Reaction import *
import constants
import mysql_queries
import user_info

# ask for user confirmation

class Confirmation:
    def __init__(self, master, confirm_text):
        self.window = tk.Toplevel(master)
        self.window.resizable(False, False)
        self.window.title("Warning!")
        self.confirmation = False

        self.label = tk.Label(self.window, text=confirm_text)
        self.no_button = tk.Button(self.window, text="No", command=self.no)
        self.yes_button = tk.Button(self.window, text="Yes", command=self.yes)
        
        self.label.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.no_button.grid(row=1, column=0)
        self.yes_button.grid(row=1, column=1)

    def yes(self):
        self.confirmation = True
    def no(self):
        self.confirmation = False

    def show(self):
        self.window.deiconify()
        self.window.wait_window()
        return self.confirmation
def get_confirmation(master, text):
    Confirmation(master, text)
    return get_confirmation

class User_options(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack()
        self.parent = parent

        """Menu choice widgets """
        self.menu_prompt_label = tk.Label(self, text=f"Hi {user_info.current_user.name}! What do you want to do?")

        self.menu_choice = tk.StringVar()
        self.menu_choice_update = tk.Radiobutton(self, text="Update", variable=self.menu_choice, value="Update", 
                                                command=self.apply_menu_choice)
        self.menu_choice_query = tk.Radiobutton(self, text="Query", variable=self.menu_choice, value="Query", 
                                                command=self.apply_menu_choice)
        self.menu_choice_delete = tk.Radiobutton(self, text="Delete", variable=self.menu_choice, value="Delete", 
                                                command=self.apply_menu_choice)
        self.menu_choice_update.select()

        # declare 3 main menus
        self.my_update_menu = Update_menu(self.parent)
        self.my_query_menu = Query_menu(self.parent)
        self.my_delete_menu = Delete_menu(self.parent)

        # set the update menu as default menu
        self.current_menu = self.my_update_menu

        """Platform choice widgets """
        self.instruction_platform = tk.Label(self, text="Please choose your platform")
        
        # images for 3 platforms
        self.fb_icon = ImageTk.PhotoImage(Image.open("./icons/fb.png").resize((58, 58)))
        self.twitter_icon = ImageTk.PhotoImage(Image.open("./icons/twitter.png").resize((58, 58)))   
        self.instagram_icon = ImageTk.PhotoImage(Image.open("./icons/instagram.png").resize((58, 58)))
        
        self.platform_choice = tk.StringVar()

        self.facebook = tk.Radiobutton(self, image=self.fb_icon, variable=self.platform_choice, value="Facebook", 
                                        command= self.apply_platform_change)
        self.twitter = tk.Radiobutton(self, image=self.twitter_icon, variable=self.platform_choice, value="Twitter", 
                                        command= self.apply_platform_change)
        self.instagram = tk.Radiobutton(self, image=self.instagram_icon, variable=self.platform_choice, value="Instagram", 
                                        command= self.apply_platform_change)
        
        # set facebook as a default platform
        self.facebook.select()

        """List of all widgets to be displayed"""
        self.widgets_list = [self.menu_prompt_label, 
                            [self.menu_choice_update, self.menu_choice_query, self.menu_choice_delete],
                            self.instruction_platform,
                            [self.facebook, self.twitter, self.instagram]]
        # all of the widgets are displayed on User_options frame, not the root
        show_widgets_in_consecutive_grids(self.widgets_list)    

        # display the current menu below all the widgets    
        self.current_menu.pack()

    def get_current_platform(self):
        return self.platform_choice.get()

    def apply_menu_choice(self):
        menu_choice = self.menu_choice.get()
        # if the new menu == current one, do nothing!
        if menu_choice != self.current_menu.get_name():
            # else, delete the current menu before applying the new menu
            self.current_menu.pack_forget()

            # set the current menu accordingly to the user choice
            if menu_choice == "Update":
                self.current_menu = self.my_update_menu
            elif menu_choice == "Query":
                self.current_menu = self.my_query_menu
            elif menu_choice == "Delete":
                self.current_menu = self.my_delete_menu
            
            self.current_menu.change_platform(self.platform_choice.get())

            # display the menu, the menu is displayed onto the root, just like User_options
            # they are NOT displayed on the users option frame
            self.current_menu.pack()

    def apply_platform_change(self):
        new_platform = self.platform_choice.get()
        self.current_menu.change_platform(new_platform)

class Delete_menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Delete"
        self.platform = None
        self.parent = parent
        self.instruction = tk.Label(self, text="Please enter the post id")
        
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_post)
        self.widgets_list = [self.instruction,
                            [self.post_id_label, self.post_id_entry],
                            self.delete_button]

        show_widgets_in_consecutive_grids(self.widgets_list)
    def get_name(self):
            return self.name

    def change_platform(self, new_platform):
        if new_platform != self.platform:
            # do something
            self.platform = new_platform

    def delete_post(self):
        # pop up windows to ask for user last confirmation
        get_confirmation(self, "Are you sure?")
        mysql_queries.delete_post(self.platform, self.post_id_entry.get())

class Query_menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Query"
        self.platform = None
        self.parent = parent
        self.instruction = tk.Label(self, text="Please enter the post id")
        
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.query_button = tk.Button(self, text="Query")
        
        # TODO: create query features!
        
        
        self.widgets_list = [self.instruction,
                            [self.post_id_label, self.post_id_entry],
                            self.query_button]
        
        # show widgets
        show_widgets_in_consecutive_grids(self.widgets_list)
    def get_name(self):
        return self.name   

    def change_platform(self, new_platform):
        if new_platform != self.platform:
            # do something
            self.platform = new_platform

class Update_menu(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.name = "Update"
        
        '''Default widgets'''
        # string that indicates the current platform/table
        self.platform = "Facebook" # default platform is Facebook
        # label as instruction for user
        self.instruction = tk.Label(self, text="Enter your post ID")
        
        # post_id widgets
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")

        # # name of the poster
        # self.poster_label = tk.Label(self, text="Name: ")
        # self.poster_entry = tk.Entry(self)
        
        # reaction widgets
        self.reactions_frame = Reaction_frame(self)

        # update button to update data to database
        self.update_button = tk.Button(self, text="Update", command=self.update_engagement_data)
        
        '''Show default widgets'''
        self.default_widgets_list = [self.instruction,
                                    [self.post_id_label, self.post_id_entry],
                                    self.reactions_frame,
                                    self.update_button]

        show_widgets_in_consecutive_grids(self.default_widgets_list)

    def validate_inputs(self):
        if not self.post_id_entry.get():
            self.instruction.config(text="Please enter the post id!") # add more meaningful error message
            return False
        elif not self.reactions_frame.get_valid_reactions_list():
            self.instruction.config(text="Please enter engagement data!") # add more meaningful error message
            return False
        else:
            return True

    def update_engagement_data(self):
        # check if user has entered valid inputs
        if not self.validate_inputs():
            return None
        
        # get a list of reactions that will be updated/inserted values
        to_be_updated_reactions = self.reactions_frame.get_valid_reactions_list()
        
        # assign platform/post_id/employee_name to table for readability
        table = self.platform
        post_id = self.post_id_entry.get()
        employee_name = user_info.current_user.get_name()

        # if post id exists, UPDATE the values
        if mysql_queries.post_id_is_in_table(post_id, table):
            mysql_queries.update_values(table, post_id, employee_name, to_be_updated_reactions)
            self.instruction.config(text="Successful updates!")
        # if post id DOES NOT exists, INSERT the values
        else:
            mysql_queries.insert_values(table, post_id, employee_name, to_be_updated_reactions)
            self.instruction.config(text="Successful insertion!")

    def get_name(self):
        return self.name

    def change_platform(self, new_platform):
        if new_platform != self.platform:
            self.platform = new_platform
            self.reactions_frame.set_reactions_list(new_platform)


# This is a place to init user and database
class Login_menu(tk.Frame):
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

        """ bind the event (enter key being press) with a function (self.login)
        If the event happens, it will automatically trigger the function/        
        """
        self.password.bind('<Return>', self.login)
        self.password.bind('<KP_Enter>', self.login)
        self.login_id.bind('<Return>', self.login)
        self.login_id.bind('<KP_Enter>', self.login)

        show_widgets_in_consecutive_grids(self.widgets_list)

        self.count = 1
        
    """login is a function that check if 
    the pair of username and passwork entered 
    are in the database
    """
    def login(self, event=None):
        account_id = self.login_id.get()
        password = self.password.get()
        
        if (account_id in constants.ALL_CREDENTIALS_IN_DATABASE and 
            password == constants.ALL_CREDENTIALS_IN_DATABASE[account_id]):
            # display the result - successful login 
            self.login_status.config(text="Successful")

            # load database at this point
            user_info.current_user = user_info.create_user(account_id)

            self.parent.change(User_options)
        else:
            if self.count >= 3:
                self.parent.quit()

            self.login_status.config(text=f"Wrong ID or Password! ({self.count})")
            self.count += 1

     
class Main_frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.frame = Login_menu(self) # default frame is the login page
        self.frame.pack()
        self.pack()

    def change(self, frame):
        self.frame.pack_forget() # delete current frame
        self.frame = frame(self) # set current frame
        self.frame.pack() # display current frame

def main():
    root = tk.Tk()
    
    root.resizable(False, False)
    root.title("Seeding Tracker")

    Main_frame(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()