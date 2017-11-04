# -*- coding: utf-8 -*-
import MySQLdb


class MysqldbHelper:

    def getCon(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
            return conn
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
                # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典

    def insert(self,sql):
        try:
            con = self.getCon()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            con.commit()
        except Exception as e:
            print e
        finally:
            cur.close()
            con.close()

    def select(self, sql):
        try:
            con = self.getCon()
            print con
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()
            # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')

    def updateByParam(self, sql, params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()
            # 不带参数的更新方法

    def update(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except MySQLdb.Error, e:
            con.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            con.close()


