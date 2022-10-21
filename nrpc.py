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


MAIN_URL = "https://www.nrpc.co.uk/"

HEADERS = {
    'User-agent': "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"
}

page_number = 1
list_person = []
while True:
    PAGE_URL = f"/findatherapist.php?country=&difficulty=&specialism=&showonmap=1&page={page_number}"
    URL = MAIN_URL + PAGE_URL
    page = requests.get(URL, headers=HEADERS)

    tree = html.fromstring(page.content)
    
    pagina = int(tree.xpath('//select[@name="page"]/../text()')[5].split('of')[1])

    if page_number > pagina:
        print('Proceso terminado...')
        break

    profiles = tree.xpath('//div[@class="blue-box"]//a/@href')
    #print(profiles)

    print(f'Pagina actual: {URL}')
    print(f'Perfiles encontrados: {str(len(profiles))}')

    count = 0
    for profile in profiles:
        try:
            page = requests.get(profile, headers=HEADERS)
            tree = html.fromstring(page.content)
            content = tree.xpath('//div[@class="infopage"]')[0]
            name = content.xpath('.//span')
            email = content.xpath('.//a[starts-with(@href,"mailto:")]/text()')
            if not name or not email:
                pass
            else:
                count = count + 1
                name = name[0].text
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
    page_number = page_number + 1

#save_info(nombre='nrpc_resultados', extension='json', data=json.dumps(list_person))
