import xlrd

datafile = 'beatles-1.xls'

def parse_file(datafile):
	workbook = xlrd.open_workbook(datafile)
	sheet = workbook.sheet_by_index(0)

	#data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

	data = []
	for irow in range(sheet.nrows):
		r = []
		for icol in range(sheet.ncols):
			r.append(sheet.cell_value(irow, icol))
		data.append(r)
	print data[0][4]

parse_file(datafile)