from collections import defaultdict
import csv
import os
import re
import json

class CSV:
	def __init__(self):
		pass

	def write_data(self, all_data, path=os.path.join("..","csv","")):
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

	def write_accumulated(self, all_data, path=os.path.join("..","csv","accumulated","")):
		for contract, rows in all_data.items():
			fields = ["DATA", "PARTICIPANTE", "SALDO", "ACUMULADO"]
			accumulated = defaultdict(int)
			temp = []
			with open(path + contract + "_acumulado.csv", mode="w") as csv_file:
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