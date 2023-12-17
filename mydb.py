import mysql.connector

dataBase = mysql.connector .connect(
    host ='localhost',
    user = 'root',
    passwd = 'Agile146658!'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE Trimex")

print ("all done")