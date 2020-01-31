#!/usr/bin/env python3
import sys
import wget
import shutil
import os

from datetime import datetime
from dateutil.relativedelta import relativedelta
from twython import Twython
from pdf2image import convert_from_path

keys_file = open("../keys.txt")
lines = keys_file.readlines()
CONSUMER_KEY = lines[0].rstrip()
CONSUMER_SECRET = lines[1].rstrip()
ACCESS_KEY = lines[2].rstrip()
ACCESS_SECRET = lines[3].rstrip()

os.mkdir('./temporal')

#Time relative work

year_ago = datetime.now() - relativedelta(years=int(sys.argv[1]))
year = year_ago.strftime("%Y")
lc_year = year_ago.strftime("%y")
month = year_ago.strftime("%m")
day = year_ago.strftime("%d")

if month == "01":
	letter_month = "E"
elif month == "02":
	letter_month = "F"
elif month == "03":
	letter_month = "M"
elif month == "04":
	letter_month = "A"
elif month == "05":
	letter_month = "Y"
elif month == "06":
	letter_month = "J"
elif month == "07":
	letter_month = "L"
elif month == "08":
	letter_month = "G"
elif month == "09":
	letter_month = "S"
elif month == "10":
	letter_month = "O"
elif month == "11":
	letter_month = "N"
else:
	letter_month = "D"

#LaVanguardia
url = f'http://hemeroteca-paginas.lavanguardia.com/LVE05/PUB/{year}/{month}/{day}/LVG{year}{month}{day}0011LB.pdf'
wget.download(url, './temporal/lavanguardia.pdf')

pages = convert_from_path('./temporal/lavanguardia.pdf', 500)

for page in pages:
    page.save('./temporal/lavanguardia.jpg', 'JPEG')

#ABC

url = f'http://hemeroteca.abc.es/cgi-bin/pagina.pdf?fn=exec;command=stamp;path=H:\cran\data\prensa_pages\Madrid\ABC\{year}\{year}{month}\{year}{month}{day}\{lc_year}{letter_month}{day}-001.xml;id=0006839617#view=Fit'
wget.download(url, './temporal/abc.pdf')
pages = convert_from_path('./temporal/abc.pdf', 500)

for page in pages:
    page.save('./temporal/abc.jpg', 'JPEG')

#ElPais

url = f'https://srv00.epimg.net/pdf/elpais/snapshot/{year}/{month}/elpais/{year}{month}{day}Big.jpg'
wget.download(url, './temporal/elpais.jpg')

twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 

image_filenames = ['./temporal/elpais.jpg', './temporal/lavanguardia.jpg', './temporal/abc.jpg']
uploaded_ids = []
for fname in image_filenames:
	with open(fname, 'rb') as img:
		twit_resp = twitter.upload_media(media=img)
		uploaded_ids.append(twit_resp['media_id'])

twitter.update_status(status= f'Portades dels principals diaris {sys.argv[1]} any/s enrere, dia {day}/{month}/{year}', media_ids=uploaded_ids)

shutil.rmtree('./temporal')
