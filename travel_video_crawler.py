from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
import xlrd
from xlutils.copy import copy
import urllib.request

class TravelVideoCrawler():

    def download(self):
        url = "http://www.statvision.com/webinars/countries%20of%20the%20world.xls"
        urllib.request.urlretrieve(url, "countries.xls")

    def test(self):
        driverLocation = "/Users/withgod/Documents/lib/chromedriver"
        os.environ["webdriver.chrome.driver"] = driverLocation
        driver = webdriver.Chrome(driverLocation)
        driver.maximize_window()
        if not os.path.isfile("countries.xls"):
            self.download()
            print("download finished")
        baseUrl = "https://google.com"
        driver.get(baseUrl)
        isVideoTab = False
        data = xlrd.open_workbook('countries.xls')
        print("Start")
        for i in range(5, 232):
            sheet = data.sheet_by_index(0)
            copy_data = copy(data)
            country = sheet.cell(i, 0).value.strip()
            region = sheet.cell(i, 1).value.strip()
            keyword = country + " travel"
            elem = driver.find_element_by_id('lst-ib')
            elem.clear()
            elem.send_keys(keyword)
            elem.submit()
            if not isVideoTab:
                video_elem = driver.find_element(By.XPATH,"(//a[@class='q qs'])[2]")
                video_elem.click()
                isVideoTab = True
            item = {}
            country = country
            item['country'] = country
            item['region'] = region
            findVideo = False
            for i in range(1,6):
                if findVideo:
                    continue
                video_url = driver.find_elements_by_class_name("iUh30")[i].text.split(" ")[0]
                if not "youtube" in video_url:
                    print("not youtube")
                    continue
                item['video_url'] = video_url
                img_url = driver.find_element_by_id("vidthumb"+str(i)).get_attribute("src")
                item['img_url'] = img_url
                title = driver.find_element(By.XPATH, "(//div[@id='rso']//div["+str(i)+"]/div//h3/a)").text
                item['title'] = title.replace(",","")
                findVideo = True
                yield item
            yield None
        yield None
        driver.close()

cc = TravelVideoCrawler()
with open('youtube.csv','w') as f:
    writer = csv.writer(f, delimiter=',',lineterminator='\n',)
    for x in cc.test():
        if x is not None:
            row = [ x['country'],x['region'], x['title'], x['img_url'], x['video_url']]
            print(row)
            writer.writerow(row)
