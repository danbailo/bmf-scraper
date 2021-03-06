from collections import defaultdict
import csv
import os
import json

class CSV:
	def __init__(self):
		pass

	def write_data(self, all_data, write_header, path=os.path.join("..","csv","")):
		if len(all_data) == 0: 
			return False
		for derivative, rows in all_data.items():
			self.fields = list(rows.keys())
			temp = []
			while True:
				try:
					with open(path + derivative.upper() + ".csv", mode="a", newline='\n', encoding='utf-8') as csv_file:
						writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=";")
						if write_header:
							writer.writeheader()
						for row in rows.values():
							temp.append(row)
						data = list(zip(*temp))
						for value in data:
							writer.writerow({
								self.fields[0]: value[0],
								self.fields[1]: value[1],
								self.fields[2]: value[2],
								self.fields[3]: value[3],
								self.fields[4]: value[4],
								self.fields[5]: value[5],
								self.fields[6]: value[6],
								self.fields[7]: value[7],
								self.fields[8]: value[8]
							})
					break	
				except PermissionError:
					print("\nERRO ao gravar arquivo .csv!")
					print("Por favor, feche todos os arquivos .csv que estão abertos!")
					input('\nCaso você tenha fechado o arquivo, pressione "Enter" para continuar.')
					continue
		return True

	def write_accumulated(self, all_data, write_header, last_accumulated, path=os.path.join("..","csv","ACCUMULATED","")):
		if len(all_data) == 0: 
			return False			
		fields = ["DATA", "PARTICIPANTE", "SALDO", "ACUMULADO"]
		for derivative, rows in all_data.items():
			accumulated = defaultdict(int)
			temp = []
			while True:
				try:
					with open(path + derivative.upper() + " ACCUMULATED.csv", mode="a", newline='\n', encoding='utf-8') as csv_file:
						writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=";")
						if write_header:
							writer.writeheader()
						for row in rows.values():
							temp.append(row)
						data = list(zip(*temp))
						for value in data:
							accumulated[value[3]] += value[8]
							try:							
								last = last_accumulated[derivative.upper()][value[3]] + value[8]
								last_accumulated[derivative.upper()][value[3]] = last
								writer.writerow({
									fields[0]: value[1],
									fields[1]: value[3],
									fields[2]: value[8],
									fields[3]: last
								})

							except TypeError:					
								writer.writerow({
									fields[0]: value[1],
									fields[1]: value[3],
									fields[2]: value[8],
									fields[3]: accumulated[value[3]]
								})		
					break
				except PermissionError:
					print("\nERRO ao gravar arquivo .csv!")
					print("Por favor, feche todos os arquivos .csv que estão abertos!")
					input('\nCaso você tenha fechado o arquivo, pressione "Enter" para continuar.')
					continue
		return True