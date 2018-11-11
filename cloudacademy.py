# The standard library modules
import os
import sys
import re

# The wget module
import wget
from urllib.parse import urlparse
from os.path import splitext, basename

# The BeautifulSoup module
from bs4 import BeautifulSoup
import urllib.request


# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webbrowser.support.ui import WebbrowserWait
#from selenium.webbrowser.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromebrowser = 'C:\\Ramanujam\\PycharmProjects\\Project1\\chromedriver.exe'
browser = webdriver.Chrome(chromebrowser)
browser.get('https://cloudacademy.com/login/')

#browser.find_element_by_id("headerLoginButton").click()


username = browser.find_element_by_id("loginform_username")
password = browser.find_element_by_id("loginform_password")

username.send_keys("ramanujam.srinivasan@cognizant.com")
password.send_keys("xxxxxxx") # password to go in here

browser.find_element_by_id("loginSubmit").click()
course_url='https://cloudacademy.com/course/highly-available-systems-sysops'
parent_path="C:\\Ramanujam\\Cloudacademy\\"
browser.get(course_url)
#browser.get('https://cloudacademy.com/course/google-cloud-platform-fundamentals')
#browser.get('https://cloudacademy.com/course/automated-data-management-with-ebs-s3-and-glacier/getting-started-5/')

course_dir = parent_path+os.path.basename(course_url)


os.makedirs(course_dir, exist_ok=True)

#elems = browser.find_elements_by_partial_link_text('automated-data-management-with-ebs-s3-and-glacier')
elems = browser.find_elements_by_xpath("//a[contains(@href,'/course/highly-available-systems-sysops')]")
print('href', elems)



for elem in elems:
    index=0
    print('href',elem.get_attribute("href"))
#    browser.get(elem.get_attribute("href")
    vurl = elem.get_attribute("href");
    browser.execute_script("window.open('{}');".format(vurl))
#    sleep(1)  # you can also try without it, just playing safe
    browser.switch_to.window(browser.window_handles[-1])  # last opened tab handle

#    WebElement loginButton = browser.findElement(By.tagName("video"));
#    videos = browser.find_element_by_tag_name("video")
#    print(videos)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//video[contains(@id, 'vjs_video')]")))
    src = browser.page_source # gets the html source of the page

    parser = BeautifulSoup(src,"lxml") # initialize the parser and parse the source "src"
    #list_of_attributes = {"class" : "some-class", "name" : "some-name"} # A list of attributes that you want to check in a tag
    tag = parser.findAll('video') # Get the video tag from the source
    print(tag)
    n = 0 # Specify the index of video element in the web page
    url = tag[n]['src'] # get the src attribute of the video
    print(url)
    my_new_string = re.sub('[^ a-zA-Z0-9]', '', browser.title)
    #my_new_string = my_new_string.replace(' ', '')

    os.makedirs(course_dir+'\\'+my_new_string, exist_ok=True)

    disassembled = urlparse(url)
    #filename, file_ext = splitext(basename(disassembled.path))
    filename= os.path.basename(disassembled.path)
    #file_ext = file_ext.replace('\\', '')
    fullfilename = os.path.join(course_dir+'\\'+my_new_string,filename )
    #wget.download(url,out="C:\\Ramanujam\\Cloudacademy\\"+my_new_string) # download the video
    urllib.request.urlretrieve(url,fullfilename)
    browser.switch_to_window(browser.window_handles[0])


#browser.get('https://cloudacademy.com/course/')
browser.close() # closes the browser