# -*- coding:utf-8 -*-

import pymysql

class operate_db(object):

	def __init__(self,user,password,db_name,host="localhost"):
		self.host = host
		self.user = user
		self.password = password
		self.db_name = db_name

	def read(self,sql):
		# 打开数据库连接
		db = pymysql.connect(self.host, self.user, self.password, self.db_name, charset='utf8' )

		# 使用cursor()方法获取操作游标
		cursor = db.cursor()

		# SQL 查询语句
		sql = sql
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				fname = row[0]
				lname = row[1]
				age = row[2]
				sex = row[3]
				income = row[4]
				# 打印结果
				print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
				(fname, lname, age, sex, income))

		except:
			print("Error: unable to fecth data")


		# 关闭数据库连接
		db.close()

	def create(self,table_name):
		# 打开数据库连接
		db = pymysql.connect(self.host, self.user, self.password, self.db_name, charset='utf8')

		# 使用cursor()方法获取操作游标
		cursor = db.cursor()

		# 如果数据表已经存在使用 execute() 方法删除表。
		cursor.execute("DROP TABLE IF EXISTS "+table_name)

		# 创建数据表SQL语句
		sql = """CREATE TABLE """+table_name+""" (
		         FIRST_NAME  CHAR(20) NOT NULL,
		         LAST_NAME  CHAR(20),
		         AGE INT,  
		         SEX CHAR(1),
		         INCOME FLOAT )"""

		cursor.execute(sql)

		# 关闭数据库连接
		db.close()

	def write(self):
		pass