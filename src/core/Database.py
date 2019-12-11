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
			"CREATE TABLE IF NOT EXISTS dados ("
			"	IDENTIFICADOR VARCHAR(64) NOT NULL,"
			"	DATA DATE NOT NULL,"
			"	DERIVATIVO VARCHAR(64) NOT NULL,"
			"	PARTICIPANTE VARCHAR(64) NOT NULL,"
			"	LONGCONTRACTS INT NOT NULL,"
			"	LONG_ DECIMAL(5,2) NOT NULL,"
			"	SHORTCONTRACTS INT NOT NULL,"
			"	SHORT_ DECIMAL(5,2) NOT NULL,"
			"	SALDO INT NOT NULL,"
			"	PRIMARY KEY(IDENTIFICADOR)"    
			");")
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS acumulado ("
			"	IDENTIFICADOR_ID VARCHAR(64) NOT NULL,"
			"	DATA DATE NOT NULL,"
			"	PARTICIPANTE VARCHAR(64) NOT NULL,"
			"	SALDO INT NOT NULL,"
			"	ACUMULADO BIGINT NOT NULL,"
			"	PRIMARY KEY(IDENTIFICADOR_ID),"
			"	FOREIGN KEY(IDENTIFICADOR_ID)"
			"	REFERENCES dados(IDENTIFICADOR)"			    
			");")			

	def insert_dados(self, all_data):
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
					"""INSERT IGNORE INTO dados (IDENTIFICADOR, DATA, DERIVATIVO, PARTICIPANTE, LONGCONTRACTS, LONG_, SHORTCONTRACTS, SHORT_, SALDO)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(value[0], date_mysql, value[2], value[3], value[4], value[5], value[6], value[7], value[8]))
			self.conn.commit()
		print("Dados inseridos com sucesso!")      
		
	def insert_acumulado(self, all_data):
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
					"""INSERT IGNORE INTO acumulado (IDENTIFICADOR, DATA, PARTICIPANTE, SALDO, ACUMULADO)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(value[0], date_mysql, value[2], value[3], value[4], value[5], value[6], value[7], value[8]))
			self.conn.commit()
		print("Dados inseridos com sucesso!")   

	def close(self):
		self.cursor.close()
		self.conn.close()