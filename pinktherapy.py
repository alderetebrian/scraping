# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
  ┯━━━━━━━━▧▣▧━━━━━━━━┯
  ━━━━━━━┛ ✠ ┗━━━━━━━━

         Author:
        @alderetebrian

  ━━━━━━━┓ ✠ ┏━━━━━━━━
  ┷━━━━━━━━▧▣▧━━━━━━━━┷
"""

from lxml import html
import requests
import json

from json_db import json_db


def save_info(nombre, extension, data):
    with open(f'{nombre}.{extension}', 'w', encoding='utf-8') as f:
        f.write(data)


MAIN_URL = "http://www.pinktherapy.com"

HEADERS = {
    'User-agent': "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"
}

#/([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)/g regex for match emails
#page_number = 1

lista = []
with open('pinktherapy_perfiles.log') as file:
    for line in file:
        lista.append(line.strip())

list_person = []
PAGE_URL = f"/en-us/findatherapist.aspx"
URL = MAIN_URL + PAGE_URL
page = requests.get(URL, headers=HEADERS)

tree = html.fromstring(page.content)

profiles = lista

print(f'Pagina actual: {URL}')
print(f'Perfiles encontrados: {str(len(profiles))}')

count = 1
for profile in profiles:
    print(f'Perfil Numero: {count}')
    try:
        page = requests.get(profile, headers=HEADERS)
        tree = html.fromstring(page.content)
        name = tree.xpath('//span[@id="dnn_ctr2027_dnnTITLE_lblTitle"]/text()')
        email = tree.xpath('//a[starts-with(@href,"mailto:")]/text()')
        if not name or not email:
            pass
        else:
            count = count + 1
            name = name[0]
            email = email[0]
            data = {
                'name': name,
                'email': email,
                'url': profile
            }

            json_db(data=data)
            #list_person.append(data)
    except:
        print(f'Rompio en la pagina: {profile}')
print(f'Perfiles con emails: {str(count)}')

#save_info(nombre='pinktherapy_resultados', extension='json', data=json.dumps(list_person))
