import json

from selenium import webdriver
from selenium.webdriver import ActionChains
from urllib.request import Request
import pandas as pd
import time
import os
import urllib.request
from selenium.common.exceptions import NoSuchElementException
import sys

from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# absolute path to chromedriver
CHROMEDRIVER_PATH = ''
TRASHOUT_LOGIN = ''
TRASHOUT_PASSWORD = ''
driver = webdriver.Chrome(CHROMEDRIVER_PATH)
print(driver)


def login(driver):
    driver.get("https://admin.trashout.ngo/trash-management/list/")
    time.sleep(3)
    driver.find_element_by_name("email").send_keys(TRASHOUT_LOGIN)
    driver.find_element_by_name("password").send_keys(TRASHOUT_PASSWORD)
    driver.find_elements_by_tag_name("button")[0].click()
    time.sleep(3)
    return driver


def next_page(driver):
    driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[3]/div/div[2]/div/ul/li[4]/a').click()
    return driver


def close_cookie(driver):
    script = 'document.getElementById("app").childNodes[0].childNodes[0].childNodes[2].style.visibility="hidden"'
    driver.execute_script(script)
    return driver


def iterate_rows(driver, page):
    page_images = dict()
    for d in driver.find_elements_by_tag_name("tr")[1:]:
        detail_link = d.find_elements_by_tag_name("td")[-1].find_element_by_tag_name("a")
        z = open_in_new_tab_process_close(driver, detail_link)
        if z != None:
            img_url, size, types_list = z
            page_images[img_url] = dict()
            page_images[img_url]['trash_size'] = size
            page_images[img_url]['types'] = types_list

    p_keys = page_images.keys()
    img_names = download_images_from_urls(p_keys, page)
    for k, name in zip(p_keys, img_names):
        page_images[k]['img_name'] = name
    print(page_images)

    return page_images


def open_in_new_tab_process_close(driver, detail_link):
    try:
        driver.execute_script("window.open('{}');".format(detail_link.get_attribute("href")))
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(5)
        first_img_url = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div').find_element_by_tag_name(
            'img').get_attribute('src')
        size = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div/div/span/span').text
        # types_container = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div/div')
        # type_elements = types_container.find_elements_by_tag_name('span')
        # print(len(type_elements))
        # for e in type_elements:
        #     print(e.text)
        # types_list = [t.find_element_by_tag_name('span').text for t in type_elements]
        time.sleep(2.5)
        type = None
        try:
            type = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[3]/div/div/div').text
        except NoSuchElementException  as e:
            print(e)
            type = driver.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div[4]/div/div/div').text
        status = get_status(driver)
        if status == 'cleaned':
            type_list = ['CLEANED']
            size = 'CLEANED'
        else:
            type_list = str(type).split('\n')

        driver = close_blank_tab(driver)
        return first_img_url, size, type_list
    except:
        driver = close_blank_tab(driver)
        return None


def download_images_from_urls(urls, page):
    img_names = []
    folder_name = "downloads"
    try:
        os.mkdir(folder_name)
    except:
        "folder exists"
    for i, url in enumerate(urls):
        img_name = download_image_from_url(url, folder_name, i, page)
        img_names.append(img_name)

    return img_names


def download_image_from_url(url, folder_name, order, page):
    try:
        img_name = os.path.join("img_" + str(page) + '_' + str(order) + ".jpg")
        urllib.request.urlretrieve(url, folder_name + '/' + img_name)
        print("can")
        return img_name
    except:
        print("cant")


def close_blank_tab(driver):
    z = driver
    z.switch_to.window(driver.window_handles[1])
    z.close()
    driver.switch_to.window(driver.window_handles[0])
    return driver


def page_images_to_csv(page_images):
    return pd.DataFrame.from_dict(page_images, orient='index')


def get_status(driver):
    status_text = driver.find_element_by_xpath(
        '//*[@id="app"]/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/span').text
    if status_text == 'Cleaned':
        return 'cleaned'
    else:
        return 'reported'


if __name__ == '__main__':
    driver = close_blank_tab(driver)
    driver = login(driver)
    close_cookie(driver)
    large_csv = pd.DataFrame(columns=['trash_size', 'types', 'img_name'])
    for page in range(0, 150):
        time.sleep(1)
        if page >= 100:
            page_images = iterate_rows(driver, page)
            large_csv = large_csv.append(page_images_to_csv(page_images))
        driver = next_page(driver)
        time.sleep(1)
    large_csv.to_csv('dataset100_150.csv', index=False)
    # driver.quit()
