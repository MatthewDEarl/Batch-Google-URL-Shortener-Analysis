import sys
import json
import urllib2
import csv

INPUT_FILE = 'shorturl.csv'
OUTPUT_FILE = 'clicks.csv'

def getArrayOfShortURLsFromFile(fileURL):
	shortURLs = []

	csvFile = open(fileURL, "rb")
	try:
		csvReader = csv.reader(csvFile, dialect='excel')
		for item in csvReader:
			shortURLs.append(item[0])
	finally:
		csvFile.close()

	return shortURLs

def useGoogleAPIToReceiveClicksForAllTimeForArrayOfShortURLs(shortURLs):
	clicks = []

	for url in shortURLs:
		data = getJSONForURL(url)
		clicks.append(int(data['analytics']['allTime']['shortUrlClicks']))

	return clicks

def getJSONForURL(url):
	apiURL = 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=' + url + '&projection=FULL'
	urlRequest = urllib2.urlopen(apiURL)
	data = json.load(urlRequest)
	
	return data

def writeOutputToFile(urls, output, outputFile):
	assert len(urls) == len(output) # will only work with equal arrays

	csvOutputFile = open('clicks.csv',"wb")
	try:
		csvWriter = csv.writer(csvOutputFile, delimiter=',',quotechar='"',quoting=csv.QUOTE_NONNUMERIC)

		for i in range(0, len(urls)):
			# Add column headings on first iteration
			if i == 0:
				csvWriter.writerow(['URL','Clicks'])
			
			csvWriter.writerow([urls[i],output[i]])
	finally:
		csvOutputFile.close()

def runWithArguments(inputFile, outputFile):
	urls = getArrayOfShortURLsFromFile(inputFile)
	output =  useGoogleAPIToReceiveClicksForAllTimeForArrayOfShortURLs(urls)
	writeOutputToFile(urls, output, outputFile)

# Run the program with arguments or fall back to defaults
if len(sys.argv) == 3:
	runWithArguments(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 1:
	runWithArguments(INPUT_FILE, OUTPUT_FILE)
else:
	print "Usage error: expected zero or two arguments"