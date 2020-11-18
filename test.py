import mysql.connector
from mysql.connector import errorcode

try:
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        auth_plugin="mysql_native_password")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    print("Successful")
    cnx.close()
