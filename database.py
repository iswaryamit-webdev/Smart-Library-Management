import mysql.connector
conn=mysql.connector.connect(host="localhost",user="root",password="Iswarya@2006",database="library_dB")
cursor=conn.cursor()
print("Database connected")