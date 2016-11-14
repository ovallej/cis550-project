import sys
import csv
import optparse
import json
import glob


insert_countries = "INSERT INTO Countries VALUES (%s, %d, %f, %d)"
insert_countries % ("'country_name'", 2, 6.8, 1000)
#COUNTRY_NAME, GDP,	Unemployment,	 POPULATION

def parse_factbook() :

	folders = ['africa', 'antarctica', 'australia-oceania', 'central-america-n-caribbean', 'central-asia', 'east-n-southeast-asia', 'europe', 'middle-east', 'north-america', 'south-america', 'south-asia']
	relativePath = 'factbook_data/'
	extension = '/*.json'

	allFilesToParse = []

	for folder in folders :
		allFilesToParse.extend(glob.glob(relativePath + folder + extension))

	for fileName in allFilesToParse :
		data = json.load(open(fileName))
		gdpNum = 0
		unemploymentNum = 0.0
		populationNum = 0

		name = "ASFDFDSKJNSDKJNFKJNLSDG"
		if 'Government' in data and 'Country name' in data['Government'] :
			if 'conventional short form' in data['Government']['Country name']:
				name = str(data['Government']['Country name']['conventional short form']['text'])
				if name == "none" :
					name = str(data['Government']['Country name']['conventional long form']['text'])
			elif 'Dutch short form' in data['Government']['Country name'] :
				name = str(data['Government']['Country name']['Dutch short form']['text'])
			else :
				"asdf"
				# print "COULDN'T PARSE NAME"

		if name == "ASFDFDSKJNSDKJNFKJNLSDG":
			continue
		# print name
		if 'Economy' in data and 'GDP (purchasing power parity)' in data['Economy'] :
			gdpText = str(data['Economy']['GDP (purchasing power parity)']['text'])
			formattedGDP = gdpText[1:]
			formattedGDP = formattedGDP.split()

			gdpNum = 0
			if len(formattedGDP) >= 2 :
				if formattedGDP[1] == 'million' :
					gdpNum = int(float(formattedGDP[0]) * 1000000)
				elif formattedGDP[1] == 'billion' :
					gdpNum = int(float(formattedGDP[0]) * 1000000000)
				elif formattedGDP[1] == 'trillion' :
					gdpNum = int(float(formattedGDP[0]) * 1000000000000)
				else :
					"asdf"
					# print "INVALID FORMATTING OF GDP"
		else :
			gdpNum = 0

		if 'Economy' in data and 'Unemployment rate' in data['Economy'] :
			unemploymentText = str(data['Economy']['Unemployment rate']['text'])

			formattedUnemployment = unemploymentText.split()
			unemploymentStr = formattedUnemployment[0][:-1]
			if unemploymentStr != "NA" :
				unemploymentNum = float(unemploymentStr)

		else :
			unemploymentNum = 0.0

		if 'People and Society' in data and 'Population' in data['People and Society'] :
			populationText = str(data['People and Society']['Population']['text'])
			formattedPopulation = populationText.split()

			populationStr = formattedPopulation[0].replace(',', '')

			if len(populationStr) < 10 :
				if not populationStr[0].isalpha() :
					if '.' in populationStr :
						if formattedPopulation[1] == 'million' :
							gdpNum = int(float(populationStr) * 1000000)
						elif formattedPopulation[1] == 'billion' :
							gdpNum = int(float(populationStr) * 1000000000)
						else :
							"asdf"
							# print "INVALID FORMATTING OF POPULATION"
					else :
						populationNum = int(populationStr)

		else :
			populationNum = 0

		print insert_countries % ("'" + name + "'", 
									 gdpNum,
									 unemploymentNum,
									 populationNum)




if __name__ == '__main__' : 
	parse_factbook()

