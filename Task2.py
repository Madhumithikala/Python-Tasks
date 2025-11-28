import requests,json,csv,mysql.connector,pymongo
from pymongo import MongoClient
try:
    fp=open("product.json",'w')
    fw=open("product.csv",'w',newline='')
    #Extraxt data from restAPI
    product_resp=requests.get("https://dummyjson.com/products")
    products=product_resp.json()['products']

    product_data_t=[]
    product_data_d=[]
    for product in products:
        product_data_t.append((product['id'],
                          product['title'],
                          product['category'],
                          product['price'],
                          product['rating']))
        product_data_d.append({"id":product['id'],
                               "title":product['title'],
                               "category":product['category'],
                               "price":product['price'],
                               "rating":product['rating']
                              })
#CSV file                         
    guru=csv.writer(fw)
    guru.writerow(["id","title","category","price","rating"])
    guru.writerows(product_data_t)
    print("CSV file is created Successfully")

#json file
    json.dump(product_data_d,fp)
    print("New json file is created")
#mysql connector
    dbcon=None
    cursor=None
    dbcon=mysql.connector.connect(
                                  host='localhost',
                                  user='root',
                                  password='root',
                                  database='db5'
    )
    print(dbcon.is_connected())
    cursor=dbcon.cursor()
    
    guru1='''INSERT INTO Products (id,title,category,price,rating) values(%s,%s,%s,%s,%s);'''
    cursor.executemany(guru1,product_data_t)
    dbcon.commit() 
    print("Inserted values Successful")

     #mongoDB file
    client=None
    client=MongoClient("mongodb://localhost:27017/")
    db=client['db5']
    product_col=db['products']
    product_col.insert_many(product_data_d)
    print ("inserted values MongoDB successfully")


except mysql.connector.Error as err:
    print(err)
finally:
    dbcon.close()
    cursor.close()
    fp.close()
    fw.close()
   
    
    








