import mysql.connector
from mysql.connector import Error
from os import name,system
from getpass import getpass
def clear():
        if name=="nt":
            _=system('cls')
        if name=='posix':
            _=system('clear')
def database_query(host1,user1,password1,database1,query):
		try:
				mydb = mysql.connector.connect(
					host=host1,
					user=user1,
					password=password1,
					database=database1)

				mycursor = mydb.cursor()
				mycursor.execute(query)
				if "show" in query:
						for x in mycursor:
							print(x)
				if "create" in query:
					print("Database is created.")
				if "drop" in query:
					print("Database drop is successful.")
		except Error as e:
			print("Error :",e)
def table_query(host1,user1,password1,database1,query):
	try :
		mydb = mysql.connector.connect(
			host=host1,
			user=user1,
			password=password1,
			database=database1
		)

		mycursor = mydb.cursor()
		mycursor.execute(query)
		if "create" in query or "CREATE" in query:
			print("Table is created.")
		elif "show" in query or "SHOW" in query:
			print("Tables in Database :")
			for x in mycursor:
				print(x)
		elif "drop" in query or "DROP" in query:
			print("Dropping table is susccesful")
		elif "alter" in query or "ALTER" in query:
			print("Table altered successfully")
	
	except Error as e:
		print("Error - ",e)
	

def select_query(host1,user1,password1,database1,sql1):
		try:
				connection=mysql.connector.connect(host=host1,database=database1,charset='utf8',user=user1,password=password1)
				print("Database connected")
				cursor = connection.cursor()
				print(type(cursor))
				cursor.execute(sql1)
				records = cursor.fetchall()
				print("Total number of rows are: ", cursor.rowcount)
				for row in records:
					print(row)
		except Error as e:
			print("Error reading data from MySQL table", e)
			connection.close()
			cursor.close()
			
def insert_query(host1,user1,password1,database1,sql1):

		try:
				mydb = mysql.connector.connect(host=host1,database=database1,charset='utf8',user=user1,password=password1)
				mycursor = mydb.cursor()
				mycursor.execute(sql1)
				mydb.commit()
				print(mycursor.rowcount, "was inserted.")
		except Error as e:
				print("Error reading data from MySQL table", e)
		finally:
				if mydb.is_connected():
					mydb.close()
def update_query(host1,user1,password1,database1,sql1):
	try :
		mydb = mysql.connector.connect(
		host=host1,
		user=user1,
		password=password1,
		database=database1
		)

		mycursor = mydb.cursor()

		mycursor.execute(sql1)

		mydb.commit()

		print(mycursor.rowcount, "record(s) affected")  
	except Error as e:
		print("Error :",e)
	finally:
					if mydb.is_connected():
						mydb.close()
					
def delete_query(host1,user1,password1,database1,sql1):
	try:
		mydb = mysql.connector.connect(host=host1,user=user1,password=password1,database=database1)

		mycursor = mydb.cursor()

		mycursor.execute(sql1)

		mydb.commit()

		print(mycursor.rowcount, "record(s) deleted")
		mydb.close()
		
	except Error as e:
		print("Error :",e)
	finally:
		if mydb.is_connected():
			mydb.close()
def about():
	print("AUTHOR : https://www.linkedin.com/in/srinadh-ch-887550232/")


def start_mysql():
	print("AUTHOR : https://www.linkedin.com/in/srinadh-ch-887550232/")
	host=input("Host Name :")
	user=input("User Name :")
	password=getpass("Password : ")
	database=input("Database Name :")
	try :
		mydb = mysql.connector.connect(host=host,user=user,password=password,database=database)
		if mydb.is_connected():
				mydb.close()
		while True:
			sql_query=input("query >")
			if "insert" in sql_query or "INSERT" in sql_query:
				insert_query(host,user,password,database,sql_query)
			elif "select" in sql_query or "SELECT" in sql_query:
				select_query(host,user,password,database,sql_query)
			elif "delete" in sql_query or "DELETE" in sql_query:
				delete_query(host,user,password,database,sql_query)
			elif "database" in sql_query or "DATABASE" in sql_query:
				database_query(host,user,password,database,sql_query)
			elif "table" in sql_query or "TABLE" in sql_query:
				table_query(host,user,password,database,sql_query)
			elif "update" in sql_query or "UPDATE" in sql_query:
				update_query(host,user,password,database,sql_query)
			elif "clear" in sql_query:
				clear()
			elif "author" in sql_query or 'about' in sql_query:
				about()
			elif "exit" in sql_query:
				print("query > Returning.")
				exit(0)
			elif sql_query=="":
				pass
			else :
				print("query > Inavalid")
	except Error as e:
		print("->",e)
		exit(0)
start_mysql()


		

