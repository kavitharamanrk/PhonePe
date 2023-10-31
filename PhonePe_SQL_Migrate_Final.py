import os
import json

import pandas as pd

import requests
import mysql.connector 

work_dir=''
fname = "data"
dbname=""
add_path_agg="Country\india\state"
add_path_map="hover\Country\india\state"
add_path_top="Country\india\state"

def get_agg_list_path(agg_list):
    for i in agg_list_folder:
        agg_trans=os.path.join(agg_list,agg_list_folder[0])
        agg_user=os.path.join(agg_list,agg_list_folder[1])
        agg_trans_path=os.path.join(agg_trans,add_path_agg)
        agg_user_path=os.path.join(agg_user,add_path_agg)
    return agg_trans_path,agg_user_path
def get_map_list_path(map_list):
    for i in map_list_folder:
        map_trans=os.path.join(map_list,map_list_folder[0])
        map_user=os.path.join(map_list,map_list_folder[1])
        map_trans_path=os.path.join(map_trans,add_path_map)
        map_user_path=os.path.join(map_user,add_path_map)
    return map_trans_path,map_user_path
def get_top_list_path(top_list):
    for i in top_list_folder:
        top_trans=os.path.join(top_list,top_list_folder[0])
        top_user=os.path.join(top_list,top_list_folder[1])
        top_trans_path=os.path.join(top_trans,add_path_top)
        top_user_path=os.path.join(top_user,add_path_top)
    return top_trans_path,top_user_path
def push_agg_trans_data(agg_trans_path):
    ppcol1= {'State': [], 'Year': [], 'Quarter': [], 'Type': [], 'Count': [],
            'Amount': []}
    agg_trans_dir = os.listdir(agg_trans_path)  
    for state in agg_trans_dir:
        cur_state=os.path.join(agg_trans_path,state)
        agg_year_list = os.listdir(cur_state)
        for year in agg_year_list:
            cur_year=os.path.join(cur_state,year)
            agg_file_list = os.listdir(cur_year)
            
            for file in agg_file_list:
                cur_file=os.path.join(cur_year,file)                
                # print(cur_file)
                data = open(cur_file, 'r')
                readJson = json.load(data)
                
                for i in readJson['data']['transactionData']:
                    trans_name = i['name']
                    trans_count = i['paymentInstruments'][0]['count']
                    trans_amount = i['paymentInstruments'][0]['amount']

                    ppcol1['State'].append(state)
                    ppcol1['Year'].append(year)
                    ppcol1['Quarter'].append(int(file.strip('.json')))
                    ppcol1['Type'].append(trans_name)
                    ppcol1['Count'].append(trans_count)
                    ppcol1['Amount'].append(trans_amount)
                    
    df_agg_trans = pd.DataFrame(ppcol1)
    return df_agg_trans

def push_agg_user_data(agg_user_path):
    ppcol2 = {'State': [], 'Year': [], 'Quarter': [], 'Brand': [], 'Count': [],
            'Percentage': []}
    agg_user_dir = os.listdir(agg_user_path)  
    for state in agg_user_dir:
        cur_state=os.path.join(agg_user_path,state)
        agg_year_list = os.listdir(cur_state)
        for year in agg_year_list:
            cur_year=os.path.join(cur_state,year)
            agg_file_list = os.listdir(cur_year)
            
            for file in agg_file_list:
                cur_file=os.path.join(cur_year,file)                
                data = open(cur_file, 'r')
                readJson = json.load(data)

                try:
                    for i in readJson['data']['usersByDevice']:
                        brand_name = i['brand']
                        brand_count = i['count']
                        brand_percentage = i['percentage']

                        ppcol2['State'].append(state)
                        ppcol2['Year'].append(year)
                        ppcol2['Quarter'].append(int(file.strip('.json')))
                        ppcol2['Brand'].append(brand_name)
                        ppcol2['Count'].append(brand_count)
                        ppcol2['Percentage'].append(brand_percentage)
                except Exception as e:
                    continue    
    df_agg_user = pd.DataFrame(ppcol2)

    return df_agg_user

def push_map_trans_data(map_trans_path):    
    ppcol3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
            'Amount': []}
    map_trans_dir = os.listdir(map_trans_path)  
    for state in map_trans_dir:
        cur_state=os.path.join(map_trans_path,state)
        map_year_list = os.listdir(cur_state)
        for year in map_year_list:
            cur_year=os.path.join(cur_state,year)
            map_file_list = os.listdir(cur_year)
            
            for file in map_file_list:
                cur_file=os.path.join(cur_year,file)                
                data = open(cur_file, 'r')
                readJson = json.load(data)
                # print(readJson)
                for i in readJson['data']["hoverDataList"]:
                    district = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]

                    ppcol3['State'].append(state)
                    ppcol3['Year'].append(year)
                    ppcol3['Quarter'].append(int(file.strip('.json')))
                    ppcol3['District'].append(district)
                    ppcol3['Count'].append(count)
                    ppcol3['Amount'].append(amount)                    
    df_map_trans = pd.DataFrame(ppcol3)
    return df_map_trans

