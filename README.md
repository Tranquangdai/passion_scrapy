## How to run
* build images **db** and **crawler**
```
docker build ./ -t beauty_scrapy
docker run -d --name db -e MYSQL_ROOT_PASSWORD=password mysql/mysql-server
docker run -d --name crawler --link db beauty_scrapy
```
* find db container host docker `inspect db | grep IPAddress`
* create database for storing crawling data
```
docker exec -ti db bash
mysql -uroot -ppassword
CREATE USER 'tranquangdai'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'tranquangdai'@'%';
ALTER USER 'tranquangdai' IDENTIFIED WITH mysql_native_password BY 'password';
CREATE DATABASE test;
USE test;
quit
```

* run crawler `docker run -ti crawler /bin/bash`
* change **settings.py** DB_HOST to db container host: `inspect db | grep IPAddress`
* create database in db container: `python -m models.passion_mysql`
* crawl data: `python -m main --type category && python -m main --type link_page && python -m main --type link_product`

## TO DO:
* add dockercompose
* add makefile
