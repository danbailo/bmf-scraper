from bs4 import BeautifulSoup
import requests
import csv
import re
import os
from collections import defaultdict
import json

class BMF:
	def __init__(self, url, date):
		self.url = url
		self.date = date

	def request(self):
		response = requests.post(self.url, data=self.date, verify=False)
		return response

	def get_filters(self, path):
		with open(path) as file:
			return [re.sub(r"\n", "", filter_) for filter_ in file.readlines()]

	def get_data_from_web(self):
		print("Requisitando dados...")
		while True:
			try:
				response = self.request()
				break
			except Exception:
				continue
		soup = BeautifulSoup(response.text, "html.parser")
		contracts = [re.sub(r"\s{2,}", "", contract.text) for contract in soup.findAll("caption")]
		tds = soup.findAll("td")

		self.data = defaultdict(lambda: defaultdict(list))
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
	
	def get_filtered_data(self, filters):
		filtered_data = {}
		for contract in filters:
			if contract in self.data:
				filtered_data[contract] = self.data[contract].copy()
		return filtered_data