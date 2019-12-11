from collections import defaultdict
import csv
import os
import re
import json

class CSV:
	def __init__(self):
		pass

	def write(self, all_data, path=os.path.join("..","csv","")):
		for contract, rows in all_data.items():
			fields = list(rows.keys())
			temp = []
			with open(path + contract + ".csv", mode="w") as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=";")
				writer.writeheader()
				for row in rows.values():
					temp.append(row)
				data = list(zip(*temp))
				for value in data:
					writer.writerow({
						fields[0]: value[0],
						fields[1]: value[1],
						fields[2]: value[2],
						fields[3]: value[3],
						fields[4]: value[4],
						fields[5]: value[5],
						fields[6]: value[6],
						fields[7]: value[7],
						fields[8]: value[8]
					})

	def write2(self, all_data, path=os.path.join("..","csv","accumulated","")):
		for contract, rows in all_data.items():
			fields = ["DATA", "PARTICIPANTE", "SALDO", "ACUMULADO"]
			accumulated = defaultdict(int)
			temp = []
			with open(path + contract + "_ACUMULADO.csv", mode="w") as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=";")
				writer.writeheader()
				for row in rows.values():
					temp.append(row)
				data = list(zip(*temp))
				for value in data:
					accumulated[value[3]] += value[8]
					writer.writerow({
						fields[0]: value[1],
						fields[1]: value[3],
						fields[2]: value[8],
						fields[3]: accumulated[value[3]]
					})
	def write_accumulated(self, all_data, path=os.path.join("..","csv","accumulated","")):
		accumulated = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		keys = ["DATA", "PARTICIPANTE", "SALDO"]
		for contract in all_data:
			temp = []
			for key in keys:
				temp.append(all_data[contract][key])
			data = list(zip(*temp))

			for row in data:
				accumulated[contract][row[0]][row[1]] += row[2]


		print(json.dumps(accumulated, indent=4))

		exit()
		with open(path + contract + "_ACUMULADO.csv", mode="w") as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=keys, delimiter=";")
			writer.writeheader()
			for k,v in accumulated.items():
				print(k,v)
#			for value in data:
#				writer.writerow({
#					fields[0]: value[0],
#					fields[1]: value[1],
#					fields[2]: value[2],
#					fields[3]: value[3],
#					fields[4]: value[4],
#					fields[5]: value[5],
#					fields[6]: value[6],
#					fields[7]: value[7],
#					fields[8]: value[8]
#					})		

	def get_accumulated(self, path=os.path.join("..","csv","")):
		all_files = [temp_file for temp_file in os.listdir(path) if temp_file[-4:] == ".csv"]		
		accumulated = defaultdict(lambda: defaultdict(list))
		accumulated = {}
		accumulated['IDENTIFICADOR'] = {}
		accumulated['DATA'] = {}
		accumulated['DERIVATIVO'] = {}
		accumulated['PARTICIPANTE'] = {}
		accumulated['SALDO'] = {}
		accumulated['ACUMULADO'] = {}
		for file in all_files:
			with open(path + file, mode='r') as csv_file:
				csv_reader = csv.DictReader(csv_file, delimiter=";", quoting=csv.QUOTE_ALL)
				for row in csv_reader:
					if row['PARTICIPANTE'] not in accumulated["ACUMULADO"].keys():
						accumulated["ACUMULADO"][row['PARTICIPANTE']] = 0
					accumulated["ACUMULADO"][row['PARTICIPANTE']] += float(row["SALDO"])
					accumulated['IDENTIFICADOR'] = row['IDENTIFICADOR']
					accumulated['DATA'] = row['DATA']
					accumulated['DERIVATIVO'] = row['DERIVATIVO']
					accumulated['PARTICIPANTE'] = row['PARTICIPANTE']
					accumulated['SALDO'] = row['SALDO']
					accumulated["ACUMULADO"].values()
		print(json.dumps(accumulated, indent=4))
		print()