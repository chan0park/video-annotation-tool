#!/usr/bin/env python
from selenium import webdriver
import urllib.request
import os.path

if not os.path.isdir('./videos/'):
    os.mkdir('./videos')
driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver')
driver.get("https://helpx.adobe.com/creative-cloud/tutorials-explore.html")

tutorials = driver.find_elements_by_class_name("learn-card")
url_list = [x.get_attribute("href") for x in tutorials]
url_list = url_list[1:10]
step_text = []
for idx, url in enumerate(url_list):
    driver.get(url)
    step_text.extend([x.text for x in driver.find_elements_by_class_name("stepNumber")])
    video_url = [x.get_attribute("src") for x in driver.find_elements_by_class_name("video-iframe")]
    for vidx, vurl in enumerate(video_url):
        driver.get(vurl)
        driver.find_elements_by_class_name("play-large-holder")[0].click()
        urllib.request.urlretrieve(driver.find_elements_by_css_selector("video")[0].get_attribute("src"), './videos/video_{}_{}.mp4'.format(idx, vidx))

with open('./step-text.txt','w') as file:
    file.write(str(step_text))
