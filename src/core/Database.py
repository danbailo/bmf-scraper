from collections import defaultdict
from tqdm import trange
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
		print('Inserindo dados na tabela "derivatives_contratos"')
		for derivative, rows in all_data.items():
			print("Derivativo:",derivative)
			temp = []
			for row in rows.values():
				temp.append(row)
			data = list(zip(*temp))
			for i in trange(len(data)):
				date = data[i][1].split("/")
				day = int(date[0])
				month = int(date[1])
				if month > 12:
					month = 12
				year = int(date[2])
				date_mysql = datetime.datetime(year, month, day)
				self.cursor.execute(
					"""INSERT IGNORE INTO derivatives_contratos (IDENTIFICADOR, DATA, DERIVATIVO, PARTICIPANTE, LONGCONTRACTS, LONG_, SHORTCONTRACTS, SHORT_, SALDO)
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(data[i][0], date_mysql, data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8]))
			self.conn.commit()
		print('Dados inseridos com sucesso na tabela "derivatives_contratos"!') 
		
	def insert_derivatives_acumulado(self, all_data):
		print('Inserindo dados na tabela "derivatives_acumulado"')
		for derivative, rows in all_data.items():
			print("Derivativo:",derivative)
			accumulated = defaultdict(int)
			temp = []
			for row in rows.values():
				temp.append(row)
			data = list(zip(*temp))
			for i in trange(len(data)):
				date = data[i][1].split("/")
				day = int(date[0])
				month = int(date[1])
				if month > 12:
					month = 12
				year = int(date[2])
				date_mysql = datetime.datetime(year, month, day)				
				accumulated[data[i][3]] += data[i][8]
				self.cursor.execute(
					"""INSERT IGNORE INTO derivatives_acumulado (IDENTIFICADOR_ID, DATA, PARTICIPANTE, SALDO, ACUMULADO)
					VALUES (%s, %s, %s, %s, %s)""",
					(data[i][0], date_mysql, data[i][3], data[i][8], accumulated[data[i][3]]))
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