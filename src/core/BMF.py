from bs4 import BeautifulSoup
import requests
import csv
import re
import os
from collections import defaultdict
import json

class BMF:
	def __init__(self, url, format_date):
		self.url = url
		self.month = format_date[0]
		self.day = format_date[1]
		self.year = format_date[2]
		self.__date = {'dData1': self.month+"/"+self.day+"/"+self.year}
		self.data = False

	def request(self):
		response = requests.post(self.url, data=self.__date, verify=False)
		return response

	def get_filters(self, path):
		with open(path) as file:
			return [re.sub(r"\n", "", filter_) for filter_ in file.readlines()]

	def get_data_from_web(self):
		while True:
			try:
				response = self.request()
				break
			except Exception:
				continue
		soup = BeautifulSoup(response.text, "html.parser")

		if soup.find("div", attrs={"class": "alert-box secondary"}):
			return False

		contracts = [re.sub(r"\s{2,}", "", contract.text) for contract in soup.findAll("caption")]
		tds = soup.findAll("td")

		self.data = defaultdict(lambda: defaultdict(list))
		if len(contracts) == 0: 
			return False
		contract = contracts.pop(0)
		
		i = 0
		while i < len(tds):
			if len(contracts) == 0: break
			if i % 5 == 0:
				participant = re.sub(r"\s{2,}", "", tds[i].text)
				i += 1
				continue
			self.data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i].text))
			if participant == "Total":
				self.data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+1].text))
				self.data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+2].text))
				self.data[contract][participant].append(re.sub(r"\s{2,}", "", tds[i+3].text))
				contract = contracts.pop(0)
				i += 4
				continue
			i += 1

	def get_prepared_data(self, filters):
		if not self.data: return False
		prepared_data = defaultdict(lambda: defaultdict(list))
		for contract in filters:
			for k,v in self.data[contract].items():				
				participant = k
				identifier = self.day + self.month + self.year + "_" + contract + "_" + participant
				date = self.day + "/" + self.month + "/" + self.year
				longcontracts = int(v[0].replace(",", ""))
				long = float(v[1])
				shortcontracts = int(v[2].replace(",", ""))
				short = float(v[3])				
				balance = longcontracts - shortcontracts

				prepared_data[contract]['IDENTIFICADOR'].append(identifier)
				prepared_data[contract]['DATA'].append(date)
				prepared_data[contract]['DERIVATIVO'].append(contract)
				prepared_data[contract]['PARTICIPANTE'].append(participant)
				prepared_data[contract]['LONGCONTRACTS'].append(longcontracts)
				prepared_data[contract]['LONG_'].append(long)
				prepared_data[contract]['SHORTCONTRACTS'].append(shortcontracts)
				prepared_data[contract]['SHORT_'].append(short)
				prepared_data[contract]['SALDO'].append(balance)
		return prepared_data