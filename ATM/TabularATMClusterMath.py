#!/usr/bin/python
#---------------------------------------
# TabularATMClusterMath.py
# (c) Jansen A. Simanullang, 01.08.2016
# 18.08.2016
#---------------------------------------
# usage: python TabularATMClusterMath.py
#---------------------------------------
from BeautifulSoup import BeautifulSoup
import os, requests, time, urlparse, sys
import urllib2, pdfkit, xlwt, xlutils
from operator import itemgetter
from xlwt import *
#---------------------------------------
# CONFIGURABLE PARAMETER
#---------------------------------------
RegionName = 'JAKARTA III'
#---------------------------------------
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + os.sep

def welcomeScreen():

	if os.name == "posix":
		os.system("clear")
	else:
		os.system("cls")

	print "TABULAR ATM PROBLEM, UTILITY & AVAILABILITY \n\n\n"



def readClusterNumber(branchCode):

	fName = scriptDirectory + "conf/clusterBranches.csv"

	arrPICs = [""]
	PICNumber = 0

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")
			
		if col[1].strip() == branchCode:

			PICNumber=col[0]
				
	f.close()

	return PICNumber


def readClusterName(PICNumber):

	fName = scriptDirectory + "conf/clusterNames.csv"

	arrPICs = [""]
	PICName = 0

	f = open(fName)

	for baris in f.readlines():

		col = baris.strip().split(",")

		if col[0] == PICNumber:		

			PICName = col[1]
		
				
	f.close()

	return PICName


def fetchHTML(alamatURL):

	#print "fetching HTML from URL...\n", alamatURL
	strHTML = urllib2.urlopen(urllib2.Request(alamatURL, headers={ 'User-Agent': 'Mozilla/5.0' })).read()
	strHTML = strHTML.decode("windows-1252")

	strHTML = strHTML.encode('ascii', 'ignore')
	mysoup = BeautifulSoup(strHTML)
	
	#print ">> URL fetched."

	return strHTML



def getStyleList(strHTML):

	#print "\ngetting Style List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrStyle = mysoup.findAll('link', rel = "stylesheet" )

	strStyle = ""

	for i in range (0, len(arrStyle)):

		strStyle = strStyle + str(arrStyle[i])
	
	return strStyle



def getTableList(strHTML):

	#print "\ngetting Table List...\n"

	mysoup = BeautifulSoup(strHTML)

	arrTable = mysoup.findAll('table')

	#print "there are:", len(arrTable), "tables."
	
	return arrTable



def getLargestTable(arrTable):

	largest_table = None

	max_rows = 0

	for table in arrTable:

		# cek satu per satu jumlah baris yang ada pada masing-masing tabel dalam array kumpulan tabel
		# simpan dalam variabel bernama numRows

		numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
		
		# jika jumlah baris pada suatu tabel lebih besar daripada '0' maka jadikan sebagai max_rows sementara
		# proses ini diulangi terus menerus maka max_rows akan berisi jumlah baris terbanyak

		if numRows > max_rows:
			
		        largest_table = table
			max_rows = numRows

	# ini hanya mengembalikan penyebutan 'tabel terbesar' hanya sebagai 'tabel'

	table = largest_table

	#if table:
	#	print ">> the largest from table list is chosen."

	return table



def getNumCols(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	soup = BeautifulSoup(str(table))

	numCols = len(soup.findAll('tbody')[0].findAll('tr')[0].findAll('td'))

	#print "number of columns is", numCols

	return numCols



def getNumRows(table):

	# bagaimana cara menentukan berapa jumlah kolomnya?

	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))
	
	return numRows



