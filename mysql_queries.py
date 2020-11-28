import mysql.connector
from mysql.connector import errorcode
import time
localtime = time.asctime(time.localtime(time.time()))
print(localtime)

# https://www.programiz.com/python-programming/datetime/current-time
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
