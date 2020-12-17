import mysql_queries

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        # self.password = None
        self.database = f"SeedingTracker{self.user_id}"
        
# convert a list of records into a dictionary of records
def convert_list_to_dict(records):
    my_dict = {}
    for each_user in records:
        name = str(each_user[0])
        password = str(each_user[1])
        my_dict[name] = password
    return my_dict

# get all usernames and passwords
def get_credentials():
    connection = mysql_queries.connect_to_database("SeedingTracker_Users")
    mycursor = connection.cursor()

    select_query = f"SELECT user_name, user_password FROM User_information"
    mycursor.execute(select_query)

    records = mycursor.fetchall() # return a list of records
    all_user_information = convert_list_to_dict(records) # convert the list to dict

    mycursor.close()
    connection.close()

    return all_user_information

# create a user object
def create_user(user_name):
    connection = mysql_queries.connect_to_database("SeedingTracker_Users")
    mycursor = connection.cursor()

    select_query = f"SELECT user_id, user_name FROM User_information WHERE user_name = '{user_name}'"

    mycursor.execute(select_query)
    user_info = mycursor.fetchone()

    user_id = str(user_info[0])
    user_name = str(user_info[1])

    mycursor.close()
    connection.close()

    return User(user_id, user_name)

current_user = None

        
