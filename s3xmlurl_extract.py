"""
A simple python script to parse all the urls form a S3 XML file.
"""
import requests
import bs4
import lxml
import sys

if len(sys.argv) > 1 :
    s3_url = sys.argv[1]
else:
    print("Please give s3 url ")
    exit(1)

req = requests.get(s3_url)
xml = bs4.BeautifulSoup(req.text, 'lxml')
keys = xml.find_all('key')
keys_data = [key.text for key in keys]

with open('s3_urls.txt', 'a+') as file:
    for id in keys_data:
        url = s3_url + id
        st = requests.head(url).status_code
        file.write("[" + str(st) + "] " + url + "\n")
