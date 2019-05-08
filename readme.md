# Agoda_Crawler

* Python 3.7.3
* Mysql 8.0.15

## Installations

#### pyhton library
```
$ sudo pip install pymysql
$ sudo pip install selenium
$ sudo pip install python-dotenv
$ sudo pip install pandas
```
#### chromedriver
```
for MAC using homebrew
$ brew cask install chromedriver
```

## Config Setting
#### mysql
```
MYSQL_HOST - mysql host, e.g. 127.0.0.1
MYSQL_USERNAME - user name, e.g. root
MYSQL_PASSWORD - password 
MYSQL_DATABASE - choose the database you want to connect, e.g. crawler_db
```
#### smtp
```
SMTP_HOST - smtp host, e.g. smtp.gmail.com
SMTP_USERNAME - smtp login username e.g. user@gmail.com
SMTP_PASSWORD - smtp login password
SUBJECT - Agoda Crawler Daily Report
EMAIL_FROM - user@gmail.com
EMAIL_TO - recipient (multiple: use comma to split email, e.g. a@test.com,b@test.com)
```
#### crawler
```
CHROME_DRIVER - /usr/local/bin/chromedriver
```
