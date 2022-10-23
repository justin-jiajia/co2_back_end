# YourRecording
### 介绍
一个记录应用,可以记录每天排放的二氧化碳。这是由ApiFlask编写的后端，由Vue编写的前端：[github](https://github.com/justin-jiajia/your-recording-front-end)

### 安装教程
#### 1.安装依赖
```shell
pip install -r requirements.txt
```
#### 2.写.env文件
```shell
vim .env

# secret随机字符，请将“strong string"替换为随机字符
SECRET_KEY=strong string 
# 数据库地址，默认在当前目录生成Sqlite数据库
# MySql: mysql://username:password@host/databasename
# Sqlite: sqlite:////home/ubuntu/co2.db
DATABASE_URL = sqlite:////home/ubuntu/co2.db
```
#### 3.初始化数据库
```shell
python -m flask initdb
```
#### 4.启动！
##### 通过Gunicorn（仅支持Linux）
```shell
gunicorn -b 0.0.0.0:8011 -w 4 wsgi:app
```
##### 通过内置开发服务器（仅开发！！）
```shell
flask run
```
