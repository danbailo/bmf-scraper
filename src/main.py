from core import BMF

if __name__ == "__main__":
	data = {
		'dData1': '12/05/2019'
	}

	bmf = BMF('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp', data)

	path = "../filters/contract.txt"

	bmf.get_filters(path)
	bmf.get_data()