def getNumRowsHead(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai header?

	soup = BeautifulSoup(str(table))
	head = soup.findAll('thead')

	numRowsHead = 0

	for i in range (0, len(head)):

		numRowsHead += len(head[i].findAll('tr'))

	#print "there is", len(head), "header with", numRowsHead, "rows"
		
	return numRowsHead



def getNumRowsFoot(table):

	# bagaimana cara menentukan berapa jumlah baris yang terpakai sebagai footer?

	soup = BeautifulSoup(str(table))
	foot = soup.findAll('tfoot')

	numRowsFoot = 0

	for i in range (0, len(foot)):

		numRowsFoot += len(foot[i].findAll('tr'))

	#print "there is", len(foot), "footer with", numRowsFoot, "rows"
		
	return numRowsFoot



def getTableDimension(table):
	
	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)
	numCols = getNumCols(table)
	
	return numRows, numRowsHead, numCols



def getSpecificRow(table, rowIndex):

	#print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def getRowIndex(table, strSearchKey):

	# fungsi ini untuk mendapatkan nomor indeks baris yang mengandung satu kata kunci

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	
	numRows = len(table.findAll(lambda tag: tag.name == 'tr' and tag.findParent('table') == table))

	rowIndex = 0

	for i in range (0, numRows):

		trs = BeautifulSoup(str(rows[i]))
		tdcells = trs.findAll("td")
			
		for j in range (0, len(tdcells)):

			if tdcells[j].getText().upper() == strSearchKey.upper():
				
				rowIndex = i

				#print "we got the index = ", rowIndex, "from ", numRows, "for search key ='"+strSearchKey+"'"
	return rowIndex



def getSpecificRows(table, rowIndex):

	print "Let's take a look at the specific rows of index", rowIndex

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	strHTMLTableRows = ""

	for i in range (rowIndex, rowIndex+1):

		strHTMLTableRows = str(rows[i])
	
	return strHTMLTableRows



def getTableContents(table):

	numRows = getNumRows(table)
	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')
	#print len(rows)
	strHTMLTableContents = ""
	TProblem = []

	# RANKING PROBLEM ATM
	#print "\n# RANKING PROBLEM ATM\n"

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")
		#print len(tdcells)
		kodeCabang = tdcells[1].getText()

		PICName = readClusterName(readClusterNumber(kodeCabang))

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textNOPG = tdcells[4].getText()
		if (textNOPG) != '':
			NOPG = int(tdcells[4].getText()) 
		else:			
			NOPG = 0
			#print "NOPG NIHIL"
		#---------------------------------------
		textNOPNG = tdcells[5].getText()
		if (textNOPG) != '':
			NOPNG = int(tdcells[5].getText()) 
		else:
			NOPNG = 0
			#print "NOPNG NIHIL"
		#---------------------------------------
		NOP = NOPG + NOPNG
		#---------------------------------------
		textRSKG = tdcells[6].getText()
		if (textRSKG) != '':
			RSKG = int(tdcells[6].getText()) 
		else:			
			RSKG = 0
			#print "RSKG NIHIL"
		#---------------------------------------
		textRSKNG = tdcells[7].getText()
		if (textRSKNG) != '':
			RSKNG = int(tdcells[7].getText()) 
		else:			
			RSKNG = 0
			#print "RSKNG NIHIL"
		#---------------------------------------
		RSK = RSKG + RSKNG
		#---------------------------------------
		textPROBOPS = tdcells[8].getText()
		if (textPROBOPS) != '':
			PROBOPS = int(tdcells[8].getText()) 
		else:			
			PROBOPS = 0
			#print "PROBOPS NIHIL"
		#---------------------------------------
		textOOS= tdcells[12].getText()
		if (textOOS) != '':
			OOS = int(tdcells[12].getText()) 
		else:			
			OOS = 0
			#print "OOS NIHIL"
		#---------------------------------------
		textOFF = tdcells[13].getText()
		if (textOFF) != '':
			OFF = int(tdcells[13].getText()) 
		else:			
			OFF = 0
			#print "OFF NIHIL"
		#---------------------------------------

		PROB = NOP + RSK + PROBOPS + OOS + OFF

		#print kodeCabang, namaCabang, NOP, RSK, PROBOPS, OOS, OFF, PROB

		TProblem.append((kodeCabang, namaCabang, NOP, RSK, PROBOPS, OOS, OFF, PROB, PICName))

		TProblem = sorted(TProblem, key=itemgetter(8, 7, 1), reverse = False)


	# RANKING UTILITY ATM
	#print "\n# RANKING UTILITY ATM\n"
	TUtility = []

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		kodeCabang = tdcells[1].getText()

		PICName = readClusterName(readClusterNumber(kodeCabang))

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textUP = tdcells[9].getText()
		if (textUP) != '':
			UP = int(tdcells[9].getText()) 
		else:			
			UP = 0
		#---------------------------------------
		textTunai = tdcells[10].getText()
		if (textTunai) != '':
			TUNAI = int(tdcells[10].getText()) 
		else:			
			TUNAI = 0
		#---------------------------------------
		textNonTunai = tdcells[11].getText()
		if (textNonTunai) != '':
			NONTUNAI = int(tdcells[11].getText()) 
		else:			
			NONTUNAI = 0
		#---------------------------------------
		PERCENT = float(TUNAI/float(UP)*100)
		#print "{0:.0f}".format(PERCENT), NONTUNAI, ATM 

		TUtility.append((kodeCabang, namaCabang, UP, TUNAI, NONTUNAI, float("{0:.2}".format(PERCENT)),PICName))
		TUtility = sorted(TUtility, key=itemgetter(6, 5, 1), reverse = False)


	# RANKING AVAILABILITY ATM
	#print "\n# RANKING AVAILABILITY ATM\n"
	TAvailability = []

	for i in range (2, numRows-1):

		trs = BeautifulSoup(str(rows[i]))
	
		tdcells = trs.findAll("td")

		kodeCabang = tdcells[1].getText()

		PICName = readClusterName(readClusterNumber(kodeCabang))

		dText = tdcells[2].getText()

		namaCabang = cleanupNamaUker(dText.upper())
		#---------------------------------------
		textATM = tdcells[3].getText()
		if (textATM) != '':
			ATM = int(tdcells[3].getText()) 
		else:			
			ATM = 0
		#---------------------------------------
		textAvail = tdcells[24].getText()
		if (textAvail) != '':
			AVAIL = float(tdcells[24].getText()) 
		else:			
			AVAIL = 0
		#---------------------------------------


		#print kodeCabang, namaCabang, AVAIL

		TAvailability.append((kodeCabang, namaCabang, ATM, AVAIL, PICName))
		TAvailability = sorted(TAvailability, key=itemgetter(4, 3, 2, 1), reverse = False)

		#print TAvailability

	return TProblem, TUtility, TAvailability



