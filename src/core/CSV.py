import csv
import json
import os
import re

class CSV:
	def __init__(self, data, date, filter_, path = os.path.join("..","csv","")):
		self.fields = [
			"IDENTIFICADOR",
			"DATA",
			"DERIVATIVO",
			"PARTICIPANTE",
			"LONGCONTRACTS",
			"LONG%",
			"SHORTCONTRACTS",
			"SHORT%",
			"SALDO"]		
		self.data = data
		self.date = date
		self.filter = filter_
		self.path = path

		#print(json.dumps(self.data,indent=4))


	def write(self):
		for file in self.filter:
			with open(self.path + file + ".csv", mode='w') as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=";", quoting=csv.QUOTE_ALL)
				writer.writeheader()
				for k,v in self.data[file].items():
					participant = k
					longcontracts = re.sub(r",", ".", v[0])
					long = v[1]
					shortcontracts = re.sub(r",", ".", v[2])
					short = v[3]
					writer.writerow({
						'IDENTIFICADOR': re.sub(r"/", "", self.date["dData1"]) + "_" + file + "_" + participant,
						'DATA': self.date["dData1"] ,
						'DERIVATIVO': file,
						'PARTICIPANTE': participant,
						'LONGCONTRACTS': v[0],
						'LONG%': long,
						'SHORTCONTRACTS': v[2],
						'SHORT%': short,
						'SALDO': str(round(eval(longcontracts + "-" + shortcontracts), 2))
					})