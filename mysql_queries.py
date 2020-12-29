import mysql.connector
import time
import constants

localtime = time.asctime(time.localtime(time.time()))
print(localtime)

# convert a list to a comma-separated string.
"""
This function is used to create mysql insert/update statement
Input: a list of items to be updated or inserted
Output: a string which contains all the items, each of which is separated by a comma
"""
def list_to_cs_string(lst):
    cs_string = ""
    length = len(lst)
    for i in range(length):
        if i == (length - 1): # if i is the last index
            cs_string += f"{str(lst[i])}"
        else:
            cs_string += f"{str(lst[i])}, "
    return cs_string

# https://www.programiz.com/python-programming/datetime/current-time

# https://stackoverflow.com/questions/5504340/python-mysqldb-connection-close-vs-cursor-close

def mysql_varchar(value):
    return f"'{value}'"

"""
This function is to connect to the database in mysql
Input: the database name
Output: a connection object to the database
The connection object is then used to create a cursor which will execute mysql statement
"""
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

# return a list of existing post id of a platform a.k.a Facebook, Twitter, Instagram
# Note: table = platform
def get_existing_post_ids(table):
    list_of_ids = []
    connection = connect_to_database(constants.DATABASE)
    
    mycursor = connection.cursor()

    # select ALL post ids
    query_statement = f"SELECT post_id FROM {table}"

    mycursor.execute(query_statement)

    records = mycursor.fetchall()

    length = len(records)
    for i in range(length):
        list_of_ids.append(records[i][0])

    # close the connection
    mycursor.close()
    connection.close()

    return list_of_ids


def query_post(table, post_id):
    pass

def delete_post(table, post_id):
    # connect to the database
    connection = connect_to_database(constants.DATABASE)
    mycursor = connection.cursor()

    # create the delete statement
    delete_stmt = f"DELETE FROM {table} WHERE post_id = {mysql_varchar(post_id)}"
    
    # execute the statement
    mycursor.execute(delete_stmt)
    connection.commit()
    
    # close the connection
    mycursor.close()
    connection.close()

def get_employee_name(table, post_id):
    # connect to the database
    connection = connect_to_database(constants.DATABASE)
    mycursor = connection.cursor()

    # create the query statement to find the name of the employee of a post id
    query = f"SELECT employee_name FROM {table} WHERE post_id = {mysql_varchar(post_id)}"
    
    # execute the query
    mycursor.execute(query)

    # catch the return value
    employee_name = mycursor.fetchone() # employee_name is a tuple   

    # close the connection
    mycursor.close()
    connection.close()

    # only return the name, which is the first item in the tuple
    return employee_name[0]

def update_values(table, post_id, employee_name, to_be_updated_reactions):
    # total items in the provided list
    length = len(to_be_updated_reactions)

    # connect to the database
    connection = connect_to_database(constants.DATABASE)
    mycursor = connection.cursor()

    # only update employee name if the current name and the new name are different
    if employee_name != get_employee_name(table, post_id):
        update_stmt = f"UPDATE {table} SET employee_name = {mysql_varchar(employee_name)} WHERE post_id = {mysql_varchar(post_id)}"
        mycursor.execute(update_stmt)
        connection.commit()

    for i in range(length):
        # generate column and according value to update
        column = to_be_updated_reactions[i].get_name()
        value = to_be_updated_reactions[i].get_count()

        # TODO: only update columns that have different values, ignore values with the same value

        # generate update statement for each index a.k.a each column and its value
        update_stmt = f"UPDATE {table} SET {column} = {value} WHERE post_id = {post_id}"

        # update EACH column, one by one
        mycursor.execute(update_stmt)
        connection.commit()
    
    mycursor.close()
    connection.close()

def insert_values(table, post_id, employee_name, to_be_updated_reactions):
    # column_and_value_pairs 
    
    columns = ["post_id", "employee_name"]
    values = [mysql_varchar(post_id), mysql_varchar(employee_name)]
    
    # generate a list of columns and their according values
    for each_reaction in to_be_updated_reactions:
        name = each_reaction.get_name()
        count = each_reaction.get_count()

        columns.append(name)
        values.append(count)
    print(f"columns = {columns}")
    print(f"values = {values}")
    # convert the previously generated lists to comma-separated strings
    columns = list_to_cs_string(columns)
    values = list_to_cs_string(values)

    # generate insert statement from the columns and their corresponding values
    insert_smt = f"INSERT INTO {table} ({columns}) VALUES ({values})"
    print(insert_smt)
    # open connection to database
    connection = connect_to_database(constants.DATABASE)
    mycursor = connection.cursor()

    # execute the insert statement
    mycursor.execute(insert_smt)
    connection.commit()

    # explicitly close the connection
    mycursor.close()
    connection.close()

def post_id_is_in_table(entered_post_id, table):
    list_of_post_ids = get_existing_post_ids(table)
    if entered_post_id in list_of_post_ids:
        return True
    else:
        return False


def create_column_and_value_pairs(post_id, employee_name, to_be_updated_reactions):
    pairs = {"post_id": post_id,
            "employee_name": employee_name}
            

def main():
    get_employee_name("Facebook", "1")

    
if __name__ == "__main__":
    main()



