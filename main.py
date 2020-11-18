import tkinter as tk
from PIL import ImageTk, Image
import csv
import pandas
import mysql.connector

def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

# def update_data_to_csv(reaction_list):
#     pass
# def update_data_to_mysql(reaction_list):
#     # reaction list is dict, key = reaction, value = count
#     try:
#         mydb = mysql.connector.connect(
#             host="localhost",
#             user="trung",
#             password="123zxc",
#             database="test"
#         )
#     except:
#         print("Cannot connect to MySQL database")
#         return 0;
#     else:
#         mycursor = mydb.cursor()
#         # engagement is the name of the table
#         for reaction in reaction_list:
#             my_command = f"UPDATE engagement SET {reaction}"

class Reaction:
    def __init__(self, name, root):
        # a string
        self.name = name

        # tk.Entry object
        self.entry = tk.Entry(root)
        self.entry.configure(validate="key")
        self.entry['validatecommand'] = (self.entry.register(testVal),'%P','%d') # set constraint to only int

        # tk.Label object
        self.label = tk.Label(root)
        self.label_image = ImageTk.PhotoImage(Image.open(f"./icons/{self.name}.png").resize((58, 58)))
        self.label.configure(image=self.label_image)
        
    def get_name(self):
        return self.name

    def get_count(self):
        return self.entry.get()

    def display_reaction(self, row, column):
        self.label.grid(row=row, column=column, pady=3, sticky='nesw')
        self.entry.grid(row=row, column=column+1, pady=3, columnspan=10, sticky='nesw')

    def destroy_reaction(self):
        self.label.grid_remove()
        self.entry.grid_remove()

def create_reactions(platform, root):
    reactions_list = []
    
    if platform == "facebook": # facebook
        fb_like = Reaction("fb_like", root)
        fb_heart = Reaction("fb_heart", root)
        fb_care = Reaction("fb_care", root)
        fb_haha = Reaction("fb_haha", root)
        fb_wow = Reaction("fb_wow", root)
        fb_sad = Reaction("fb_sad", root)
        fb_angry = Reaction("fb_angry", root)
        fb_comment = Reaction("fb_comment", root)
        fb_share = Reaction("fb_share", root)
        reactions_list = [fb_like, fb_heart, fb_care, fb_haha, fb_wow, fb_sad, fb_angry, fb_comment, fb_share]

    elif platform == "twitter": # twitter
        twitter_cmt = Reaction("twitter_cmt", root)
        twitter_retweet = Reaction("twitter_retweet", root)
        twitter_heart = Reaction("twitter_heart", root)
        reactions_list = [twitter_cmt, twitter_retweet, twitter_heart]

    elif platform == "instagram": # instagram
        instagram_cmt = Reaction("instagram_cmt", root)
        instagram_heart = Reaction("instagram_heart", root)
        reactions_list = [instagram_cmt, instagram_heart]
    
    return reactions_list

def show_reactions(reactions_list, cur_row):
    if not reactions_list:
        return 0
    
    for i in range(len(reactions_list)):
        reactions_list[i].display_reaction(cur_row, 0)
        cur_row += 1
    
    return cur_row

def destroy_reactions(reactions_list):
    if not reactions_list:
        return 0
    
    for i in range(len(reactions_list)):
        reactions_list[i].destroy_reaction()
    
class Manual(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # show the main frame
        self.pack()
        self.parent = parent

        self.current_reactions = []

        self.fb_icon = ImageTk.PhotoImage(Image.open("./icons/fb.png").resize((58, 58)))
        self.twitter_icon = ImageTk.PhotoImage(Image.open("./icons/twitter.png").resize((58, 58)))
        self.instagram_icon = ImageTk.PhotoImage(Image.open("./icons/instagram.png").resize((58, 58)))

        '''Default widgets'''
        # radiobuttons for platfrom choices
        self.platform_choice = tk.StringVar()
        #self.platform_choice.set("facebook")
        self.facebook = tk.Radiobutton(self, image=self.fb_icon, variable=self.platform_choice, value="facebook", command= self.update_reactions_widgets)
        self.twitter = tk.Radiobutton(self, image=self.twitter_icon, variable=self.platform_choice, value="twitter", command= self.update_reactions_widgets)
        self.instagram = tk.Radiobutton(self, image=self.instagram_icon, variable=self.platform_choice, value="instagram", command= self.update_reactions_widgets)
        
        # label as instruction for user
        self.instruction = tk.Label(self, text="Manually enter the engagement data for your post")
        
        # post_id widgets
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.post_id_status = tk.Label(self)

        '''Show default widgets'''
        self.facebook.grid(row=0, column=0)
        self.twitter.grid(row=0, column=1)
        self.instagram.grid(row=0, column=2)

        self.instruction.grid(row=1, columnspan=10)

        self.post_id_label.grid(row=2, column=0, pady=10, sticky='nesw')
        self.post_id_entry.grid(row=2, column=1, pady=10, columnspan=10, sticky='nesw')
        
        self.post_id_status.grid(row=3, columnspan=10)

        # update button to update data to database
        self.update_button = tk.Button(self, text="Update", command=self.update_engagement_data)
        self.view_button = tk.Button(self, text="View")

        # check if post id already exists
        self.update_post_id_status()

        # display reactions widgets accordingly to their platform
        self.update_reactions_widgets()

    def update_engagement_data(self):
        pass

    def update_post_id_status(self):
        self.post_id_status["text"] = self.post_id_entry.get()
        self.after(100, self.update_post_id_status)
    
    def update_reactions_widgets(self):
        # destroy old widgets
        destroy_reactions(self.current_reactions)
        self.update_button.grid_remove()

        self.current_reactions = create_reactions(self.platform_choice.get(), self)
        cur_row = show_reactions(self.current_reactions, 4)

        if not self.current_reactions:
            cur_row = 4
        self.update_button.grid(row=cur_row, column=0, columnspan=10)
        self.view_button.grid(row=cur_row, column=2, columnspan=10)

def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Seeding Tracker")

    Manual_window = Manual(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()