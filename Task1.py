import requests,json,csv,mysql.connector
try:

    fp1=open("user.json",'w')
    fp2=open('user.csv','w',newline="")
    #Extract Data from Rest API
    user_resp=requests.get('https://jsonplaceholder.typicode.com/users')
    users=user_resp.json()
    #Transform for CSV File and json file
    user_data_t=[]
    user_data_d=[]
    for user in users:
        user_data_t.append((user['id'],
                          user['username'],
                          user['email'],
                          user['address']['city']))
        user_data_d.append({"uid":user['id'],
                           "uname":user['username'],
                           "email":user['email'],
                           "city":user['address']['city']})
    #a)CSV File  
    cw_obj=csv.writer(fp2)
    cw_obj.writerow(["uid","uname","email","city"])
    cw_obj.writerows(user_data_t)
    print("New CSV File Created Successfully")

    #  json file
    json.dump(user_data_d,fp1)
    print("New JSON file Created")

    #mysql connector
    dbcon=None
    cursor=None
    dbcon=mysql.connector.connect(
                                host="localhost",
                                user='root',
                                password='root',
                                database='db5'
    )
    print(dbcon.is_connected())
    cursor=dbcon.cursor()
    sql_st=''' INSERT INTO users(uid,uname,email,city)values(%s,%s,%s,%s);'''
    cursor.executemany(sql_st,user_data_t)
    dbcon.commit()
    print("Data Inserted Successfully!")
except mysql.connector.Error as err:
    print(err)
finally:
    cursor.close()
    dbcon.close()
     