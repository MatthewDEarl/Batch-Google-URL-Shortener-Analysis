"""
Author: Matthew Earl <matthew.earl@me.com>
"""

import sys
import json
import urllib2
import csv

INPUT_FILE = 'shorturl.csv'
OUTPUT_FILE = 'clicks.csv'

def get_array_of_short_URLs_with_file(fileURL):
	shortURLs = []

	csvFile = open(fileURL, "rb")
	try:
		csvReader = csv.reader(csvFile, dialect='excel')
		for item in csvReader:
			shortURLs.append(item[0])
	finally:
		csvFile.close()

	return shortURLs

def use_google_short_URL_API_to_receive_clicks_with_array_of_short_URLs(shortURLs):
	clicks = []

	for url in shortURLs:
		data = get_JSON_with_URL(url)
		clicks.append(int(data['analytics']['allTime']['shortUrlClicks']))

	return clicks

def get_JSON_with_URL(url):
	apiURL = 'https://www.googleapis.com/urlshortener/v1/url?shortUrl=' + url + '&projection=FULL'
	urlRequest = urllib2.urlopen(apiURL)
	data = json.load(urlRequest)
	
	return data

def write_output_to_file(urls, output, outputFile):
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

def run_with_arguments(inputFile, outputFile):
	urls = get_array_of_short_URLs_with_file(inputFile)
	output =  use_google_short_URL_API_to_receive_clicks_with_array_of_short_URLs(urls)
	write_output_to_file(urls, output, outputFile)

# Run the program with arguments or fall back to defaults
if len(sys.argv) == 3:
	assert sys.argv[1].endswith(".csv") && sys.argv[2].endswith(".csv")
	run_with_arguments(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 1:
	run_with_arguments(INPUT_FILE, OUTPUT_FILE)
else:
	print "Usage error: expected zero or two arguments"