import os
import sqlite3
import random
"""
ПОЛЯ
id_         INT PRYMARY KEY   уникальное значение записи
user       INT              автор записи
name       TEXT              название/метка
lat        REAL               
lon        REAL    
time       TEXT             время оповещения 

методы
create_base()                     return T/F
add_base(user,name,lat,lon,time)  return T/F
get_records(user)                 return [(id,user,name,lat,lon,time),(),()...] /F
get_record(id)                    return (id,user,name,lat,lon,time)/F
del_record(id)                    return T/F

cur.execute('CREATE TABLE user_db (id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, name TEXT, lat REAl, lon REAL, time TEXT )')

"""

def creat_base():
    if  (not os.path.exists('data.db')):        
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()  
        cur.execute('CREATE TABLE IF NOT EXISTS user_db (id_ INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, name TEXT, lat REAl, lon REAL, time TEXT )')
    # !!! проверить создание БД, корректнее проверять файл и БД а не только файл  cur.execute("""CREATE TABLE IF NOT EXISTS users(
        return True  

def add_base(user:str, name:str, lat:float, lon:float, time=8):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()    
    cur.execute(f'SELECT * FROM user_db WHERE (user = "{user}" AND name = "{name}" AND lat="{lat}" AND lon= "{lon}" AND time="{time}")')
    result = cur.fetchall()  
    print("add_base: результат поиска", result)
    if result == []:
        cur.execute(f'INSERT INTO user_db (user, name, lat, lon, time) VALUES("{user}", "{name}","{lat}", "{lon}", "{time}")')
        conn.commit()
        print("add_base: Внесена")
        return True
    else:
        print("add_base: Не внесена, дубль")
        return False
    
    
def get_records(user):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()    
    cur.execute(f'SELECT * FROM user_db WHERE (user = "{user}")')
    result = cur.fetchall()
    print("get_records: результат поиска", result)
    if result == []:
        return False
    else:
        word=[]
        for r in result:
            w={"id":r[0],"user":r[1],"name":r[2],"lat":r[3],"lon":r[4],"time":r[5]}
            word.append(w)
            print("get_records: результат ", word)
        return word
def get_record(id_):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()    
    cur.execute(f'SELECT * FROM user_db WHERE (id_ = "{id_}")')
    result = cur.fetchall()
    print("get_record: результат поиска", result)
    if result == []:
        return False
    else:
        return result 
    
def del_record(id_):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()    
    cur.execute(f'SELECT * FROM user_db WHERE (id_ = "{id_}")')
    result = cur.fetchall()
    print("del_record: результат поиска", result)
    if result == []:
        print("del_record:Запись не найдена")
        return False
    else:
        cur.execute(f'DELETE FROM user_db WHERE (id_ = "{id_}")')
        conn.commit()
        print("del_record:Запись найдена, Удалена")
        return True 
    
def get_time_record(time):
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()    
    cur.execute(f'SELECT * FROM user_db WHERE (time = "{time}")')
    result = cur.fetchall()
    print("get_time_record: результат поиска", result)
    if result == []:
        return False
    else:
        word=[]
        for r in result:
            w={"id":r[0],"user":r[1],"name":r[2],"lat":r[3],"lon":r[4],"time":r[5]}
            word.append(w)
        print("get_time_record: результат ", word)
        return word    

if __name__ == "__main__":    
    creat_base()
    user=1
    name=random.randrange(1,100)
    lat=3
    lon=4
    time=9
    for i in range(0,60):
        
        print(add_base(user+i, random.randrange(1,100), lat, lon, i))
        
    #print(add_base(user, name, lat, lon, time))
    #print(get_records(user))
    #print(get_record(10))
    #print(del_record(5))