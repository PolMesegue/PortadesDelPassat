#!/usr/bin/env python3
import sys
import wget
import shutil
import os
import tweepy

from datetime import datetime
from dateutil.relativedelta import relativedelta
from pdf2image import convert_from_path

try:
	os.mkdir('temporal')

	keys_file = open("keys.txt")
	lines = keys_file.readlines()
	CONSUMER_KEY = lines[0].rstrip()
	CONSUMER_SECRET = lines[1].rstrip()
	ACCESS_KEY = lines[2].rstrip()
	ACCESS_SECRET = lines[3].rstrip()
	keys_file.close()

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	#Time relative work

	years_elapsed=int(sys.argv[1])
	year_ago = datetime.now() - relativedelta(years=years_elapsed)
	year = year_ago.strftime("%Y")
	lc_year = year_ago.strftime("%y")
	month = year_ago.strftime("%m")
	day = year_ago.strftime("%d")

	aux=['E','F','M','A','Y','J','L','G','S','O','N','D']
	letter_month=aux[int(month)-1]

	#LaVanguardia
	try:
		url = f'http://hemeroteca-paginas.lavanguardia.com/LVE05/PUB/{year}/{month}/{day}/LVG{year}{month}{day}0011LB.pdf'
		wget.download(url, 'temporal/lavanguardia.pdf')

		pages = convert_from_path('temporal/lavanguardia.pdf', 500)

		for page in pages:
			page.save('temporal/lavanguardia.jpg', 'JPEG')

		
	#ABC
	try:
		url = f'http://hemeroteca.abc.es/cgi-bin/pagina.pdf?fn=exec;command=stamp;path=H:\cran\data\prensa_pages\Madrid\ABC\{year}\{year}{month}\{year}{month}{day}\{lc_year}{letter_month}{day}-001.xml;id=0006839617#view=Fit'
		wget.download(url, 'temporal/abc.pdf')
		pages = convert_from_path('temporal/abc.pdf', 500)

		for page in pages:
	    		page.save('temporal/abc.jpg', 'JPEG')

	#ElPais
	try:
		url = f'https://srv00.epimg.net/pdf/elpais/snapshot/{year}/{month}/elpais/{year}{month}{day}Big.jpg'
		wget.download(url, 'temporal/elpais.jpg')


	filenames = ['temporal/elpais.jpg', 'temporal/lavanguardia.jpg', 'temporal/abc.jpg']
	uploaded_ids = []
	for filename in filenames:
		res = api.media_upload(filename)
		uploaded_ids.append(res.media_id)

	anyoanys = 'any' if years_elapsed == 1 else 'anys'

	api.update_status(status= f'Portades dels principals diaris {years_elapsed} {anyoanys} enrere, dia {day}/{month}/{year}', media_ids=uploaded_ids)

except:
	uploaded_ids = []
	res = api.media_upload('fail.jpg')
	uploaded_ids.append(res.media_id)
	api.update_status("Per motius tècnics, no ha sigut possible la piulada, ho intentarem de nou en breus instants", media_ids=uploaded_ids)

finally:
	shutil.rmtree('temporal')
