# -*- coding: utf-8 -*-
#!/usr/bin/python
# author:killvoon
import paramiko
import psutil
import time
import handledb
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from multiprocessing import TimeoutError

##定义主机列表
linux = ['192.168.159.146', '192.168.159.147']

class CPU():
	def connectHost(self,ip, uname='root', passwd='123456'):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip, username=uname, password=passwd)
		return ssh


	def MainCheck(self):
		# 查看linux文件系统使用率
		# 建立主机连接
		Mysqlhelper = handledb.MysqldbHelper()
		for a in range(len(linux)):
		    try:
		        ssh = self.connectHost(linux[a])
		        # 查看文件系统命令
		        cmd = "df -h|sed '1d'|awk '{print $2\",\" $3\",\" $4\",\" $6\",\" $5}'"
		        stdin, stdout, stderr = ssh.exec_command(cmd)
		        filesystem_usage = stdout.readlines()
		        # 查看系统时间
		        chk = "date \"+%Y-%m-%d %H:%M:%S\""
		        stdin, stdout, stderr = ssh.exec_command(chk)
		        check_time = stdout.readlines()
		        check_time = check_time[0]
		        # 查看主机名
		        hostname = "hostname"
		        stdin, stdout, stderr = ssh.exec_command(hostname)
		        hostname = stdout.readlines()
		        hostname = hostname[0]
		        # 循环列表，将文件系统使用率插入到数据库中
		        for i in range(len(filesystem_usage)):
		            list_1 = filesystem_usage[i]
		            list_1 = list(list_1.split(','))
		            # print(len(list_1))
		            # 主机ip、主机名、磁盘总大小、已用大小、剩余大小、路径、使用率
		            sql = "insert into filesys_usage(hostip,hostname,alldisk,disk_use,disk_free,filepath,usage,check_time) values('%s','%s','%s','%s','%s','%s','%s','%s')" % (linux[a], hostname, list_1[0], list_1[1], list_1[2], list_1[3], list_1[4], check_time)
		            #print(sql)
		            Mysqlhelper.update(sql)


		        # 查看cpu使用率，并将信息写入到数据库中(取三次平均值)
		        cpu = "vmstat 1 3|sed  '1d'|sed  '1d'|awk '{print $15}'"
		        stdin, stdout, stderr = ssh.exec_command(cpu)
		        cpu = stdout.readlines()
		        cpu_usage = str(round((100 - (int(cpu[0]) + int(cpu[1]) + int(cpu[2])) / 3), 2)) + '%'
		        sql = "insert into cpu_usage(hostname,cpu_use,check_time) values('%s','%s','%s')" % (linux[a], cpu_usage, check_time)

		        #print sql

		        Mysqlhelper.update(sql)

		        # 查看内存使用率，并将信息写入到数据库中

		        mem = "cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'"
		        stdin, stdout, stderr = ssh.exec_command(mem)
		        mem = stdout.readlines()
		        mem_total = round(int(mem[0]) / 1024)
		        mem_total_free = round(int(mem[1]) / 1024) + round(int(mem[2]) / 1024) + round(int(mem[3]) / 1024)

		        mem_use = mem_total - mem_total_free

		        mem_usage = str(round(((mem_total - mem_total_free) / mem_total) * 100, 2)) + "%"
		        sql = "insert into mem_usage(hostname,mem_total,mem_free,mem_use,mem_usage,check_time) values('%s','%s','%s','%s','%s','%s')" % (
		        linux[a], str(round(int(mem[0]) / 1024)) + "M", str(mem_total_free) + "M",
		        str(mem_use) + "M", mem_usage, check_time)
		        #print sql
		        Mysqlhelper.update(sql)


		    except TimeoutError:
		        error = 'can not connect,please check server machine!'
		        #sql = 'insert into error_report values(\'%s\',\'%s\',sysdate,\'%s\')' % (linux[a], check_time, error)
		        print("连接服务器 %s 异常" % (linux[a]))
		        #handledb.MysqldbHelper.update(sql)
		        self.sendMail()
		        continue




	# def connectDB(dbname='orcl'):
	#     if dbname == 'orcl':
	#         connstr = 'system/king@192.168.95.223/orcl'
	#         db = cx_Oracle.connect(connstr)
	#         return db


	# def sqlDML(sql, db):
	#     cr = db.cursor()
	#     cr.execute(sql)
	#     cr.close()
	#     db.commit()
	#

	##定义邮件函数

	def sendMail(from_addr, to_addr, subject, password):
		mail_user = from_addr
		mail_pass = password
		mail_host = "smtp.163.com"
		receiver = to_addr
		sender = "Caldera" + "<" + mail_user + "@163.com" + ">"  # 注意发件人格式
		content = "您的服务器连接异常"

		msg = MIMEText(content)
		msg['Subject'] = '爬虫服务器连接异常'
		msg['From'] = sender
		msg['To'] = receiver

		try:
		    s = smtplib.SMTP()
		    s.connect(mail_host)
		    s.login(mail_user, mail_pass)
		    s.sendmail(sender, receiver, msg.as_string())  # 三个参数不要省略
		    s.close()
		    print('邮件发送成功！')
		except Exception:
		    print("邮件发送失败！")

