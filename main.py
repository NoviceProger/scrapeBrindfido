from builtins import print

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random

urlldict = []
urlldict.append(
		{
			'url': "https://www.bringfido.com/lodging/hotels/region/united_states/",
			'type': "Hotels",
			'namefile': "Hotels"
		}
	)
urlldict.append(
		{
			'url': "https://www.bringfido.com/lodging/rentals/region/united_states/",
			'type': "Vacation Rentals",
			'namefile': "Rentals"
		}
	)
urlldict.append(
		{
			'url': "https://www.bringfido.com/lodging/bandbs/region/united_states/",
			'type': "Bed & Breakfasts",
			'namefile': "Bandbs"
		}
	)
urlldict.append(
		{
			'url': "https://www.bringfido.com/lodging/campgrounds/region/united_states/",
			'type': "Campgrounds",
			'namefile': "Campgrounds"
		}
	)
# url = "https://www.bringfido.com/lodging/hotels/region/united_states/" #Hotels
# url = "https://www.bringfido.com/lodging/rentals/region/united_states/"  #Vacation Rentals
# url = "https://www.bringfido.com/lodging/bandbs/region/united_states/"   #Bed & Breakfasts
# url = "https://www.bringfido.com/lodging/campgrounds/region/united_states/"   # Campgrounds

# 1 webdriver
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# web = webdriver.Chrome(ChromeDriverManager().install(), options=option)
web = webdriver.Chrome(ChromeDriverManager().install())  # браузер не стартував, допомогло встановлення
# web = webdriver.Chrome('/path/to/chromedriver')
web.implicitly_wait(1.5)

# 2 url to search
# import re
from bs4 import BeautifulSoup
import json

# all Html
for url_item in urlldict:
	hhh = web.get(url_item['url'])
	time.sleep(5)
	# find_button ='//*[@id="71_AMP_content_0"]/li[2]/a/div'
	# web.find_element(By.XPATH, find_button).click()

	find_button = '//*[@id="body"]/div[4]/div[2]/div[1]/div[1]/main/div/div[1]/div[3]/a'
	# '//*[@id="resultsList"]/amp-list-load-more[1]/button'
	web.find_element(By.XPATH, find_button).click()
	time.sleep(random.randint(2, 5))

	gear_xp = '//*[@id="resultsList"]/amp-list-load-more[1]/button'
	start_time = time.time()
	k = 1
	while k < 2:
		try:
			WebDriverWait(web, 50).until(EC.element_to_be_clickable((By.XPATH, gear_xp)))
			web.find_element(By.XPATH, gear_xp).click()
			print(f"True. k={k}")
		except:
			print(f"False. k={k}")
			k = 27
			pass
		k += 1

	finish_time = time.time() - start_time
	print(f'GEAR: {finish_time}')
	source_html = web.page_source
	# запис в ХТМЛ-файл
	with open(f"index{url_item['namefile']}.html", 'w', encoding='utf-8') as file:
		file.write(source_html)

web.close()
web.quit()

for url_item in urlldict:
	# 4 відкриття ХТМЛ файлу
	result = []
	HTMLFile = open(f"index{url_item['namefile']}.html", "r", encoding='utf-8')
	# Reading the file
	index = HTMLFile.read()
	soup = BeautifulSoup(index, 'lxml')

	# 5 пошук потрібних значень
	# soup = BeautifulSoup(index, 'lxml')

	url_next = soup.find_all('div', class_='resultsList__body resultsList__body--containedTiles')
		# print(url_next)
	# rep = 0
	for item_list in url_next:
		# rep += 1
		# print(rep)
		items = item_list.find_all('div', class_='propertyTile')
		# print(items)
		for item in items:
			item_text = item.find('a', class_='propertyTile__name__a').find('span').text.strip()
			if item_text == "":
				print('Pusto')
				continue
			# else:
			# 	print(item_text)
			find_url = item.find('a', class_='propertyTile__name__a').get('href')
			# print(find_url)
			if str(find_url).startswith('http'):
				item_url = find_url
			else:
				item_url = f"https://www.bringfido.com{find_url}"
			# item_url = item.find('a',class_='propertyTile__priceLink')#.get('href')
			# print(item_url)
			# print(f"name: {item_text} url: https://www.bringfido.com{item_url}")
			item_policy = item.find_all('div', class_='propertyTile__policy')
			# print(item1.text.strip())
			if item_policy:
				policy1 = item_policy[0].text.strip()
				policy2 = item_policy[1].text.strip()
				policy3 = item_policy[2].text.strip()
			else:
				policy1 = 'None'
				policy2 = 'None'
				policy3 = 'None'
				# print(item_text)
			item_location = item.find('div', class_='propertyTile__locationRow').find('a',
																			class_='propertyTile__location').text.strip()
			location = str(item_location).split(',')
			# item_id = re.search('\d{4,7}',item.find(class_='propertyTile__overlay').get('id'))
			result.append(
				{
					'type': url_item['type'],
					'name': item_text,
					'url': item_url,
					'policy1': policy1,
					'policy2': policy2,
					'policy3': policy3,
					'city': location[0],
					'state': location[1]
				}
			)
