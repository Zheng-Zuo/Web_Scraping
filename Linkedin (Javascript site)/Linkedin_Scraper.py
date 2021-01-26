from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import csv


writer = csv.writer(open('output.csv','w'))
writer.writerow(['name','headline','education_background'])
driver = webdriver.Chrome(executable_path='D:/scrapy_projects/chromedriver.exe')

driver.get("https://www.linkedin.com/")
sleep(3)

driver.find_element_by_xpath("//a[@class='nav__button-secondary']").click()
sleep(3)

#use your real username, otherwise it won't work
username = driver.find_element_by_name("session_key")
username.send_keys('demo')
sleep(1)

#use your real username, otherwise it won't work
password = driver.find_element_by_name("session_password")
password.send_keys('demo')
sleep(1)

driver.find_element_by_xpath("//*[@type='submit']").click()
sleep(3)

driver.get("https://www.google.com/")
sleep(3)

input_box = driver.find_element_by_xpath("//*[@class='gLFyf gsfi']")
input_box.send_keys('site:linkedin.com/in/ AND "python developer" AND "New York"')
sleep(1)

input_box.send_keys(Keys.ENTER)
sleep(3)

profiles = driver.find_elements_by_xpath("//a[starts-with(@href, 'https://www.linkedin.com')]")
profiles = [profile.get_attribute('href') for profile in profiles]

for profile in profiles:
    driver.get(profile)
    sleep(3)

    sel = Selector(text=driver.page_source)

    name = sel.xpath("//li[@class='inline t-24 t-black t-normal break-words']/text()").get()
    headline = sel.xpath("//h2[@class='mt1 t-18 t-black t-normal break-words']/text()")[0].get()
    education_background = sel.xpath("//*[@class='pv-entity__degree-info']/h3/text()").getall()

    writer.writerow([name,headline,education_background])


driver.quit()