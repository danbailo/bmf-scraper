import mysql.connector
import re
import datetime

class Database:
	def __init__(self, user=None, password=None, database=None, host="127.0.0.1", port="3306"):
		if user is None:
			print("Por favor, entre com usuario e senha!")
			exit(-1)
		if password is None:
			print("Por favor, entre com usuario e senha!")
			exit(-1)            
		self.conn = mysql.connector.connect(
			user=user,
			passwd=password,
			host=host,
			port=port
		)
		print("Conectado ao banco de dados com sucesso!")
		self.cursor = self.conn.cursor()
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS {database};".format(database=database))
		self.cursor.execute("USE {database};".format(database=database))
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS DADOS ("
			"  IDENTIFICADOR VARCHAR(64) NOT NULL,"
			"  DATA DATE NOT NULL,"
			"  DERIVATIVO VARCHAR(64) NOT NULL,"
			"  PARTICIPANTE VARCHAR(64) NOT NULL,"
			"  LONGCONTRACTS DECIMAL(11,5) NOT NULL,"
			"  LONG_ DECIMAL(5,2) NOT NULL,"
			"  SHORTCONTRACTS DECIMAL(11,5) NOT NULL,"
			"  SHORT_ DECIMAL(5,2) NOT NULL,"
			"  SALDO DECIMAL(30,20) NOT NULL,"
			"  PRIMARY KEY(IDENTIFICADOR)"    
			");")
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS ACUMULADO ("
			"  IDENTIFICADOR VARCHAR(64) NOT NULL,"
			"  DATA DATE NOT NULL,"
			"  DERIVATIVO VARCHAR(64) NOT NULL,"
			"  PARTICIPANTE VARCHAR(64) NOT NULL,"
			"  SALDO DECIMAL(30,20) NOT NULL,"
			"  ACUMULADO DECIMAL(30,20) NOT NULL,"
			"  PRIMARY KEY(IDENTIFICADOR)"    
			");")			

	def insert_data(self, all_data):
		for _, rows in all_data.items():
			temp = []
			for row in rows.values():
				temp.append(row)
			data = list(zip(*temp))
			for value in data:
				date = value[1].split("/")
				day = int(date[0])
				month = int(date[1])
				if month > 12:
					month = 12
				year = int(date[2])
				date_mysql = datetime.datetime(year, month, day)
				self.cursor.execute(
					"""INSERT IGNORE INTO DADOS (IDENTIFICADOR, DATA, DERIVATIVO, PARTICIPANTE, LONGCONTRACTS, LONG_, SHORTCONTRACTS, SHORT_, SALDO)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(value[0], date_mysql, value[2], value[3], value[4].replace(",", ""), value[5], value[6].replace(",", ""), value[7], value[8]))
			self.conn.commit()
		print("Dados inseridos com sucesso!")      
		
	def close(self):
		self.cursor.close()
		self.conn.close()