def getColIndex(table, strSearchKey1, strSearchKey2):

	# fungsi ini untuk mendapatkan nomor indeks kolom yang mengandung satu kata kunci

	numCols = getNumCols(table)
	numRowsHead = getNumRowsHead(table)

	soup = BeautifulSoup(str(table))
	rows = soup.findAll('tr')

	colIndex1 = -1

	for i in range (0, 1):

		trs = BeautifulSoup(str(rows[i]))
		thcells = trs.findAll("th")
			
		for i in range (0, len(thcells)):

			if ("colspan" in str(thcells[i]) and thcells[i].findAll('a')[0].getText().upper() == strSearchKey1.upper()):

				intColSpan = int(thcells[i]['colspan'])

				print i, intColSpan

				colIndex1 = (i-1) * intColSpan + 1

				
			elif ("rowspan" in str(thcells[i]) and thcells[i].getText().upper() == strSearchKey1.upper()):

				intColSpan = 1

				colIndex1 = (i-1) * intColSpan + 1 

				print i, "rowspan"
	#colIndex2 = 0
	for i in range (1, 2):
					
		soup = BeautifulSoup(str(rows[i]))
		thcells2 = soup.findAll("th")

		# the length must be limited to the colindex of the above search
		maxIndex = len(thcells2)
		maxIndex = colIndex1 - 1

		for i in range (0, maxIndex):
		
			if thcells2[i].getText().upper() == strSearchKey2.upper():
				colIndex2 = i+3 # the factor +3 is due to the two columns with the rowspan before
				


				
	print "we got the col index = (", colIndex1, ") from ", numCols-1, "index for search key ='"+strSearchKey1+"'"
	print "we got the col index = (", colIndex2, ") from ", numCols-1, "index for search key ='"+strSearchKey2+"'"
	return colIndex2



