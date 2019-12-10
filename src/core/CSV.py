import csv
import os
import re

class CSV:
	def __init__(self, data, path=os.path.join("..","csv","")):
		self.data = data
		self.path = path

	def write(self):
		for contract, rows in self.data.items():
			fields = list(rows.keys())
			temp = []
			with open(self.path + contract + ".csv", mode="w") as csv_file:
				writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=";", quoting=csv.QUOTE_ALL)
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