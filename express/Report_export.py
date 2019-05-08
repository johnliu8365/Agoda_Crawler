#!/usr/bin/env python
# coding: utf-8

import pymysql
import pandas as pd
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

def get_report(dir_path):
    host = os.getenv('MYSQL_HOST')
    username = os.getenv('MYSQL_USERNAME')
    password = os.getenv('MYSQL_PASSWORD')
    database = os.getenv('MYSQL_DATABASE')
    db = pymysql.connect(host, username, password, database, charset='utf8')

    try:
        sql = "SELECT * FROM Price P JOIN Room R ON P.room_id = R.id WHERE DATE(P.created_at) = CURDATE()"
        data = pd.read_sql(sql, db)
        data.drop(columns=['id', 'created_at', "room_id"], inplace=True)
        data.columns = [ '每晚價格(NTD)', '人數限制', '優惠內容&取消規定', '房數','客房', '房型摘要']
        data.set_index(keys = ['客房', '房型摘要', '每晚價格(NTD)'], inplace=True)
        file_name = os.path.join(dir_path, 'report/') + (datetime.datetime.today()).strftime('%Y%m%d') + '_Agoda_Crawler.xlsx'
        data.to_excel(file_name)
        return file_name
    except Exception as e:
        print(e)

def send_email(file_name):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = os.getenv('SUBJECT')
        msg['From'] = os.getenv('EMAIL_TO')
        msg['To'] = os.getenv('EMAIL_FROM')

        text = MIMEText("今天 東京灣喜來登大飯店 的房價報告")
        msg.attach(text)

        xlsx = MIMEApplication(open(file_name,'rb').read())
        xlsx.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
        msg.attach(xlsx)

        server = smtplib.SMTP(os.getenv('SMTP_HOST'))
        server.ehlo()
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


def main():
    dir_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    env_path = os.path.join(dir_path, '.env')
    load_dotenv(dotenv_path=env_path)
    file_name = get_report(dir_path)
    send_email(file_name)

if __name__ == '__main__':
	main()