def cleanupNamaUker(namaUker):


	namaUker = namaUker.replace("JAKARTA ","")
	namaUker = namaUker.replace("Jakarta ","")
	namaUker = namaUker.replace("JKT ","")
	namaUker = namaUker.replace("KANCA ","")
	namaUker = namaUker.replace("KC ","")

	return namaUker.strip()




def getRowInterest(table, keyword):

	strHTMLTableRows = getSpecificRow(table, getRowIndex(table, keyword))
	
	mysoup = BeautifulSoup(strHTMLTableRows)

	arrTDs = mysoup.findAll('td')

	return arrTDs[1].getText()


def colorAvail(percentAvail):

	strColor = str(percentAvail)

	if percentAvail >= 0.00:
		strColor = "merah"
	if percentAvail >= 87.00:
		strColor = "kuning"
	if percentAvail >= 93.00:
		strColor = "hijau_muda"
	if percentAvail >= 97.00:
		strColor = "hijau_tua"


	return strColor


def colorProblem(PRO):

	strColor = str(PRO)

	if PRO == 0.00:
		strColor = "hijau_tua"
	if PRO >= 1:
		strColor = "hijau_muda"
	if PRO == 3:
		strColor = "kuning"
	if PRO > 3:
		strColor = "merah"


	return strColor

def colorUtility(percentTunai):

	strColor = str(percentTunai)

	if percentTunai >= 0.00:
		strColor = "merah"
	if percentTunai >= 80.00:
		strColor = "kuning"
	if percentTunai >= 90.00:
		strColor = "hijau_muda"
	if percentTunai >= 100.00:
		strColor = "hijau_tua"


	return strColor

def prepareDirectory(strOutputDir):
	# siapkan struktur direktori untuk penyimpanan data
	# struktur direktori adalah ['OUTPUT', 'EDC', '2015', '04-APR', 'DAY-28'] makes './OUTPUT/EDC/2015/04-APR/DAY-28'

	arrDirectoryStructure = [strOutputDir, 'ATM', time.strftime("%Y"), time.strftime("%m-%b").upper() , "DAY-"+time.strftime("%d")]

	fullPath = scriptDirectory

	for i in range (0, len(arrDirectoryStructure)):
	
		fullPath = fullPath + arrDirectoryStructure[i] + "/"

		if not os.path.exists(fullPath):

			print "creating directories:", arrDirectoryStructure[i]
		    	os.mkdir(fullPath)
			os.chdir(fullPath)

	print fullPath

	return fullPath


