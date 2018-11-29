import urllib.request
import urllib.response
import http.cookiejar
import http.client
import csv
import json
import re
import math
from html.parser import HTMLParser
from bs4 import BeautifulSoup

class Csvrow:
	def __init__(self):
		self.row = {"Handle":"",
					"Title":"",
					"Body (HTML)":"",
					"Vendor":"",
					"Type":"",
					"Tags":"",
					"Published": "TRUE",
					"Option1 Name":"Title",
					"Option1 Value":"Default Title",
					# "Option2 Name":"",
					# "Option2 Value":"",
					# "Option3 Name":"",
					# "Option3 Value":"",
					"Variant SKU":"",
					"Variant Grams":"",
					# "Variant Inventory Tracker":"",
					"Variant Inventory Qty":"1",
					"Variant Inventory Policy":"deny",
					"Variant Fulfillment Service":"manual",
					"Variant Price":"",
					"Variant Compare At Price":"",
					"Variant Requires Shipping":"TRUE",
					"Variant Taxable":"TRUE",
					# "Variant Barcode":"",
					"Image Src":"",
					# "Image Alt Text":"",
					"Gift Card":"FALSE",
					# "SEO Title":"",
					# "SEO Description":"",
					# "Google Shopping / Google Product Category":"",
					# "Google Shopping / Gender":"",
					# "Google Shopping / Age Group":"",
					# "Google Shopping / MPN":"",
					# "Google Shopping / AdWords Grouping":"",
					# "Google Shopping / AdWords Labels":"",
					# "Google Shopping / Condition":"",
					# "Google Shopping / Custom Product":"",
					# "Google Shopping / Custom Label 0":"",
					# "Google Shopping / Custom Label 1":"",
					# "Google Shopping / Custom Label 2":"",
					# "Google Shopping / Custom Label 3":"",
					# "Google Shopping / Custom Label 4":"",
					# "Variant Image":"",
					"Variant Weight Unit":"lb"}

def rowSorter(hasInfo, hasDesc, hasMap, productrow, headers):
	
	row = productrow.row
	# print(row)
	try:
		if hasInfo == False and hasMap == False:
			print("No info and no MAP")
			with open("no-info-no-map.csv", "a", newline="") as noINFOnoMAP:
				noINFOnoMAPwriter = csv.DictWriter(noINFOnoMAP, headers, dialect="excel", delimiter=",")
				noINFOnoMAP.writerow(row)			
		elif hasDesc == False and hasMap == True:
			print("No description.")
			with open("no-body.csv", "a", newline="") as noDESC:
				noDESCwriter = csv.DictWriter(noDESC, headers, dialect="excel", delimiter=",")
				noDESCwriter.writerow(row)
		elif hasDesc == False and hasMap == False:
			print("No description and no MAP")
			with open("no-body-no-map.csv", "a", newline="") as noDESCnoMAP:
				noDESCnoMAPwriter = csv.DictWriter(noDESCnoMAP, headers, dialect="excel", delimiter=",")
				noDESCnoMAPwriter.writerow(row)
		elif hasMap == False:
			print("No MAP")
			with open("no-map-only.csv", "a", newline="") as noMAP:
				noMAPwriter = csv.DictWriter(noMAP, headers, dialect="excel", delimiter=",")
				noMAPwriter.writerow(row)
		else:
			print("Found all data")
			with open("finalwebsite.csv", "a", newline="") as finalwebsite:
				finalwebsitewriter = csv.DictWriter(finalwebsite, headers, dialect="excel", delimiter=",")
				finalwebsitewriter.writerow(row)
	except:
		row["Body (HTML)"] = ""
		with open("no-body.csv", "a", newline="") as noDESC:
				noDESCwriter = csv.DictWriter(noDESC, headers, dialect="excel", delimiter=",")
				noDESCwriter.writerow(row)

