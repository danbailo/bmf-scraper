from bs4 import BeautifulSoup
import requests
import csv
import re
import os
from collections import defaultdict
import json

class BMF:
	def __init__(self, url):
		self.url = url
		self.data = False

	def set_date(self, format_date):
		self.month = format_date[0]
		self.day = format_date[1]
		self.year = format_date[2]
		self.__date = {'dData1': self.month+"/"+self.day+"/"+self.year}		

	def request(self):
		response = requests.post(self.url, data=self.__date, verify=False)
		return response

	def get_filters(self, path=os.path.join("..", "inputs", "derivatives.txt")):
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

		derivatives = [re.sub(r"\s{2,}", "", derivative.text) for derivative in soup.findAll("caption")]
		tds = soup.findAll("td")

		self.data = defaultdict(lambda: defaultdict(list))
		if len(derivatives) == 0: 
			return False
		derivative = derivatives.pop(0)
		
		i = 0
		while i < len(tds):
			if len(derivatives) == 0: break
			if i % 5 == 0:
				participant = re.sub(r"\s{2,}", "", tds[i].text)
				i += 1
				continue
			self.data[derivative][participant].append(re.sub(r"\s{2,}", "", tds[i].text))
			if participant == "Total":
				self.data[derivative][participant].append(re.sub(r"\s{2,}", "", tds[i+1].text))
				self.data[derivative][participant].append(re.sub(r"\s{2,}", "", tds[i+2].text))
				self.data[derivative][participant].append(re.sub(r"\s{2,}", "", tds[i+3].text))
				derivative = derivatives.pop(0)
				i += 4
				continue
			i += 1

	def get_id(self, filters, path=os.path.join("..", "csv", "")):		
		self.write_header = False
		self.dates = set()
		self.last_date = ""
		for derivative in filters:
			try:
				with open(path + derivative + ".csv", mode='r') as csv_file:
					csv_reader = csv.DictReader(csv_file, delimiter=";")
					for row in csv_reader:
						self.dates.add(row["DATA"])
						self.last_date = row["DATA"]
			except FileNotFoundError:
				self.write_header = True
				pass

	def get_accumulated(self, filters, path=os.path.join("..", "csv", "ACCUMULATED", "")):
		last_accumulated = defaultdict(lambda: defaultdict(int))
		for derivative in filters:
			try:
				with open(path + derivative.upper() + " ACCUMULATED.csv", mode='r') as csv_file:
					csv_reader = csv.DictReader(csv_file, delimiter=";")
					for row in csv_reader:
						if row["DATA"] == self.last_date:
							last_accumulated[derivative.upper()][row["PARTICIPANTE"]] = int(row["ACUMULADO"])
			except FileNotFoundError:
				return False
		return last_accumulated

	def prepare_data(self, filters):
		if not self.data: return False
		prepared_data = defaultdict(lambda: defaultdict(list))
		for derivative in filters:
			for k,v in self.data[derivative].items():				
				participant = k
				date = self.day + "/" + self.month + "/" + self.year

				if date in self.dates: continue

				identifier = self.day + self.month + self.year + "_" + derivative + "_" + participant
				longcontracts = int(v[0].replace(",", ""))
				long = float(v[1])
				shortcontracts = int(v[2].replace(",", ""))
				short = float(v[3])				
				balance = longcontracts - shortcontracts

				prepared_data[derivative]['IDENTIFICADOR'].append(identifier)
				prepared_data[derivative]['DATA'].append(date)
				prepared_data[derivative]['DERIVATIVO'].append(derivative)
				prepared_data[derivative]['PARTICIPANTE'].append(participant)
				prepared_data[derivative]['LONGCONTRACTS'].append(longcontracts)
				prepared_data[derivative]['LONG_'].append(long)
				prepared_data[derivative]['SHORTCONTRACTS'].append(shortcontracts)
				prepared_data[derivative]['SHORT_'].append(short)
				prepared_data[derivative]['SALDO'].append(balance)

		return prepared_data