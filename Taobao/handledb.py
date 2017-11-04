# -*- coding: utf-8 -*-
import MySQLdb


class MysqldbHelper:

    def __init__(self):
        try:
            con = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='python', port=3306, charset='utf8')
            self.conn = con
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
                # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典

    def select(self, sql):
        try:
            # con = self.getCon()
            # print con
            cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error, e:
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            
            # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')

    def updateByParam(self, sql, params):
        try:
            cur = self.conn.cursor()
            count = cur.execute(sql, params)
            self.conn.commit()
            return count
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
           

    def update(self, sql):
        try:
            cur = self.conn.cursor()
            count = cur.execute(sql)
            self.conn.commit()
            return count
        except MySQLdb.Error, e:
            self.conn.rollback()
            print "Mysqldb Error:%s" % e
        finally:
            cur.close()
            

    def close(self):
        self.conn.close()


