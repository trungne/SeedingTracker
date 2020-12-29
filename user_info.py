import constants
import mysql_queries

class User:
    def __init__(self, user_id, name, number_of_post):
        self.user_id = user_id
        self.name = name
        self.number_of_post = number_of_post
        # self.password = None

    def insert_values(self, table, post_id, to_be_updated_reactions):
        mysql_queries.insert_values(table, post_id, to_be_updated_columns)

    def get_name(self):
        return self.name
# create a user object
def create_user(_id):
    connection = mysql_queries.connect_to_database(constants.DATABASE)
    mycursor = connection.cursor()

    select_query = f"SELECT account_id, employee_name, number_of_post FROM Employee WHERE account_id = '{_id}'"

    mycursor.execute(select_query)
    user_info = mycursor.fetchone()

    user_id = str(user_info[0])
    user_name = str(user_info[1])

    if user_info:
        number_of_post = int(user_info[2])
    else:
        number_of_post = 0

    mycursor.close()
    connection.close()

    return User(user_id, user_name, number_of_post)

current_user = None
