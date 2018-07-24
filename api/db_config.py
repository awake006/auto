import pymysql
'''
fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
fetchall(): 接收全部的返回结果行.
rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
'''


def mysql(self, host, user, passwd, db):
    con = pymysql.connect(host, user, passwd, db)
    cursor = con.cursor()
    return con, cursor
