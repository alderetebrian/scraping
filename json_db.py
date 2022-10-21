#!/usr/bin/python

import sqlite3

def json_db(data:dict):
    email = data['email']
    name = data['name']
    url = data['url']
    try:
        conn = sqlite3.connect('test.db')
        #print("Opened database successfully")
        conn.execute(f"INSERT INTO scrap_contenido (email,name,url) \
            VALUES ('{email}', '{name}', '{url}')")
        print('Datos Ingresados:')
        print(f'Email: {email}')
        print(f'Name: {name}')
        conn.commit()
        conn.close()
    except Exception as e:
        pass