from selenium import webdriver
import xlrd
from xlutils.copy import copy
from selenium.webdriver.common.by import By
import os
import urllib.request

class TravelCrawler():

    def download(self):
        url = "http://www.statvision.com/webinars/countries%20of%20the%20world.xls"
        urllib.request.urlretrieve(url, "countries.xls")
    
    def test(self):

        driverLocation = "/Users/withgod/Documents/lib/chromedriver"
        os.environ["webdriver.chrome.driver"] = driverLocation
        baseUrl = "https://google.com"
        driver = webdriver.Chrome(driverLocation)
        driver.maximize_window()
        driver.get(baseUrl)

        isVideo = True
        print(" This is the number of travel vedio per country in google")
        for i in range(6,10):

            data = xlrd.open_workbook('countries.xls')
            sheet = data.sheet_by_index(0)
            copy_data = copy(data)

            country = sheet.cell(i, 0).value.strip()
            keyword = country + " travel"

            elem = driver.find_element_by_id('lst-ib')
            elem.clear()
            elem.send_keys(keyword)
            elem.submit()

            if isVideo:
                video_elem = driver.find_element(By.XPATH,"(//a[@class='q qs'])[2]")
                video_elem.click()
                isVideo = False

            elem = driver.find_element_by_id("resultStats")
            result = elem.text
            number = result.split(" ")[2]
            print(country,":", number)
        driver.quit()


tt = TravelCrawler()
tt.download()
tt.test()
