import mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=r"123zxc",
        database = "mydatabase",
        auth_plugin="mysql_native_password"
    )