from selenium import webdriver
from selenium.webdriver.support.select import Select #for dropdowns
import re
import time
import csv

def car_brand_scrape(driver):

	#left dropdown with car brands select object
	drop_down = Select(driver.find_element_by_xpath('//select[@class="form-control search-make"]'))
	# car_makers = [brand.text for brand in drop_down.options][1:34]

	for i in range(2): #33 car brands we want to scrape
		#go to each car brand
		drop_down.select_by_index(i+32)
		driver.find_element_by_xpath('//button[@id="make-model-form-submit"]').click()
		time.sleep(2)

		scrape_listings_for_one_brand(driver,drop_down)

def scrape_listings_for_one_brand(driver,drop_down):
	page_num=1
	while True:
		reviews = driver.find_elements_by_xpath('//article[@class="srp-list-item "]') #finding all the listing on page
		print("{} page : {} with {} reviews".format(drop_down.first_selected_option.text,page_num,len(reviews)))
		print(driver.find_element_by_xpath('//span[@class="srp-list-total"]/small').text) #which reviews are displayed
		page_num += 1
		for review in reviews:
			review_dict={}
			try:
				model_year = review.find_element_by_xpath('.//span[@class="srp-list-item-basic-info-model"]').text
				price = re.findall(': \$\S+',review.find_element_by_xpath('.//span[@class="srp-list-item-price"]').text)[0][3:]
				dealership = review.find_element_by_xpath('.//a[@class="srp-list-item-dealership-name"]').text

				pillar_4 = review.find_elements_by_xpath('.//ul[@class="srp-list-item-pillars-list"]//li') #list of 4 items below
				damage = pillar_4[0].find_element_by_xpath('./span').text
				damage_det = pillar_4[0].find_element_by_xpath('./p').text
				owners = pillar_4[1].find_element_by_xpath('./span').text
				owners_det = pillar_4[1].find_element_by_xpath('./p').text
				usage = pillar_4[2].find_element_by_xpath('./span').text
				usage_det = pillar_4[2].find_element_by_xpath('./p').text
				service = pillar_4[3].find_element_by_xpath('./span').text
				service_det = pillar_4[3].find_element_by_xpath('./p').text

				basic_info_lst = review.find_elements_by_xpath('.//div[@class="srp-list-item-basic-info srp-list-item-special-features"]/span')
				mileage = re.sub(',','',re.findall('\d*,\d+',basic_info_lst[0].text)[0]) #edge case of no comma <1000 mileage
				body_type = re.findall(':.?\w+',basic_info_lst[1].text)[0][2:]    
				color = re.findall(':.?\w+',basic_info_lst[2].text)[0][2:] 
				engine= re.findall(':.+',basic_info_lst[3].text)[0][2:]

				descr = review.find_element_by_xpath('.//div[@class="srp-list-item-options truncate-options-srp show"]/span[2]').text    

				review_dict['model_year'] = model_year
				review_dict['price'] = price
				review_dict['dealership'] = dealership

				review_dict['damage'] = damage
				review_dict['damage_det'] = damage_det
				review_dict['owners'] = owners
				review_dict['owners_det'] = owners_det
				review_dict['usage'] = usage
				review_dict['usage_det'] = usage_det
				review_dict['service'] = service
				review_dict['service_det'] = service_det

				review_dict['mileage'] = mileage
				review_dict['body_type'] = body_type
				review_dict['color'] = color
				review_dict['engine'] = engine

				review_dict['description'] = descr

				writer.writerow(review_dict.values())

			except:
				continue
		try:
			next_button = driver.find_element_by_xpath('//li[@class="next"]/a').click()
			time.sleep(1)
		except:
			break


#activating the scrape
#create empty csv file in same folder to store data
csv_file=open('car_listings.csv','w',encoding='utf-8', newline='')
writer = csv.writer(csv_file)
csv_headers = ['model_year','price','dealership','damage','damage_det','owners','owners_det','usage','usage_det','service','service_det',
				'mileage','body_type','color','engine','description']
writer.writerow(csv_headers)
#diff driver setups for diff computer
#these three lines below are for home desktop
options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', False)
driver = webdriver.Chrome(r"C:\Users\Jimmy Jing\Documents\Selenium\chromedriver.exe", options=options) 

#laptop
# driver = webdriver.Chrome(r"C:\Users\Jimmy Jing\chromedriver.exe") 

#go to starting website and input zip code to search, only needed in scrape (not in manual human use case)
driver.get('https://www.carfax.com/Used-Acura_m1')
driver.find_element_by_xpath('//*[@id="react-app"]//input[@class="zipListingForm__zipInput zip "]').send_keys('07661')
driver.find_element_by_xpath('//button[@class="button searchForm-submit-btn search_button"]').click()
time.sleep(1)

car_brand_scrape(driver)

driver.close()