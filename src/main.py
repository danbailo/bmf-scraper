from core import BMF, CSV, Database
from datetime import timedelta, date
import datetime
import json

#01/01/2010.

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

if __name__ == "__main__":

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

		bmf = BMF('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp', {'dData1': month+"/"+day+"/"+year})
		
		path = "../filters/contract.txt"
		filters = bmf.get_filters(path)
		bmf.get_data_from_web()

		prepared_data = bmf.get_prepared_data(filters)
		if not prepared_data: continue

		if not temp_dict: temp_dict = prepared_data.copy()

		for f in filters:
			for key in keys:				
				temp_dict[f][key] += prepared_data[f][key]

	csv = CSV(temp_dict)
	csv.write()

#	Traceback (most recent call last):
#  File "main.py", line 73, in <module>
#    database.insert_into_all_data(temp_dict)
#  File "/home/daniel/Workspace/bmf-scraper/src/core/Database.py", line 48, in insert_into_all_data
#    date_mysql = datetime.datetime(year, month, day)
#ValueError: month must be in 1..12

	
	database = Database(
		user="root",
		password="59228922ddd",
		database="BMF_values"
	)
	database.insert_into_all_data(temp_dict)
	database.close()