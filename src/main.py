from core import BMF, CSV

if __name__ == "__main__":
	date = {
		'dData1': '12/05/2019'
	}

	bmf = BMF('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp', date)

	path = "../filters/contract.txt"

	bmf.get_filters(path)
	bmf.get_data()

	csv = CSV(bmf.data, date, bmf.filters)
	csv.write()