import tkinter as tk
from PIL import ImageTk, Image
import csv

import mysql.connector

def testVal(inStr,acttyp):
            if acttyp == '1': #insert
                if not inStr.isdigit():
                    return False
            return True

def update_data_to_csv(reaction_list):
    pass
def update_data_to_mysql(reaction_list):
    # reaction list is dict, key = reaction, value = count
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="trung",
            password="123zxc",
            database="s3818328"
        )
    except:
        print("Cannot connect to MySQL database")
        return 0;
    else:
        mycursor = mydb.cursor()
        # engagement is the name of the table
        for reaction in reaction_list:
            my_command = f"UPDATE engagement SET {reaction}"

class Reaction:
    def __init__(self, name, icon, count=0):
        self.name = name
        self.icon = icon
        self.count = count

    def get_name(self):
        return self.name

    def get_icon(self):
        return self.icon

    def get_count(self):
        return self.count
        
class Manual(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # show the main frame
        self.pack()
        self.parent = parent

        # create main widgets
        self.instruction = tk.Label(self, text="Manually enter the engagement data for your post")

        # post id widgets
        self.post_id_entry = tk.Entry(self)
        self.post_id_label = tk.Label(self, text="Post ID: ")
        self.post_id_status = tk.Label(self)

        # icons
        self.like_img = ImageTk.PhotoImage(Image.open("./icons/like.png"))
        self.heart_img = ImageTk.PhotoImage(Image.open("./icons/heart.png"))
        self.care_img = ImageTk.PhotoImage(Image.open("./icons/care.png"))
        self.haha_img = ImageTk.PhotoImage(Image.open("./icons/haha.png"))
        self.wow_img = ImageTk.PhotoImage(Image.open("./icons/wow.png"))
        self.sad_img = ImageTk.PhotoImage(Image.open("./icons/sad.png"))
        self.angry_img = ImageTk.PhotoImage(Image.open("./icons/angry.png"))

        # reactions widgets
        self.likes = Reaction("likes", self.like_img, )

        self.like_entry = tk.Entry(self, validate="key")
        self.like_icon = tk.Label(self, image=self.like_img)

        self.heart_entry = tk.Entry(self, validate="key")
        self.heart_icon = tk.Label(self, image=self.heart_img)

        self.care_entry = tk.Entry(self, validate="key")
        self.care_icon = tk.Label(self, image=self.care_img)

        self.haha_entry = tk.Entry(self, validate="key")
        self.haha_icon = tk.Label(self, image=self.haha_img)

        self.wow_entry = tk.Entry(self, validate="key")
        self.wow_icon = tk.Label(self, image=self.wow_img)

        self.sad_entry = tk.Entry(self, validate="key")
        self.sad_icon = tk.Label(self, image=self.sad_img)

        self.angry_entry = tk.Entry(self, validate="key") 
        self.angry_icon = tk.Label(self, image=self.angry_img)

        # 7 reactions entries and icons
        self.list_of_reaction_entries = [
            self.like_entry, 
            self.heart_entry,
            self.care_entry,
            self.haha_entry,
            self.wow_entry,
            self.sad_entry,
            self.angry_entry
            ]

        self.list_of_reaction_icons = [
            self.like_icon,
            self.heart_icon,
            self.care_icon,
            self.haha_icon,
            self.wow_icon,
            self.sad_icon,
            self.angry_icon
        ]

        self.reactions = {
            "likes": 0,
            "hearts" : 0,
            "care": 0,
            "haha": 0,
            "wow": 0,
            "sad": 0,
            "angry": 0
        }

        self.update_button = tk.Button(self, text="Update", command=self.update_engagement_data)
    def show_widgets(self):
        # show main widgets
        self.instruction.grid(row=0, columnspan=2)

        self.post_id_entry.grid(row=1, column=1, sticky='nesw')
        self.post_id_label.grid(row=1, column=0, sticky='nesw')
        self.post_id_status.grid(row=2, columnspan=2)

        cur_row = 3
        for i in range(len(self.list_of_reaction_entries)):
            self.list_of_reaction_icons[i].grid(row=cur_row, column=0,sticky='nesw')
            self.list_of_reaction_entries[i].grid(row=cur_row, column=1, sticky='nesw')

            # set constraint for each entry
            self.list_of_reaction_entries[i]['validatecommand'] = (self.list_of_reaction_entries[i].register(testVal),'%P','%d')
            cur_row += 1
        self.update_button.grid(row=cur_row, columnspan=2)

    def update_engagement_data(self):
        self.reactions["likes"] = self.like_entry.get()
        self.reactions["hearts"] = self.heart_entry.get()
        self.reactions["care"] = self.care_entry.get()
        self.reactions["haha"] = self.haha_entry.get()
        self.reactions["wow"] = self.wow_entry.get()
        self.reactions["sad"] = self.sad_entry.get()
        self.reactions["angry"] = self.angry_entry.get()
        update_data_to_mysql(self.reactions)
def main():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Seeding Tracker")

    Manual_window = Manual(root)
    Manual_window.show_widgets()
    root.mainloop()

if __name__ == "__main__":
    main()