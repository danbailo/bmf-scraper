from core import BMF, CSV, Database
from datetime import timedelta, date
from tqdm import trange
import datetime
import os

def daterange(initial_date, final_date):
	for n in trange(int ((final_date - initial_date).days)):
		yield initial_date + timedelta(n)

def get_option():
	print("\nCaso você tenha digitado a data errada, você tem a opção de digitar novamente.")
	option = input("Gostaria de digitar a data novamente, [s]im ou [n]ão?\n> ")	
	return option

if __name__ == "__main__":
	while True:
		print("\nEntre com a opção desejada:")
		print("1) Coletar dados;")
		print("2) Conectar no banco de dados;")
		print("3) Sair")
		option = int(input("> "))

		csv = CSV()

		if option == 1:
			print("Digite o caminho de onde os arquivos serão gravados: ")
			print("obs: caso o caminho seja escrito incorretamente, os arquivos serão gravados no diretório padrão.")
			print("Diretório padrão - ./bmf-scraper/csv/")
			path = input("> ")

			print("Digite o caminho de onde os arquivos ACUMULADOS serão gravados: ")
			print("obs: caso o caminho seja escrito incorretamente, os arquivos serão gravados no diretório padrão.")
			print("Diretório padrão - ./bmf-scraper/csv/accumulated/")
			path_accumulated = input("> ")

			if not os.path.isdir(path):
				path = os.path.join("..","csv","")
			if not os.path.isdir(path):
				path_accumulated = os.path.join("..","csv","accumulated","")				

			print("Entre com o intervalo de busca - [INICIAL, FINAL)\n")

			print("Data INICIAL - dia/mes/ano")
			while True:
				day_initial = int(input("Dia: "))
				month_initial = int(input("Mês: "))
				year_initial = int(input("Ano: "))

				option = get_option()
				if option[0].lower() == 'n': break

			print("\nData FINAL - dia/mes/ano")
			while True:
				day_final = int(input("Dia: "))
				month_final = int(input("Mês: "))
				year_final = int(input("Ano: "))
				
				option = get_option()
				if option[0].lower() == 'n': break

			print()

			initial_date = date(year_initial, month_initial, day_initial)
			final_date = date(year_final, month_final, day_final)	
			temp_dict = {}
			keys = ['IDENTIFICADOR', 'DATA', 'DERIVATIVO', 'PARTICIPANTE', 'LONGCONTRACTS', 'LONG_', 'SHORTCONTRACTS', 'SHORT_', 'SALDO']

			print("Coletando dados...")
			for single_date in daterange(initial_date, final_date):				
				day = str(single_date.day)
				month = str(single_date.month)
				year = str(single_date.year)
				
				if len(day) == 1:
					day = "0" + day
				if len(month) == 1:
					month = "0" + month			

				format_date = (month, day, year)

				bmf = BMF('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp', format_date)
				
				path = "../filters/contract.txt"
				filters = bmf.get_filters(path)
				bmf.get_data_from_web()

				prepared_data = bmf.get_prepared_data(filters)
				if not prepared_data: 
					continue

				state = 0
				if not temp_dict: 
					temp_dict = prepared_data.copy()
					state = 1

				for f in filters:
					for key in keys:
						if state == 1: continue		
						temp_dict[f][key] += prepared_data[f][key]

			print("Dados coletados com sucesso!")		
			csv.write_data(temp_dict, path=path)
			csv.write_accumulated(temp_dict, path=path_accumulated)
			print("Os dados foram gravados no diretório: {path}.".format(path=path))

		elif option == 2:
			user = input("Digite o usuário do banco de dados: ")
			password = input("Digite a senha do usuário do banco de dados: ")
			db_name = input("Digite o nome do banco de dados: ")
			host = input("Digite o IP de onde está localizado o banco de dados(caso seja IP local, não digite nada, apenas dê um ENTER): ")
			port = input("Digite a porta da conexão de onde está localizado o banco de dados(caso seja a porta padrão, não digite nada, apenas dê um ENTER): ")

			database = Database(
				user=user,
				password=password,
				database=db_name,
				host=host,
				port=port
			)

			print("\t\nEntre com a opção desejada:")
			print("\t1) Inserir dados no banco dados;")
			print("\t2) Truncar tabelas;")
			print("\t3) Sair")
			option_bd = int(input("\t> "))

			if option_bd == 1:
				if not temp_dict:
					print("Antes de inserir os dados no banco, esses devem ser coletados!")
					print("Por favor, execute a opção de coletar os dados e tente novamente!")
				else:	
					database.insert_dados(temp_dict)
					database.insert_acumulado(temp_dict)
			elif option_bd == 1:
				#database.truncate_tables(temp_dict)
				pass

			database.close()
		elif option == 3: exit(0)
		else: continue
