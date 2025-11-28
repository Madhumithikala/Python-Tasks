import requests,json,csv,mysql.connector,pymongo
from pymongo import MongoClient;

try:
    maa=open('users.csv','w',newline='')
    chaa=open('users.json','w')

    #Extract data from REST API
    user_resp = requests.get("https://jsonplaceholder.typicode.com/users")
    users=user_resp.json()

    user_t=[]
    user_d=[]
    for user in users:
        user_t.append((user ['id'],
                    user ['name'],
                    user['email'],
                    user['phone']
                ))
        user_d.append({"uid":user['id'],
                        "uname":user['name'],
                        "email":user['email'],
                        "phone":user['phone']
                    })
    #csv file
    boss=csv.writer(maa)
    boss.writerow(['uid','uname','email','phone'])
    boss.writerows(user_t)
    print("csv file is created success")
    #json file
    json.dump(user_d,chaa)
    print("Json file is created successfully")

    #mysql connection

    dbcon=None
    cursor=None

    dbcon=mysql.connector.connect(host='localhost',
                            user='root',
                            password='root',
                            database='db2'
                            )
    print(dbcon.is_connected())
    cursor=dbcon.cursor()

    kalki=''' insert into users(id,name,email,phone) values(%s,%s,%s,%s);'''
    cursor.executemany(kalki,user_t)
    dbcon.commit()

    print("Data is inserted mysql file")

    #mongoDB file 

    client=None
    client=MongoClient("mongodb://localhost:27017/")
    malli=client['db2']
    kajal=malli['users']
    kajal.insert_many(user_d)
    print("Data  transfered to mongoDB file")

except mysql.connector.Error as errr:
    print(errr)
finally:
    dbcon.close()
    cursor.close()


