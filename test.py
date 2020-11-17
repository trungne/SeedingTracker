import mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user="trung",
        passwd=r"123zxc",
        db = "mydatabase",
        port=3306,
        auth_plugin="mysql_native_password"
    )