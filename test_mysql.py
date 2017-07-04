#!/usr/bin/env python
#-*- coding: UTF-8 -*-
 
'''
#Module name:testmysql.py
#Created by Leo Wen  
'''
import os
import sys
import MySQLdb as mdb
import traceback

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_pw = 'lj'
db_name = 'mysql'

now_dir = os.getcwd()
#print now_dir

'''
查询版本
'''
def test1():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
 
		#所有的查询，都在连接 con 的一个模块 cursor 上面运行的
		cur = con.cursor()
 
		#执行一个查询
		cur.execute("SELECT VERSION()")
		#取得上个查询的结果，是单个结果
 
		data = cur.fetchone()
		print "Database version : %s " % data
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			#无论如何，连接记得关闭
			con.close()
'''
创建一个表
'''
def test2():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		#创建一个数据表 writers(id,name)
		
		cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, Name VARCHAR(25))")
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			con.commit()
			#无论如何，连接记得关闭
			con.close()

'''
插入数据
connect,cursor,insert,commit,close
如插入数据时没有写id,将自动累加id
'''
def test3():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()

		#以下插入了 5 条数据
		cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
		cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
		cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
		cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
		cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			con.commit()
			#无论如何，连接记得关闭
			con.close()
'''
查询数据
connect,cursor,select,close
'''
def test4():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		cur.execute("SELECT * FROM Writers")
		'''
		#获取rowcount
		rowcount = int(cur.rowcount)
		for i in range(rowcount):
			row = cur.fetchone()
			if row:
				print row[0],':',row[1]
		#print cur.fetchall()
		for row in cur.fetchall():
			print row
		'''	
		#获取连接对象的描述信息,description
		desc = cur.description
		print 'cur.description:',desc
		#打印表头，就是字段名字
		print "%s %s" % (desc[0][0], desc[1][0])


	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			#无论如何，连接记得关闭
			con.close()

'''
查询数据
使用字典 cursors 取得结果集（可以使用表字段名字访问值）
connect,cursor,select,close
'''
def test5():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		#获取连接上的字典 cursor，注意获取的方法，
		#每一个 cursor 其实都是 cursor 的子类
		cur = con.cursor(mdb.cursors.DictCursor)
		cur.execute("SELECT * FROM Writers")
		for row in cur.fetchall():
			print row['Id'],':',row['Name']
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			#无论如何，连接记得关闭
			con.close()

'''
数据更新
connect,cursor,update,commit,close
'''
def test6():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		#update对已经存在的进行修改
		cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",("Guy de Maupasant", "8"))
		#使用 cur.rowcount 获取影响了多少行
		print "Number of rows updated: %d" % cur.rowcount
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			#无论如何，连接记得关闭
			con.commit()
			con.close()

'''
把图片用二进制存入 MYSQL
'''
def test7():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		#创建一个数据表 writers(id,name)
		
		cur.execute("CREATE TABLE Images(Id INT PRIMARY KEY AUTO_INCREMENT, Data MEDIUMBLOB)")
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			con.commit()
			#无论如何，连接记得关闭
			con.close()

'''
把图片用二进制存入 MYSQL
'''
def test8():
	try:
		fd = open('./web.png')
		img = fd.read()
	except Exception,e:
		traceback.print_exc()
	finally:
		if fd:
			fd.close()

	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		cur.execute("INSERT INTO Images SET Data='%s'" % mdb.escape_string(img))
		cur.close()
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			con.commit()
			#无论如何，连接记得关闭
			con.close()
#读图片
def test9():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		cur.execute("SELECT Data FROM Images LIMIT 1")
		fout = open('image.png','wb')
		#直接将数据如文件
		#print cur.fetchone()
		fout.write(cur.fetchone()[0])
		fout.close()
	except Exception,e:
		traceback.print_exc()
	finally:
		if con:
			#无论如何，连接记得关闭
			con.close()


'''
数据更新,自动回滚
connect,cursor,update,commit,close
'''
def test10():
	con = None
	try:
		#连接 mysql 的方法： connect('ip','user','password','dbname')
		con = mdb.connect(mysql_ip, mysql_user,mysql_pw, db_name);
		cur = con.cursor()
		#update对已经存在的进行修改
		cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",("Guy de Maupasant", "8"))
		cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",("Leo Tolstoy", "9"))
		cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",("Boris Pasternak", "10"))
		cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s",("Leonid Leonov", "11"))
		#使用 cur.rowcount 获取影响了多少行
		print "Number of rows updated: %d" % cur.rowcount
	except Exception,e:
		traceback.print_exc()
		con.rollback()		#如果出现错误，回滚
	finally:
		if con:
			#无论如何，连接记得关闭
			con.commit()
			con.close()
if __name__ == "__main__":
	#test1()
	#test2()	
	#test3()
	test10()
	test5()










