# 1 webdriver
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
# urlldict.append(
# 		{
# 			'url': "https://www.bringfido.com/lodging/rentals/region/united_states/",
# 			'type': "Vacation Rentals",
# 			'namefile': "Rentals"
# 		}
# 	)
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
# option = webdriver.ChromeOptions()
# option.add_argument('headless')
# web = webdriver.Chrome(ChromeDriverManager().install(), options=option)
web = webdriver.Chrome(ChromeDriverManager().install())  # браузер не стартував, допомогло встановлення
# web = webdriver.Chrome('/path/to/chromedriver')
web.implicitly_wait(1.5)

# 2 url to search
import re
from bs4 import BeautifulSoup
import json

for url_item in urlldict:
	# 3 all Html
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
	while k < 6000:
		try:
			WebDriverWait(web, 10).until(EC.element_to_be_clickable((By.XPATH, gear_xp)))
			web.find_element(By.XPATH, gear_xp).click()
		#	print(f"True. k={k}")
		except:
		#	print(f"False. k={k}")
			k = 6000
			pass
		k += 1

	finish_time = time.time() - start_time
	print(f'GEAR: {finish_time}')
	source_html = web.page_source
	# запис в ХТМЛ-файл
	with open(f"index{url_item['namefile']}.html", 'w', encoding='utf-8') as file:
		file.write(source_html)

	# 4 find links
	result = []
	HTMLFile = open(f"index{url_item['namefile']}.html", "r", encoding='utf-8')
	# Reading the file
	index = HTMLFile.read()
	soup = BeautifulSoup(index, 'lxml')

	# 5 find next page

	soup = BeautifulSoup(index, 'lxml')

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
			item_url = f"https://www.bringfido.com{item.find('a', class_='propertyTile__name__a').get('href')}"
			# print(f"name: {item_text} url: https://www.bringfido.com{item_url}")
			item_policy = item.find_all('div', class_='propertyTile__policy')
			# print(item1.text.strip())
			policy1 = item_policy[0].text.strip()
			policy2 = item_policy[1].text.strip()
			policy3 = item_policy[2].text.strip()
			item_location = item.find('div', class_='propertyTile__locationRow').find('a',
																			class_='propertyTile__location').text.strip()
			location = str(item_location).split(',')
			if item_text == "":
				print('Pusto')
				continue
			# else:
			# 	print(item_text)
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

	# find_button = '//*[@id="body"]/div[4]/div[2]/div[1]/div[1]/main/div/div[1]/div[3]/a'
	# # '//*[@id="resultsList"]/amp-list-load-more[1]/button'
	# web.find_element(By.XPATH, find_button).click()
	# time.sleep(random.randint(2, 5))

	# '//*[@id="resultsList"]/div[3]/div/div[1]'
	# '//*[@id="resultsList"]/div[3]/div[2]/div[1]'
	# '//*[@id="resultsList"]/div[3]/div[3]/div[1]'
	# find_xp = '//*[@id="resultsList"]/div[3]/div/div[1]'
	# scrape_nextpage(soup)
	# k = 1
	# while k < 3:
	# 	try:
	# 		find_xp = '//*[@id="resultsList"]/amp-list-load-more[1]/button'
	# 		scrape_nextpage(find_xp)
	# 		k += 1
	# 	except:
	# 		print('Zaversheno')
	# 		k = 5

	with open(f"{url_item['namefile']}.json", 'w') as file:
		json.dump(result, file, indent=4, ensure_ascii=False)

web.close()
web.quit()
