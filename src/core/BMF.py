from bs4 import BeautifulSoup
import requests
import csv
import re

class BMF:
	def __init__(self, url, data):
		self.url = url
		self.data = data
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

	def request(self):
		response = requests.post(self.url, data=self.data, verify=False)
		return response

	def get_data(self):
		print("Requisitando dados...")
		while True:
			try:
				response = self.request()
				break
			except Exception:
				continue
		soap = BeautifulSoup(response.text, "html.parser")
		tables = soap.find("table")

		for contract in tables.findAll("caption"):
			print(re.sub(r"\s{2,}", "", contract.text))

		print()

		for tbody in tables.findAll("tbody"):
			print(([temp for temp in tbody.find("tr", recursive=False).text.split("\n") if temp != ""]))

		exit()

		j = 0
		rows = [re.sub(r"\s{2,}", "", contract.text) for contract in tables.findAll("td")]
		for row in rows:
			print(row, end=" ")
			j+=1
			if j%5==0: print()
		exit()
		with open('bmf.csv', mode='w') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=";")
			writer.writeheader()	

			for i in range(0, len(rows), 5):
				try:
					if i % 5 == 0:
						contract = contracts[j]
						j += 1
					participant = rows[i]
					longcontracts = rows[i+1]
					long = re.sub(r",", ".", rows[i+2])
					shortcontracts = rows[i+3]
					short = re.sub(r",", ".", rows[i+4])						
					writer.writerow({
						'IDENTIFICADOR': self.data["dData1"] + "_" + contract + "_" + participant,
						'DATA': self.data["dData1"] ,
						'DERIVATIVO': contract,
						'PARTICIPANTE': participant,
						'LONGCONTRACTS':longcontracts,
						'LONG%': long,
						'SHORTCONTRACTS': shortcontracts,
						'SHORT%': short,
						'SALDO': str(eval(long + "-" + short))
					})						

				except Exception as err:
					print("Entrei aq", err)
					break