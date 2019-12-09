from core import BMF, CSV, Database
import datetime
import json

#01/01/2010.

if __name__ == "__main__":

	print("Entre com o intervalo de busca - [INICIAL, FINAL]")
	print("Data inicial - dia/mes/ano")
	day_initial = input("Dia: ")
	month_initial = input("Mes: ")
	year_initial = input("Ano: ")

	print("\nData final - dia/mes/ano")
	day_final = input("Dia: ")
	month_final = input("Mes: ")
	year_final = input("Ano: ")	

	day = "12"
	month = "05"
	year = "2019"

	date = day+"/"+month+"/"+year

	date = {
		'dData1': date,
	}

	bmf = BMF('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp', date)

	path = "../filters/contract.txt"

	filters = bmf.get_filters(path)
	bmf.get_data_from_web()

	prepared_data = bmf.get_prepared_data(filters)

	csv = CSV(prepared_data)
	csv.write()

	database = Database(
		user="root",
		password="59228922ddd",
		database="BMF_values"
	)

	database.insert_into_all_data(prepared_data)