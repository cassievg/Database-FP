import mysql.connector

__cnx=None

def getsqlconnection():
    global __cnx
    if __cnx is None:
        __cnx = mysql.connector.connect(user='root', password='ellis',
                                host='127.0.0.1',
                                database='onlinestore')
    return __cnx
