import scrapy 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from alitrip.items import Route, Flight
import re 
import sys 

class AliSpider(scrapy.Spider):
	name = "ali"
	allowed_domains = ["alitrip.com"]
	start_urls = ['https://www.alitrip.com/']

	def __init__(self):
		self.driver = webdriver.Firefox()

	def parse(self, response):
		print("get selenium driver")
		driver = self.driver
		driver.get(response.url)
		

		driver.maximize_window()

		time.sleep(20)



		elem = driver.find_element_by_xpath("(//span[@class='sub-item-in'])[2]")
		elem.click()

		print("input form")
		driver.find_element_by_xpath("(//input[@name='depCityName'])[2]").send_keys("PEK")
		driver.find_element_by_xpath("(//input[@name='arrCityName'])[2]").send_keys("YVR")
		driver.find_element_by_xpath("(//input[@name='depDate'])[2]").send_keys("2016-06-13")
		driver.find_element_by_xpath("(//input[@name='arrDate'])[2]").send_keys("2016-06-25")
		driver.find_element_by_xpath("(//input[@name='arrDate'])[2]").send_keys(Keys.ENTER)

		for handle in driver.window_handles:
			driver.switch_to_window(handle)

		time.sleep(40)
		driver.maximize_window()

		#direct or not 
		#driver.find_element_by_xpath("//span[@class='pi-checkbox-icon']").click()

		time.sleep(5)
		allRoutes = driver.find_elements_by_css_selector("div[class='J_FlightItem item-root']")

		i = 0 
		for route in allRoutes:
			aRoute = Route() 
			airlines = route.find_elements_by_class_name("J_line")
			depatureTime = route.find_elements_by_class_name("b-time")
			arriveTime = route.find_elements_by_class_name("s-time")
			if len(airlines) > 1:
				aRoute["transfer"] = True
				aRoute["numOfTransfer"] = len(airlines)
				for x in range(len(airlines)):
					aFlight = Flight()
					aFlight["airLines"] = airlines[x].text
					aFlight["depatureTime"] = depatureTime[x].text
					aFlight["arriveTime"] = arriveTime[x].text
					if x == 0:	
						aRoute["flights"] = [dict(aFlight)]
					else:
						aRoute["flights"].append([dict(aFlight)])
			else:
				aRoute["transfer"] = False
				aFlight = Flight()
				aFlight["airLines"] = airlines[0].text
				aFlight["depatureTime"] = depatureTime[0].text
				aFlight["arriveTime"] = arriveTime[0].text
				aRoute["flights"] = [dict(aFlight)]

			price0 = driver.execute_script("return document.getElementsByClassName('total-price')[" + str(i) +"].innerHTML;")
			match = re.search("\d+", price0)
			aRoute["price"] = match.group(0)
			i+=1

			yield aRoute

		driver.quit()

		





