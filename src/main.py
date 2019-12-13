from core import BMF, CSV, Database
from datetime import timedelta, date
from tqdm import trange
from sys import platform
import datetime
import os

AUTO_MYSQL = False

def daterange(initial_date, final_date):
	for n in trange(int ((final_date - initial_date).days)):
		yield initial_date + timedelta(n)

def get_option():
	print("\nCaso você tenha digitado a alguma informação errada, você tem a opção de digitar novamente.")
	option = input("Gostaria de digitar os dados novamente, [s]im ou [n]ão?\n> ")	
	return option

def get_path(accumulated=False):
	print("\nDigite o caminho de onde os arquivos serão gravados: ")
	print("Obs: Caso o caminho seja escrito incorretamente, os arquivos serão gravados no diretório padrão.")
	print("Pressione Enter para manter o diretório padrão.")
	if not accumulated:
		if platform == "linux" or platform == "linux2":
			print(r"Diretório padrão - ./bmf-scraper/csv")
		elif platform == "win32":			
			print(r"Diretório padrão - .\bmf-scraper\csv")
	else:		
		if platform == "linux" or platform == "linux2":
			print(r"Diretório padrão - ./bmf-scraper/csv/ACCUMULATED")
		elif platform == "win32":			
			print(r"Diretório padrão - .\bmf-scraper\csv\ACCUMULATED")		
	path = input("> ")
	if path:
		if platform == "linux":
			if path[-1] != "/":
				path = path + "/"			
		elif platform == "win32":
			if path[-1] != "\\":
				path = path + "\\"
	return path

if __name__ == "__main__":

	csv = CSV()
	db = Database()
	temp_dict = {}	
	
	while True:		
		print("\nEntre com a opção desejada:")
		print("1) Coletar dados;")
		print("2) Conectar no banco de dados;")
		print("3) Sair")
		try:
			option = int(input("> "))
		except Exception:
			continue

		if option == 1:
			path = get_path()
			path_accumulated = get_path(accumulated=True)

			if not os.path.isdir(path):
				path = os.path.join("..","csv","")
			if not os.path.isdir(path_accumulated):
				path_accumulated = os.path.join("..","csv","accumulated","")

			print("\nEntre com o intervalo de busca - [INICIAL, FINAL]\n")

			while True:
				print("Data INICIAL - dia/mês/ano")
				try:
					day_initial, month_initial, year_initial = input().split("/")
					if len(year_initial) != 4:
						print("\nPor favor, insira o ano no formato XXXX!")
						continue
					option = input("\nA data inicial informada foi {date}. Deseja alterar, [s]im ou [n]ão/Enter?\n> ".format(date=day_initial+"/"+month_initial+"/"+year_initial))
					#date_initial = datetime.datetime(int(year_initial), int(month_initial),int(day_initial))
					initial_date = date(int(year_initial), int(month_initial), int(day_initial))
					if option == "": option = "n"
					if option[0].lower() == 'n': break					
				except Exception:
					print("Por favor, entre com valores válidos!\n")
					continue
			while True:
				print("\nData FINAL - dia/mês/ano")
				today = date.today()
				try:
					day_final, month_final, year_final = input().split("/")
					final_date = date(int(year_final), int(month_final), int(day_final))
					final_date = final_date + datetime.timedelta(days=1)

					if len(year_final) != 4 and year_final != "":
						print("\nPor favor, insira o ano no formato XXXX!")
						continue					
					if(day_final) == "":
						day_final = today.day
					if(month_final) == "":
						month_final = today.month
					if(year_final) == "":
						year_final = today.year

				except ValueError:					
					day_final = today.day
					month_final = today.month
					year_final = today.year
					final_date = date(int(year_final), int(month_final), int(day_final))
				
				if final_date <= initial_date:
					print("\nA data final precisa ser maior do que a inicial!")
					continue													
				option = input("\nA data final informada foi {date}. Deseja alterar, [s]im ou [n]ão/Enter?\n> ".format(date=str(day_final)+"/"+str(month_final)+"/"+str(year_final)))
				if option == "": option = "n"
				if option[0].lower() == 'n': break									

			print()

			initial_date = date(int(year_initial), int(month_initial), int(day_initial))
			final_date = date(int(year_final), int(month_final), int(day_final))
			final_date = final_date + datetime.timedelta(days=1)
			temp_dict = {}
			keys = ['IDENTIFICADOR', 'DATA', 'DERIVATIVO', 'PARTICIPANTE', 'LONGCONTRACTS', 'LONG_', 'SHORTCONTRACTS', 'SHORT_', 'SALDO']

			print("Coletando dados de {initial} até {final}.".format(initial=initial_date, final=final_date))
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

				filters = bmf.get_filters()
				bmf.get_id(filters)
				last_accumulated = bmf.get_accumulated(filters)

				header = bmf.write_header
				bmf.get_data_from_web()

				prepared_data = bmf.prepare_data(filters)
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

			print("\nDados coletados com sucesso!")		

			#print(last_accumulated)

			writed1 = csv.write_data(temp_dict, write_header=header, path=path)
			writed2 = csv.write_accumulated(temp_dict, last_accumulated=last_accumulated ,write_header=header, path=path_accumulated)
			if not writed1 and not writed2:
				print("\nOs dados não foram gravados pois já estão no escritos no csv!")
			else:
				print("\nOs dados foram gravados com sucesso!")

			if AUTO_MYSQL:
				print("\nInserindo dados automaticamente no banco.")
				config = db.get_config()
				db.connect(config)
				db.create_tables()				
				db.insert_derivatives_contratos(temp_dict)
				print()
				db.insert_derivatives_acumulado(temp_dict)

		elif option == 2:
			while True:
				try:
					config = db.get_config()
					db.connect(config)
					db.create_tables()

					while True:
						print("\nEntre com a opção desejada:")
						print("1) Inserir dados no banco;")
						print("2) Auto Insert MySQL;")
						print("3) Truncar tabelas;")
						print("4) Voltar")
						try:
							option_bd = int(input("> "))
						except ValueError:
							continue

						if option_bd == 1:
							if not temp_dict:
								print("\nNão existem dados para ser inseridos no banco!")
								print("Por favor, execute a opção de coletar os dados e tente novamente!")
							else:
								db.insert_derivatives_contratos(temp_dict)
								print()
								db.insert_derivatives_acumulado(temp_dict)
						
						elif option_bd == 2:
							AUTO_MYSQL = True
							print("Inserir dados automaticamente ligado!")
							
						elif option_bd == 3:
							db.truncate_tables()

						elif option_bd == 4: 
							db.close()					
							break
					break
				except Exception as err:
					print(err)
					print("\nERRO ao se conectar ao banco de dados, verifique se os dados no arquivo de configuração estão corretos e se o serviço do banco de dados está ligado e tente novamente!")
					input('\nCaso você tenha alterado o arquivo, pressione "Enter" para continuar.')
					print("\nSe o erro persistir, pressione CTRL+C para finalizar a execução do programa!")
					
		elif option == 3: exit(0)
		else: continue
