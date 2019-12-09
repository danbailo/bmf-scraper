from bs4 import BeautifulSoup
import requests
import csv
import re
import os
from collections import defaultdict
import json

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

	def get_filters(self, path):
		with open(path) as file:
			self.filters = [re.sub(r"\n", "", filter_) for filter_ in file.readlines()]

	def get_data(self):
		print("Requisitando dados...")
		while True:
			try:
				response = self.request()
				break
			except Exception:
				continue
		soup = BeautifulSoup(response.text, "html.parser")
		contracts = []
		for contract in soup.findAll("caption"):
			temp = re.sub(r"\s{2,}", "", contract.text)
			if temp in self.filters:
				contracts.append(temp)

		contracts = [re.sub(r"\s{2,}", "", contract.text) for contract in soup.findAll("caption")]

		tds = soup.findAll("td")

		data = defaultdict(lambda: defaultdict(list))
		contract = contracts.pop(0)
		
		i = 0
		while i < len(tds):
			if len(contracts) == 0: break
			if i % 5 == 0:
				participant = re.sub(r"\s{2,}", "", tds[i].text)
				i += 1
				continue
			data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i].text))
			if participant == "Total":
				data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+1].text))
				data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+2].text))
				data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+3].text))
				contract = contracts.pop(0)
				i += 4 #salta o i para a proxima tabela
				continue
			i += 1

		print(json.dumps(data,indent=4))

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