def putDataXL(offRow, offCol, TProblem, TUtility, TAvailability):

	book = xlwt.Workbook()

	# add new colour to palette and set RGB colour value
	xlwt.add_palette_colour("sky_blue_10", 0x21)
	book.set_colour_RGB(0x21, 153,204,255)
	xlwt.add_palette_colour("blue_classic", 0x22)
	book.set_colour_RGB(0x22, 207,231,245)
	xlwt.add_palette_colour("hijau_tua", 0x23)
	book.set_colour_RGB(0x23, 0,204,0)
	xlwt.add_palette_colour("hijau_muda", 0x24)
	book.set_colour_RGB(0x24, 153,255,153)
	xlwt.add_palette_colour("kuning", 0x25)
	book.set_colour_RGB(0x25, 255,255,0)
	xlwt.add_palette_colour("merah", 0x26)
	book.set_colour_RGB(0x26, 255,51,51)


	sheet1 = book.add_sheet('PIC', cell_overwrite_ok = True)
	sheet1.row(0).height_mismatch = True
	sheet1.row(0).height = 360
	styleTitle = 'pattern: pattern solid, fore_colour white;'
	styleTitle += 'align: vertical center, horizontal center, wrap on;'
	styleTitle += 'font: name Tahoma, height 280, bold 1;'

	sheet1.write_merge(offRow, offRow, offCol, offCol+19, 'ATM PRO ' + RegionName + ' PER CLUSTER' , xlwt.easyxf(styleTitle))
	shiftDown = 1

	sheet1.row(1).height_mismatch = True
	sheet1.row(1).height = 360
	sheet1.write_merge(offRow+shiftDown, offRow+shiftDown, offCol, offCol+19, 'posisi tanggal ' +time.strftime("%d/%m/%Y-%H:%M") , xlwt.easyxf(styleTitle))
	contentAlignmentHorz = ["center", "right", "center", "center", "center", "center", "center", "center", "center"]


	def styler(strColor,  fontHeight):

		styleHeader = 'pattern: pattern solid, fore_colour '+strColor+';'
		styleHeader += 'align: vertical center, horizontal center, wrap on;'
		styleHeader += 'borders: top thin, bottom thin;'
		styleHeader += 'font: name Tahoma, height '+str(fontHeight)+', bold 1;'
				
		return styleHeader


	def makeHeader(xRow, yCol, jenisTabel):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+7, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "NOP", "RSK", "OPS", "OOS", "OFF", "JML"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))


	# TABULASI RANKING PROBLEM  ----------------------------------------------------
	makeHeader(offRow, offCol, 'BY PROBLEM')
	sheet1.col(offCol+0).width = 5*315
	sheet1.col(offCol+1).width = 22*315
	sheet1.col(offCol+2).width = 4*315
	sheet1.col(offCol+3).width = 4*315
	sheet1.col(offCol+4).width = 4*315
	sheet1.col(offCol+5).width = 4*315
	sheet1.col(offCol+6).width = 4*315
	sheet1.col(offCol+7).width = 4*315
	sheet1.col(offCol+8).width = 8*315

	shiftDownSeparator = 0
	headRow = []

	for i in range (0, len(TProblem)):

		if TProblem[i-1][8] != TProblem[i][8]:
			separatorStyle = 'borders: top thin, bottom thin;'
			separatorStyle += 'font: name Tahoma, height 180, bold 1;'
			separatorStyle += 'pattern: pattern solid, fore_colour white;'
			separatorStyle += 'align: horiz center'
			shiftDownSeparator +=1
			headRow.append(i+shiftDownSeparator+5)
			sepStyle = xlwt.easyxf(separatorStyle)
			r = i+offRow+4*shiftDown+shiftDownSeparator-1
			c = offCol
			sheet1.write(r, c, "", sepStyle)
			sheet1.write(r, c+1, TProblem[i][8].upper(), sepStyle)

		for j in range(0,len(TProblem[i])-1):

			strColor = colorProblem(TProblem[i][7])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[j]
			style = xlwt.easyxf(contentStyle)
			cellContent = TProblem[i][j]
			if j == len(TProblem[i])-1:
					cellContent = Formula("SUM(C"+str(i+shiftDownSeparator+5)+":H"+str(i+shiftDownSeparator+5)+")")

			if cellContent	== 0:
				cellContent = '-'

			sheet1.write(i+offRow+4*shiftDown+shiftDownSeparator, j+offCol, cellContent, style)
			lastRow = i+offRow+4*shiftDown+shiftDownSeparator+3

	headRow.append(lastRow)
	# PROBLEM ----------------------------------------------------
	for k in range (0, len(headRow)-1):

		sheet1.write(headRow[k]-2, c+2, Formula("SUM(C"+str(headRow[k])+":C"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, c+3, Formula("SUM(D"+str(headRow[k])+":D"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, c+4, Formula("SUM(E"+str(headRow[k])+":E"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, c+5, Formula("SUM(F"+str(headRow[k])+":F"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, c+6, Formula("SUM(G"+str(headRow[k])+":G"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, c+7, Formula("SUM(H"+str(headRow[k])+":H"+str(headRow[k+1]-2)+")"), sepStyle)
	# PROBLEM ----------------------------------------------------




	shiftLeft = 9

	def makeHeader2(xRow, yCol, jenisTabel):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+5, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "UP", "TUNAI", "NON", "%"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))

	makeHeader2(offRow, offCol+shiftLeft, "BY UTILITY")
	sheet1.col(offCol+shiftLeft-1).width = 2*315
	sheet1.col(offCol+shiftLeft+0).width = 5*315
	sheet1.col(offCol+shiftLeft+1).width = 22*315
	sheet1.col(offCol+shiftLeft+2).width = 5*315
	sheet1.col(offCol+shiftLeft+3).width = 6*315
	sheet1.col(offCol+shiftLeft+4).width = 4*315
	sheet1.col(offCol+shiftLeft+5).width = 5*315

	shiftDownSeparator = 0
	headRow = []

	for k in range (0, len(TUtility)):

		if TUtility[k-1][6] != TUtility[k][6]:
			separatorStyle = 'borders: top thin, bottom thin;'
			separatorStyle += 'font: name Tahoma, height 180, bold 1;'
			separatorStyle += 'pattern: pattern solid, fore_colour white;'
			separatorStyle += 'align: horiz center'
			shiftDownSeparator +=1
			sepStyle = xlwt.easyxf(separatorStyle)
			r = k+offRow+4*shiftDown+shiftDownSeparator-1
			headRow.append(r+2)
			c = offCol+shiftLeft
			sheet1.write(r, shiftLeft, "", sepStyle)
			sheet1.write(r, shiftLeft+1, TUtility[k][6].upper(), sepStyle)
			sheet1.write(r, shiftLeft, "", sepStyle)
			sheet1.write(r, shiftLeft, "", sepStyle)

		for l in range(0,len(TUtility[k])-1):

			strColor = colorUtility(TUtility[k][5])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[l]

			cellContent = TUtility[k][l]
			if cellContent	== 0:
				cellContent = '-'

			style = xlwt.easyxf(contentStyle)
			sheet1.write(k+offRow+4*shiftDown+shiftDownSeparator, l+offCol+shiftLeft, cellContent, style)
			lastRow = k+offRow+4*shiftDown+shiftDownSeparator+3

	headRow.append(lastRow)
	#print headRow, len(headRow)
	# UTILITY ----------------------------------------------------
	for k in range (0, len(headRow)-1):

		sheet1.write(headRow[k]-2, shiftLeft+2, Formula("SUM(L"+str(headRow[k])+":L"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, shiftLeft+3, Formula("SUM(M"+str(headRow[k])+":M"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, shiftLeft+4, Formula("SUM(N"+str(headRow[k])+":N"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, shiftLeft+5, Formula("(M"+str(headRow[k]-1)+"/L"+str(headRow[k]-1)+")*100"), xlwt.easyxf(separatorStyle,num_format_str= '0.00'))


	# AVAILABILITY ----------------------------------------------------

	shiftLeft = 16

	def makeHeader3(xRow, yCol, jenisTabel):

		sheet1.write_merge(xRow+2*shiftDown, xRow+2*shiftDown, yCol, yCol+3, 'RANKING ' + jenisTabel, xlwt.easyxf(styler('sky_blue_10', 240)))
	
		arrJudul = ["CODE", "BRANCH", "ATM", "%"]

		for i in range (0, len(arrJudul)):

			sheet1.write(xRow+3*shiftDown , i+yCol, arrJudul[i], xlwt.easyxf(styler('blue_classic', 180)))



	makeHeader3(offRow, offCol+shiftLeft, "BY AVAILABILITY")
	#print TAvailability
	sheet1.col(offCol+shiftLeft-1).width = 2*315
	sheet1.col(offCol+shiftLeft+0).width = 5*315
	sheet1.col(offCol+shiftLeft+1).width = 22*315
	sheet1.col(offCol+shiftLeft+2).width = 5*315
	sheet1.col(offCol+shiftLeft+3).width = 7*315
	sheet1.col(offCol+shiftLeft+4).width = 8*315

	shiftDownSeparator = 0
	headRow = []

	for m in range (0, len(TAvailability)):

		if TAvailability[m-1][4] != TAvailability[m][4]:
			separatorStyle = 'borders: top thin, bottom thin;'
			separatorStyle += 'font: name Tahoma, height 180, bold 1;'
			separatorStyle += 'pattern: pattern solid, fore_colour white;'
			separatorStyle += 'align: horiz center'
			shiftDownSeparator +=1
			sepStyle = xlwt.easyxf(separatorStyle)
			r = m+offRow+4*shiftDown+shiftDownSeparator-1
			c = offCol+shiftLeft
			headRow.append(r+2)
			sheet1.write(r, c, "", sepStyle)
			sheet1.write(r, c+1, TAvailability[m][4].upper(), sepStyle)
			tempSum = 0

		for n in range(0,len(TAvailability[m])-1):

			strColor = colorAvail(TAvailability[m][3])
			contentStyle = 'font: name Tahoma, height 180;'
			contentStyle += 'pattern: pattern solid, fore_colour '+strColor+';'
			contentStyle += 'align: horiz '+contentAlignmentHorz[n]

			style = xlwt.easyxf(contentStyle)
			sheet1.write(m+offRow+4*shiftDown+shiftDownSeparator, n+offCol+shiftLeft, TAvailability[m][n], style)

			strFormula = "PRODUCT(S" + str(m+offCol+shiftLeft+shiftDownSeparator-shiftLeft+5)+ ":T" +str(m+offCol+shiftLeft+shiftDownSeparator-shiftLeft+5)+")"
			sheet1.write(m+offRow+4*shiftDown+shiftDownSeparator, shiftLeft+4, Formula(strFormula), xlwt.easyxf('font: color white;'))

			lastRow = m+offRow+4*shiftDown+shiftDownSeparator+3

	headRow.append(lastRow)
	
	# AVAILABILITY ----------------------------------------------------
	for k in range (0, len(headRow)-1):

		sheet1.write(headRow[k]-2, shiftLeft+2, Formula("SUM(S"+str(headRow[k])+":S"+str(headRow[k+1]-2)+")"), sepStyle)
		sheet1.write(headRow[k]-2, shiftLeft+3, Formula("U"+str(headRow[k]-1)+"/S"+str(headRow[k]-1)), xlwt.easyxf(separatorStyle,num_format_str= '0.00'))
		sheet1.write(headRow[k]-2, shiftLeft+4, Formula("SUM(U"+str(headRow[k])+":U"+str(headRow[k+1]-2)+")"), xlwt.easyxf('font: color white;') )

	headRow.append(lastRow)

	namaFileXLS = prepareDirectory("OUTPUT") + RegionName + "-ATM PRO PER CLUSTER-" +time.strftime("%Y%m%d-%H")+'.xls'

	book.save(namaFileXLS)

	# MATHEMATICAL CALCULATION ----------------------------------------------------
	UP, TUNAI, NONTUNAI, PERCENT = 0, 0, 0, 0
	for i in range(0,len(TUtility)):
		
		clusterName = TUtility[i][-1].upper()
		if clusterName == "Jakbar".upper():
			UP += TUtility[i][2]
			TUNAI += TUtility[i][3]
			NONTUNAI += TUtility[i][4]

	PERCENT = float(float(TUNAI)/float(UP)*100)
	print "NOP=", UP, TUNAI, NONTUNAI, "{0:.2}".format(PERCENT)
		#TProblem.append((kodeCabang, namaCabang, NOP, RSK, PROBOPS, OOS, OFF, PROB, PICName))
		#TUtility.append((kodeCabang, namaCabang, UP, TUNAI, NONTUNAI, float("{0:.2}".format(PERCENT)),PICName))

def main():

	alamatURL = 'http://atmpro.bri.co.id/statusatm/dashboard_cabang.pl?REGID=15&REGNAME=Jakarta%20III'
	strHTML = fetchHTML(alamatURL)
	table = getLargestTable(getTableList(strHTML))
	TProblem, TUtility, TAvailability = getTableContents(table)
	putDataXL(0, 0, TProblem, TUtility, TAvailability)

main()
