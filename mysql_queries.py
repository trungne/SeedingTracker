import mysql.connector
import time
from constants import *
import user_info

localtime = time.asctime(time.localtime(time.time()))
print(localtime)

def list_to_cs_string(lst):
    cs_string = ""
    length = len(lst)
    for i in range(length):
        if i == (length - 1): # if i is the last index
            cs_string += f"{str(lst[i])}"
        else:
            cs_string += f"{str(lst[i])}, "
    return cs_string

def platform_post_ID(table):
    if table == "Facebook":
        return "fb_post_ID"
    elif table == "Twitter":
        return "twitter_post_ID"
    elif table == "Instagram":
        return "instagram_post_ID"

# https://www.programiz.com/python-programming/datetime/current-time

# https://stackoverflow.com/questions/5504340/python-mysqldb-connection-close-vs-cursor-close
def connect_to_database(db):
    try:
        connection = mysql.connector.connect(
        host="localhost",
        user="root",
        auth_plugin="mysql_native_password",
        database=db)

    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False
    else:
        pass
        # print("Successful")

    return connection

# return a list of existing post id of a platform
# Note: table = platform
def get_existing_post_ids(table):
    list_of_ids = []
    connection = connect_to_database("SeedingTracker1")
    # connection = connect_to_database(user_info.current_user.database)
    mycursor = connection.cursor()
    query_statement = f"SELECT {platform_post_ID(table)} FROM {table}"
    mycursor.execute(query_statement)

    records = mycursor.fetchall()
    length = len(records)
    for i in range(length):
        list_of_ids.append(records[i][0])

    mycursor.close()
    connection.close()
    return list_of_ids

def query_post(table, post_id):
    pass

def delete_post(table, post_id):
    connection = connect_to_database(user_info.current_user.database)
    mycursor = connection.cursor()

    delete_stmt = f"DELETE FROM {table} WHERE {platform_post_ID(table)} = {post_id}"
    mycursor.execute(delete_stmt)
    connection.commit()
    
    # print(delete_stmt)

    mycursor.close()
    connection.close()

def update_values(table, to_be_updated_reactions):
    connection = connect_to_database(user_info.current_user.database)
    mycursor = connection.cursor()

    post_id = to_be_updated_reactions[0]
    employee_name = to_be_updated_reactions[1]
    length = len(to_be_updated_reactions)

    # start at 2 to skip updating post ip and employee's name
    for i in range(2, length):
        column = to_be_updated_reactions[i].get_name()
        value = to_be_updated_reactions[i].get_count()

        update_stmt = f"UPDATE {table} SET {column} = {value} WHERE {platform_post_ID(table)} = {post_id}"
        # print(update_stmt)

        mycursor.execute(update_stmt)
        connection.commit()
    
    mycursor.close()
    connection.close()

def insert_values(table, to_be_updated_columns):
    connection = connect_to_database(user_info.current_user.database)
    if connection == False:
        return False
    
    mycursor = connection.cursor()

    post_id = to_be_updated_columns[0]
    employee_name = to_be_updated_columns[1]

    columns = [platform_post_ID(table), "employee_name"]
    values = [post_id, f"'{employee_name}'"]

    for each_reaction in to_be_updated_columns[2:]:
        name = each_reaction.get_name()
        count = each_reaction.get_count()

        columns.append(name)
        values.append(count)
    
    columns = list_to_cs_string(columns)
    values = list_to_cs_string(values)

    insert_smt = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    # print(insert_smt)

    mycursor.execute(insert_smt)
    connection.commit()

    mycursor.close()
    connection.close()

    return True

def main():
    get_existing_post_ids("Facebook")

if __name__ == "__main__":
    main()