if __name__ == '__main__':
	productrow = Csvrow()
	# login details - hardcoded for now.
	username	= 'xxxxxxxxxx'
	password	= 'xxxxxxxxxx'

	values 		= urllib.parse.urlencode({'username':username,'pass':password})
	binary_data = values.encode('UTF-8')
	headers 	= {"Content-type": "application/x-www-form-urlencoded",
						 "Accept": "text/plain"}
	
	# keeps session cookies.
	cj = http.cookiejar.CookieJar()
	# uses cj above to manage cookies
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
	urllib.request.install_opener(opener)

	# sends a POST with the username and password to start the logged in session.
	request = urllib.request.Request('xxxxxxxxxxx', binary_data)
	response = opener.open(request)

	# debug.
	print(response.status, response.reason)
		
	# column content for the csv to be imported to website autosports webpage
	headers = []
	with open("products_export.csv", newline="") as products_export:
		prodreader = csv.DictReader(products_export, delimiter=",")
		# get the first line of the csv (column headers)
		prodline = prodreader.__next__()
		headers = prodreader._fieldnames
		print(prodreader._fieldnames)

		# files opened with "w" are truncated (overwritten)
		with open("products_export.csv", "w", newline="") as finalwebsite:
			finalwriter = csv.DictWriter(finalwebsite, prodreader._fieldnames, dialect="excel",delimiter=",")
			finalwriter.writeheader()

		with open("no-map-only.csv", "w", newline="") as noMAP:
			noMAPwriter = csv.DictWriter(noMAP, prodreader._fieldnames, dialect="excel", delimiter=",")
			noMAPwriter.writeheader()

		with open("no-info-no-map.csv", "w", newline="") as noINFOnoMAP:
			noINFOnoMAPwriter = csv.DictWriter(noINFOnoMAP, prodreader._fieldnames, dialect="excel", delimiter=",")
			noINFOnoMAPwriter.writeheader()	

		with open("no-body.csv", "w", newline="") as noDESC:
			noDESCwriter = csv.DictWriter(noDESC, prodreader._fieldnames, dialect="excel", delimiter=",")
			noDESCwriter.writeheader()

		with open("no-body-no-map.csv", "w", newline="") as noDESCnoMAP:
			noDESCnoMAPwriter = csv.DictWriter(noDESCnoMAP, prodreader._fieldnames, dialect="excel", delimiter=",")
			noDESCnoMAPwriter.writeheader()
			
	with open("websitet14.csv", newline="") as csvfile:
		# variables added to a list
		
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:			
			info = False
			description = False
			maPrice = False
			# row[2] contains the internal part number for website
			request = urllib.request.Request('http://www.website.com/search.php?search='+row[2]+'&type=Part+%23')
			response = opener.open(request)
			pagedata = response.read()
			soup = BeautifulSoup(pagedata.decode('utf-8', 'ignore'))

			
			# Cost, Retail, Jobber, and Map area on the websitet14.csv
			# row[4], row[5], row[6], and row[7] respectively
			
			productrow.row["Vendor"] = row[0]

			productrow.row["Variant SKU"] = row[2]
			if row[5] != "\\N":
				# the retail price that's marked out on the webpage
				productrow.row["Variant Compare At Price"] = row[5]

			productrow.row["Variant Price"] = row[7]
			if productrow.row["Variant Price"] != "\\N":
				maPrice = True
				# the MAP value that is shown as the current price on the webpage

			try:
				partDescList = list((soup.find("div", class_="search-v4-product-info").stripped_strings))
				Title = partDescList[7].upper()
				Handle = partDescList[7].replace(' ', '-').lower()
				Handle = re.sub(r'\-\([^)]*\)', '', Handle)
				Handle = re.sub(r'\/', '-', Handle)
				productrow.row["Title"] = Title
				productrow.row["Handle"] = Handle
				info = True
			except:
				# info still default false
				print("There is no title or handle info for this part.")
				# if info == False and maPrice == '\\N':
				# 	# put this row into the no-info-no-map.csv
				# 	rowSorter(info, description, maPrice)

			if "value=\'Product Info\'" not in pagedata.decode("utf-8"): 
				description = False
				print(row[2] + 'does not have product info')
				# rowSorter(info, description, maPrice)

			else:
				print(row[2])

				valueToSearch = soup.find("input", class_="button small orange")["name"]

				request = urllib.request.Request('http://www.website.com/search/product_info.php?pn='+valueToSearch)
				response = opener.open(request)
				pagedata = response.read()
				infoSoup = BeautifulSoup(pagedata.decode('utf-8', 'ignore'))

				productOverview = infoSoup.find("div", id="product_overview")
				try:
					productrow.row["Body (HTML)"] = ''.join(str(t) for t in productOverview.children)
					description = True
				except:
					print("The body of this description is empty.")
					description = False

				otherInfo = infoSoup.findAll("div", class_="half")
				if(otherInfo[1] is not None) or (len(otherInfo[1]) != 0):
					otherInfoList = list(otherInfo[1].stripped_strings)
					# get the last index position
					productrow.row["Type"] = otherInfoList[len(otherInfoList)-1]
				try:
					soup2 = infoSoup.find("tr", class_="odd")
					infoChildren = soup2.findChildren()
					startYear= infoChildren[0].string
					endYear  = infoChildren[1].string
					make 	 = infoChildren[2].string
					model	 = infoChildren[3].string
					years 	 = []
					tags	 = []
					Tags = ""
					productrow.row["Tags"] = ""

					# print(startYear, endYear, make, model)					
					try:
						for i in range(int(startYear),int(endYear)+1):
							years.append(i)
							tags.append(i)
						# print(tags, make, model)
						tags.append(make)
						tags.append(model)
						for t in tags:
							Tags += str(t) + ", "
						print("Tags are: ",Tags)
						productrow.row["Tags"] = Tags[:-2] # remove last two positions on the Tags variable			
					except ValueError:
						print("No years given for this part: ", row[2])			
						
				except AttributeError:
					print("There is no year info listed for this product.")
				try:
					ImageSrc = infoSoup.find("img", class_="product-image-large")["src"]
				except:
					print("There is no image for this product.")
				if ImageSrc != None:
					productrow.row["Image Src"] = ImageSrc

				if row[5] != "\\N":
					productrow.row["Variant Compare At Price"] = row[5] #retail price

				try:
					lbsToGrams = math.ceil(float(row[13]) / 0.0022046)
					productrow.row["Variant Grams"] = str(lbsToGrams)
				except:
					print("could not get grams for this part.")
				
				# print(info, description, maPrice)
				print(productrow.row["Tags"])
				rowSorter(info, description, maPrice, productrow, headers)
