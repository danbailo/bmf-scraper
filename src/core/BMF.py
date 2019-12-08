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

		contracts = [re.sub(r"\s{2,}", "", contract.text) for contract in tables.findAll("caption")]
		j = 0
		rows = [re.sub(r"\s{2,}", "", contract.text) for contract in tables.findAll("td")]
		
		with open('bmf.csv', mode='w') as csv_file:
			writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=";")
			writer.writeheader()	

			for i in range(0,len(rows)):
				try:
					if i % 5 == 0:
						contract = contracts[j]
						participant = rows[i]
						longcontracts = rows[i+1]
						long = re.sub(r",", ".", rows[i+2])
						shortcontracts = rows[i+3]
						short = re.sub(r",", ".", rows[i+4])
						j += 1
					print(participant)
					print(longcontracts)
					print(long)
					print(shortcontracts)
					print(short)

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
					#break