from core import BMF, CSV, Database
from datetime import timedelta, date
import datetime
import json

#01/01/2010.

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)
if __name__ == "__main__":
	while True:
		print("\nEntre com a opcao desejada")
		print("1) Coletar dados")
		print("2) Gerar planilha dos valores acumulados")
		print("3) Sair")
		option = int(input("> "))

		csv = CSV()

		if option == 1:
			print("Entre com o intervalo de busca - [INICIAL, FINAL)\n")
			print("Data INICIAL - dia/mes/ano")

			while True:
				day_initial = int(input("Dia: "))
				month_initial = int(input("Mes: "))
				year_initial = int(input("Ano: "))
				option = input("Gostaria de digitar a data novamente, sim ou nao?\n> ")
				if option[0].lower() == 'n': break

			print("\nData FINAL - dia/mes/ano")
			while True:
				day_final = int(input("Dia: "))
				month_final = int(input("Mes: "))
				year_final = int(input("Ano: "))
				option = input("Gostaria de digitar a data novamente, sim ou nao?\n> ")
				if option[0].lower() == 'n': break
			print()	
			start_date = date(year_initial, month_initial, day_initial)
			end_date = date(year_final, month_final, day_final)

			
			temp_dict = {}
			keys = ['IDENTIFICADOR', 'DATA', 'DERIVATIVO', 'PARTICIPANTE', 'LONGCONTRACTS', 'LONG_', 'SHORTCONTRACTS', 'SHORT_', 'SALDO']

			for single_date in daterange(start_date, end_date):				
				day = str(single_date.day)
				month = str(single_date.month)
				year = str(single_date.year)
				
				if len(day) == 1:
					day = "0" + day
				if len(month) == 1:
					month = "0" + month			

				print("Requisitando dados do data:",day+"/"+month+"/"+year)

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

				print(json.dumps(prepared_data, indent=4))
				
				for f in filters:
					for key in keys:
						if state == 1: continue		
						temp_dict[f][key] += prepared_data[f][key]

				print(json.dumps(temp_dict, indent=4))

#			print(json.dumps(temp_dict, indent=4))
			#csv.write(temp_dict)
			exit()
			csv.write2(temp_dict)
			#database = Database(
			#	user="root",
			#	password="59228922ddd",
			#	database="BMF_values"
			#)
			#database.insert_data(temp_dict)
			#database.close()
		elif option == 2:
			csv.get_accumulated()
		elif option == 3: exit(0)
		else: continue
