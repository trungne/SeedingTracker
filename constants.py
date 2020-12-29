import mysql_queries

# convert a list of records into a dictionary of records
def convert_list_to_dict(records):
    my_dict = {}
    for each_user in records:
        account_id = str(each_user[0])
        password = str(each_user[1])
        my_dict[account_id] = password
    return my_dict

# get all usernames and passwords from the database
def get_credentials():
    connection = mysql_queries.connect_to_database(DATABASE)
    mycursor = connection.cursor()

    select_query = f"SELECT account_id, password FROM Employee"
    mycursor.execute(select_query)

    records = mycursor.fetchall() # return a list of records
    all_user_information = convert_list_to_dict(records) # convert the list to dict
    mycursor.close()
    connection.close()
    return all_user_information

MAX_COLUMN_RANGE = 10
DEFAULT_PAD_Y = 4
DATABASE = "SeedingTracker"
ALL_CREDENTIALS_IN_DATABASE = get_credentials()


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

