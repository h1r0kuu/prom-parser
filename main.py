import csv
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Prom:
	def __init__(self):
		self.url = 'https://prom.ua/Shampuni-dlya-volos'

	def get_text(self, url):
		header = {
			'authority': 'https://prom.ua/',
			'method': 'GET',
			'scheme': 'https',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
			'cache-control': 'max-age=0',
			'dnt': '1',
			'referer': url,
			'upgrade-insecure-requests': '1',
			'user-agent': UserAgent().random,
		}
		return requests.get(url, headers=header).text
	
	def get_max_page(self):
		soup = BeautifulSoup(self.get_text(self.url), 'lxml')
		div = soup.select_one('div.x-pager__content')
		a = div.select('a.x-pager__item')[-2].get('data-page')
		return a


	def block(self, url):
		soup = BeautifulSoup(self.get_text(url), 'lxml')
		block = soup.select('div.x-gallery-tile.js-gallery-tile.js-productad.x-gallery-tile_type_click')
		for div in block:
			url = div.select_one('a.x-gallery-tile__tile-link').get('href')
			self.parse_url(url)
	def parse_url(self,url):
		try:
			soup = BeautifulSoup(self.get_text(url), 'lxml')
		except:
			print('Error in url - {}'.format(url))
		try:
			title = soup.select_one('h1.x-title').text
		except:
			title = ''
		try:
			price = soup.select_one('span.x-hidden').select('span')[0].text.strip()
		except:
			price = ''
		try:
			number = soup.select_one('span.x-pseudo-link.x-iconed-text__link.js-product-ad-conv-action').get('data-pl-main-phone')
		except:
			number = ''
		try:
			place = soup.select_one('div.x-iconed-text__text')
		except:
			print('Place error')
		try: 
			city = place.select_one('span.x-pseudo-link').text
		except: 
			city = ''
		try:	
			street = place.select_one('div.x-iconed-text__address').get('data-comaddr-address-text')
		except:
			street = ''
		data = {
			'title': title,
			'price': price,
			'number': number,
			'city': city,
			'street': street,
			'url':url
		}
		self.write_csv( data )

	def write_csv(self,data):
		with open('prom.csv', 'a') as f:
			writer = csv.writer(f)
			if data['title'] != '' or data['price'] != '' or data['number'] != '' or data['city'] != '' or data['street'] != '' or data['url'] != '':
				writer.writerow((data['title'], data['price'], data['number'], data['city'], data['street'], data['url']))
			else:
				print('Пустота')
	def run(self):
		for i in range(1,int(self.get_max_page())-1):
			self.block(self.url+f';{i}')