#
# 	# find_button = '//*[@id="body"]/div[4]/div[2]/div[1]/div[1]/main/div/div[1]/div[3]/a'
# 	# # '//*[@id="resultsList"]/amp-list-load-more[1]/button'
# 	# web.find_element(By.XPATH, find_button).click()
# 	# time.sleep(random.randint(2, 5))

	# 6 запис у файл JSON
	with open(f"D:\Path\{url_item['namefile']}.json", 'w', encoding='utf-8') as file:
		json.dump(result, file, indent=4, ensure_ascii=False)

# 6 Запис в ексель
import xlsxwriter
import os

# workbook = xlsxwriter.Workbook(f"NBU{dt.date.today().strftime('%d%m%Y')}.xlsx")
workbook = xlsxwriter.Workbook("D:\Path\Results.xlsx")

bold = workbook.add_format({'bold': True, 'font_color': 'red'})
bold.set_align('center')

bold_1 = workbook.add_format({'bold': True, 'font_color': 'black'})
bold_1.set_align('center')
bold_1.set_border(1)

bold_2 = workbook.add_format({'bold': True, 'font_color': 'blue'})
bold_2.set_align('center')
bold_2.set_border(1)

bold_3 = workbook.add_format({'bold': True, 'font_color': 'black'})
# bold_3.set_bg_color('#b4b4b4')
bold_3.set_align('center')
bold_3.set_border(2)

dirPath = r"D:\Path"
extensions = (".json")

for root, dirs, files in os.walk(dirPath):
	for filename in files:
		if os.path.isfile(os.path.join(dirPath, filename)):
			if filename.endswith(extensions):
				file_name = os.path.join(dirPath, filename)
				worksheet = workbook.add_worksheet(name=f"{str(filename).split('.')[0]}")
				# Format the column
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 15)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 35)
				worksheet.set_column('G:G', 20)
				worksheet.set_column('H:H', 10)
				worksheet.set_default_row(25)

				worksheet.write('A1', 'Type', bold_3)
				worksheet.write('B1', 'Bring Fido Source Link', bold_3)
				worksheet.write('C1', 'Policy 1', bold_3)
				worksheet.write('D1', 'Policy 2', bold_3)
				worksheet.write('E1', 'Policy 3', bold_3)
				worksheet.write('F1', 'Property Name', bold_3)
				worksheet.write('G1', 'City', bold_3)
				worksheet.write('H1', 'State', bold_3)
				file_json = open(file_name, 'r')
				row = 2
				data = json.load(file_json)

				for i in data:
					# add new row
					worksheet.write(f'A{row}', i['type'])
					worksheet.write(f'B{row}', i['url'])
					worksheet.write(f'C{row}', i['policy1'])
					worksheet.write(f'D{row}', i['policy2'])
					worksheet.write(f'E{row}', i['policy3'])
					worksheet.write(f'F{row}', i['name'])
					worksheet.write(f'G{row}', i['city'])
					worksheet.write(f'H{row}', i['state'])
# 					worksheet.write(f'B{row}', valute, bold_1)
# 					worksheet.write(f'C{row}', rate, bold_1)
					row += 1
time.sleep(4)
workbook.close()
print(f"Записано файл: {workbook.filename}")
