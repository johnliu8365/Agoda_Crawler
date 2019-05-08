#!/usr/bin/env python
# coding: utf-8

import time
import datetime
import pymysql
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv

dir_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
env_path = os.path.join(dir_path, '.env')
load_dotenv(dotenv_path=env_path)
host = os.getenv('MYSQL_HOST')
username = os.getenv('MYSQL_USERNAME')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')
db = pymysql.connect(host, username, password, database, charset='utf8')


def get_max_people(driver, room):
    block = room.find_element_by_class_name('ChildRoomsList-capacity')
    actions = ActionChains(driver)
    actions.move_to_element(block)
    actions.perform()
    word = driver.find_elements_by_class_name('CapacityTooltipBody-header')
    for w in word:
        if w.text[:2] == '最多':
            return w.text
        elif w.text[:2] == '此專':
            return '最多'+w.text[11:15]

def insert_room_data(room_name, room_info):
    cursor = db.cursor()
    sql = 'INSERT INTO Room(room_name, room_info) VALUES(%s,%s)'
    cursor.execute(sql,(room_name, room_info))
    db.commit()
    cursor.close()
    return cursor.lastrowid

def find_room_data():
    cursor = db.cursor()
    sql = 'SELECT id, room_name FROM Room'
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    
    rooms = {}
    for rows in data:
        rooms[rows[1]] = rows[0]
        
    return rooms

def insert_price_data(price):
    cursor = db.cursor()
    sql = 'INSERT INTO Price(room_id, price_ntd, price_people, price_info, price_left) VALUES(%s,%s,%s,%s,%s)'
    cursor.execute(sql,(price['room_id'], price['ntd'], price['people'], price['info'], price['left']))
    db.commit()
    cursor.close()

def get_room_data(driver):
    db_rooms = find_room_data()

    driver.implicitly_wait(10)
    masters = driver.find_elements_by_class_name('MasterRoom')

    for WebElement in masters:
        room_name = WebElement.find_element_by_class_name('MasterRoom-headerTitle--text').find_element_by_tag_name('span').text
        if room_name in db_rooms:
            room_id = db_rooms[room_name]
        else:
            roomInfos = WebElement.find_elements_by_class_name('MasterRoom-amenitiesTitle')
            room_info = ""
            for i in roomInfos[:-1]:
                room_info += str(i.text + '\n')
            room_id = insert_room_data(room_name, room_info)
        
        rooms = WebElement.find_elements_by_class_name('ChildRoomsList-room')
        for room in rooms:
            price = {'room_id': room_id, 'info': ''}
            features = room.find_elements_by_class_name('ChildRoomsList-roomFeature')
            for feature in features:
                price['info'] += str(feature.text + '\n')
            price['ntd'] = room.find_element_by_class_name('pd-price').text
            price['ntd'] = int(price['ntd'].replace(',',''))
            price_left = room.find_element_by_class_name('red-orange').text
            for s in price_left:
                if s.isdigit():
                    price['left'] = s
                    break
            price['people'] = get_max_people(driver, room)
            print(price)
            insert_price_data(price)

def main():
    # 開啟webdriver，並搜尋'東京灣喜來登大飯店'
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get('https://www.agoda.com/zh-tw/')
    driver.find_element_by_css_selector('.SearchBoxTextEditor').send_keys("東京灣喜來登大飯店")
    time.sleep(1)
    driver.find_element_by_css_selector('.SearchBoxTextEditor').send_keys(Keys.ENTER)

    # 點選 入住時間明天->退房時間後天->兩人入住->搜尋
    tomorrow = datetime.date.today() + datetime.timedelta(1)
    afterTomorrow = datetime.date.today() + datetime.timedelta(2)
    driver.find_element_by_class_name("DayPicker-NavButton--prev").click()
    driver.find_element_by_xpath("//div[@aria-label= '" + tomorrow.strftime("%a %b %d %Y") + "']").click()
    time.sleep(0.5)
    driver.find_element_by_xpath("//div[@aria-label= '" + afterTomorrow.strftime("%a %b %d %Y") + "']").click()
    driver.find_element_by_css_selector('.TravellerSegment--active > .TravellerSegment__title').click()
    driver.find_element_by_css_selector('.Searchbox__searchButton').click()

    get_room_data(driver)
    driver.quit()

if __name__ == '__main__':
	main()
