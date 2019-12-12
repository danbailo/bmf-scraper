from collections import defaultdict
import mysql.connector
import datetime
import os
import re

class Database:
	def __init__(self):
		pass
	
	def get_config(self, path=os.path.join("..", "inputs", "db_config.txt")):
		config = []
		with open(path) as file:
			for line in file:
				try:
					config.append(re.match(r".*: (.*)", line)[1])
				except TypeError:
					config.append("")
		return config

	def connect(self, config):
		user = config[0]
		password = config[1]
		database = config[2]
		host = config[3]
		port = config[4]

		if user == "":
			print("Por favor, insira o usuário do banco de dados no arquivo de configuração!")
			exit(-1)

		if database == "":
			print("Por favor, insira o nome do banco de dados no arquivo de configuração!")
			exit(-1)			

		if host == "":
			host = "127.0.0.1"

		if port == "":
			port = "3306"

		try:
			self.conn = mysql.connector.connect(
				user=user,
				passwd=password,
				database=database,
				host=host,
				port=port
			)
			self.cursor = self.conn.cursor()
		except mysql.connector.errors.ProgrammingError:
			self.conn = mysql.connector.connect(
				user=user,
				passwd=password,
				host=host,
				port=port
			)
			self.cursor = self.conn.cursor()
			try:
				self.cursor.execute("CREATE DATABASE IF NOT EXISTS {database};".format(database=database))	
				self.cursor.execute("USE {database};".format(database=database))
			except Exception:
				print("\nERRO tentar se conectar ao banco de dados!")
				print("Por favor, instale o banco de dados que foi disponibilizado no arquivo README.md ou verifique os dados e tente novamente!")
				exit(-1)			

		print("\nConectado ao banco de dados com sucesso!")

	def create_tables(self):
		self.cursor.execute(
			"CREATE TABLE IF NOT EXISTS derivatives_contratos ("
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
			"CREATE TABLE IF NOT EXISTS derivatives_acumulado ("
			"	IDENTIFICADOR_ID VARCHAR(64) NOT NULL,"
			"	DATA DATE NOT NULL,"
			"	PARTICIPANTE VARCHAR(64) NOT NULL,"
			"	SALDO INT NOT NULL,"
			"	ACUMULADO BIGINT NOT NULL,"
			"	PRIMARY KEY(IDENTIFICADOR_ID),"
			"	FOREIGN KEY(IDENTIFICADOR_ID)"
			"	REFERENCES derivatives_contratos(IDENTIFICADOR)"			    
			");")

	def insert_derivatives_contratos(self, all_data):
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
					"""INSERT IGNORE INTO derivatives_contratos (IDENTIFICADOR, DATA, DERIVATIVO, PARTICIPANTE, LONGCONTRACTS, LONG_, SHORTCONTRACTS, SHORT_, SALDO)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(value[0], date_mysql, value[2], value[3], value[4], value[5], value[6], value[7], value[8]))
			self.conn.commit()
		print('\nDados inseridos com sucesso na tabela "derivatives_contratos"!') 
		
	def insert_derivatives_acumulado(self, all_data):
		for _, rows in all_data.items():
			accumulated = defaultdict(int)
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
				accumulated[value[3]] += value[8]
				self.cursor.execute(
					"""INSERT IGNORE INTO derivatives_acumulado (IDENTIFICADOR_ID, DATA, PARTICIPANTE, SALDO, ACUMULADO)
					VALUES (%s, %s, %s, %s, %s)""",
					(value[0], date_mysql, value[3], value[8], accumulated[value[3]]))
			self.conn.commit()
		print('Dados inseridos com sucesso na tabela "derivatives_acumulado"!') 

	def truncate_tables(self):
		self.cursor.execute("DROP TABLE IF EXISTS derivatives_acumulado")
		self.cursor.execute("DROP TABLE IF EXISTS derivatives_contratos")
		self.cursor.execute(
			"CREATE TABLE derivatives_contratos ("
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
			"CREATE TABLE derivatives_acumulado ("
			"	IDENTIFICADOR_ID VARCHAR(64) NOT NULL,"
			"	DATA DATE NOT NULL,"
			"	PARTICIPANTE VARCHAR(64) NOT NULL,"
			"	SALDO INT NOT NULL,"
			"	ACUMULADO BIGINT NOT NULL,"
			"	PRIMARY KEY(IDENTIFICADOR_ID),"
			"	FOREIGN KEY(IDENTIFICADOR_ID)"
			"	REFERENCES derivatives_contratos(IDENTIFICADOR)"			    
			");")
		print("\nTabelas truncadas com sucesso!") 

	def close(self):
		self.cursor.close()
		self.conn.close()