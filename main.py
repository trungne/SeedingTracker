# libraries
import tkinter as tk
from PIL import ImageTk, Image

# other python files
from Reaction import *
from constants import *
import mysql_queries
import user_info

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
        mysql_queries.delete_post(self.platform, int(self.post_id_entry.get()))
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

        # name of the poster
        self.poster_label = tk.Label(self, text="Name: ")
        self.poster_entry = tk.Entry(self)
        
        # reaction widgets
        self.reactions_frame = Reaction_frame(self)

        # update button to update data to database
        self.update_button = tk.Button(self, text="Update", command=self.update_engagement_data)
        
        '''Show default widgets'''
        self.default_widgets_list = [self.instruction,
                                    [self.post_id_label, self.post_id_entry],
                                    [self.poster_label, self.poster_entry],
                                    self.reactions_frame,
                                    self.update_button]

        show_widgets_in_consecutive_grids(self.default_widgets_list)

    def update_engagement_data(self):
        post_id = self.post_id_entry.get()
        post_id_exists = self.check_post_id_status(post_id)
        employee_name = self.poster_entry.get()

        to_be_updated_columns = [post_id, employee_name]
        to_be_updated_columns.extend(self.reactions_frame.get_reactions_list())
        
        table = self.platform

        if not post_id or not employee_name or not to_be_updated_columns:
            self.instruction.config(text="Invalid input(s)!") # add more meaningful error message
        else:
            if post_id_exists:
                mysql_queries.update_values(table, to_be_updated_columns)
                self.instruction.config(text="Successful updates!")
            else:
                mysql_queries.insert_values(table, to_be_updated_columns)
                self.instruction.config(text="Successful insertion!")

    """a function to check if the entered post id already exists in the database"""
    ## TODO: return false values
    def check_post_id_status(self, entered_post_id):
        list_of_post_ids = mysql_queries.get_existing_post_ids(self.platform)
        if int(entered_post_id) in list_of_post_ids:
            # print("This will update your existing record")
            # update function
            return True
        else:
            # print("This will create a new record!")
            # create a new record
            return False

    def get_name(self):
        return self.name

    def change_platform(self, new_platform):
        if new_platform != self.platform:
            self.platform = new_platform
            self.reactions_frame.set_reactions_list(new_platform)

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

        self.password.bind('<Return>', self.login)
        self.password.bind('<KP_Enter>', self.login)
        self.login_id.bind('<Return>', self.login)
        self.login_id.bind('<KP_Enter>', self.login)

        show_widgets_in_consecutive_grids(self.widgets_list)

        self.count = 1
    def login(self, event=None):
        name = self.login_id.get()
        password = self.password.get()
        
        credentials = user_info.get_credentials()

        if name in credentials and password == credentials[name]:
            self.login_status.config(text="Successful")
            # load database at this point
            user_info.current_user = user_info.create_user(name)
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

    my_programe = Main_frame(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()