def push_map_user_data(map_user_path):
    ppcol4 = {"State": [], "Year": [], "Quarter": [], "District": [],
            "Registered_Users": [], "AppOpens": []}

    map_user_dir = os.listdir(map_user_path)  
    for state in map_user_dir:
        cur_state=os.path.join(map_user_path,state)
        map_year_list = os.listdir(cur_state)
        for year in map_year_list:
            cur_year=os.path.join(cur_state,year)
            map_file_list = os.listdir(cur_year)
            
            for file in map_file_list:
                cur_file=os.path.join(cur_year,file)                
                data = open(cur_file, 'r')
                readJson = json.load(data)
                # print(readJson)
                district=[]
                dis=readJson['data']['hoverData']                   
                for i in dis:
                    district=i
                    for key,val in dis[i].items():
                        if key=='registeredUsers':
                            registereduser=val
                        elif key=='appOpens':
                            appOpens = val
                    
                    ppcol4['State'].append(state)
                    ppcol4['Year'].append(year)
                    ppcol4['Quarter'].append(int(file.strip('.json')))
                    ppcol4["District"].append(district)
                    ppcol4["Registered_Users"].append(registereduser)
                    ppcol4["AppOpens"].append(appOpens)
    df_map_user = pd.DataFrame(ppcol4)
    return df_map_user

def push_top_trans_data(top_trans_path):
    ppcol5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Count': [],
                'Amount': []}
    top_trans_dir = os.listdir(top_trans_path)  
    for state in top_trans_dir:
        cur_state=os.path.join(top_trans_path,state)
        top_year_list = os.listdir(cur_state)
        for year in top_year_list:
            cur_year=os.path.join(cur_state,year)
            top_file_list = os.listdir(cur_year)
            
            for file in top_file_list:
                cur_file=os.path.join(cur_year,file)                
                data = open(cur_file, 'r')
                readJson = json.load(data)  

                for i in readJson['data']['pincodes']:
                    name = i['entityName']
                    count = i['metric']['count']
                    amount = i['metric']['amount']
                    ppcol5['State'].append(state)
                    ppcol5['Year'].append(year)
                    ppcol5['Quarter'].append(int(file.strip('.json')))
                    ppcol5['Pincode'].append(name)
                    ppcol5['Count'].append(count)
                    ppcol5['Amount'].append(amount)

    df_top_trans = pd.DataFrame(ppcol5)
    return df_top_trans

def push_top_user_data(top_user_path):
    ppcol6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
                'RegisteredUsers': []}
    top_user_dir = os.listdir(top_user_path)  
    for state in top_user_dir:
        cur_state=os.path.join(top_user_path,state)
        top_year_list = os.listdir(cur_state)
        for year in top_year_list:
            cur_year=os.path.join(cur_state,year)
            top_file_list = os.listdir(cur_year)
            
            for file in top_file_list:
                cur_file=os.path.join(cur_year,file)                
                data = open(cur_file, 'r')
                readJson = json.load(data)  
             
                for i in readJson['data']['pincodes']:
                    name = i['name']
                    ppcol6['State'].append(state)
                    ppcol6['Year'].append(year)
                    ppcol6['Quarter'].append(int(file.strip('.json')))
                    registeredUsers = i['registeredUsers']
                    ppcol6['Pincode'].append(name)
                    ppcol6['RegisteredUsers'].append(registeredUsers)

    df_top_user = pd.DataFrame(ppcol6)         
    return df_top_user

def insert_data(type,df_data):
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database=dbname
        )
    mycursor = mydb.cursor(buffered=True)
    if type=="agg_trans":
        for i,row in df_data.iterrows():
            sqlquery = "INSERT INTO agg_transaction VALUES (%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sqlquery, tuple(row))
            mydb.commit()
    elif type=="agg_user":
        for i,row in df_data.iterrows():
            sqlquery = "INSERT INTO agg_user VALUES (%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sqlquery, tuple(row))
            mydb.commit()
    elif type=='map_trans':
        for i,row in df_data.iterrows():
            sql = "INSERT INTO map_transaction VALUES (%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, tuple(row))
            mydb.commit()
    elif type=='map_user':
        for i,row in df_data.iterrows():
            sql = "INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, tuple(row))
            mydb.commit()
    elif type=='top_trans':
        for i,row in df_data.iterrows():
            sql = "INSERT INTO top_transaction VALUES (%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sql, tuple(row))
            mydb.commit()
    elif type=='top_user':
        for i,row in df_data.iterrows():
            sql = "INSERT INTO top_user VALUES (%s,%s,%s,%s,%s)"
            mycursor.execute(sql, tuple(row))
            mydb.commit()
    return "Success"

work_dir = os.path.join(os.getcwd(),fname)
work_dir_list = os.listdir(work_dir)   
for i in range(len(work_dir_list)):
    if i==0:
        agg_list=os.path.join(work_dir,work_dir_list[0])
        agg_list_folder = os.listdir(agg_list)
        agg_trans_path,agg_user_path=get_agg_list_path(agg_list)
        df_agg_trans=push_agg_trans_data(agg_trans_path)
        insert_data("agg_trans",df_agg_trans)
        df_agg_user=push_agg_user_data(agg_user_path)
        insert_data("agg_user",df_agg_user)
    elif i==1:
        map_list=os.path.join(work_dir,work_dir_list[1]) 
        map_list_folder = os.listdir(map_list)
        map_trans_path,map_user_path=get_map_list_path(map_list)
        df_map_trans=push_map_trans_data(map_trans_path)
        insert_data("map_trans",df_map_trans)
        df_map_user=push_map_user_data(map_user_path)
        insert_data("map_user",df_map_user)
    elif i==2:      
        top_list=os.path.join(work_dir,work_dir_list[2]) 
        top_list_folder = os.listdir(top_list)
        top_trans_path,top_user_path=get_top_list_path(top_list)
        df_top_trans=push_top_trans_data(top_trans_path)
        insert_data("top_trans",df_top_trans)
        df_top_user=push_top_user_data(top_user_path)
        insert_data("top_user",df_top_user)