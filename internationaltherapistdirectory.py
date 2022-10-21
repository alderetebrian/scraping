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


MAIN_URL = "https://internationaltherapistdirectory.com/"

HEADERS = {
    'User-agent': "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"
}

page_number = 1
list_person = []
while True:
    PAGE_URL = f"/page/{page_number}/?geodir_search=1&stype=gd_place&s=+&snear&sgeo_lat&sgeo_lon"
    URL = MAIN_URL + PAGE_URL
    page = requests.get(URL, headers=HEADERS)

    if 'No listings were found matching your selection.' in page.text:
        print('Proceso terminado...')
        break

    tree = html.fromstring(page.content)
    content = tree.xpath('//div[@class="geodir-loop-container  sdel-16e277cd"]')[0]
    profiles = content.xpath('.//li')

    print(f'Pagina actual: {URL}')
    print(f'Perfiles encontrados: {str(len(profiles))}')

    count = 0
    for profile in profiles:
        name = profile.xpath('.//h2//text()')
        email = profile.xpath('.//a[starts-with(@href, "javascript:window.location.href")]/text()')
        if not name or not email:
            pass
        else:
            count = count + 1
            name = " ".join(name).strip()
            email = "".join(email).strip()
            data = {
                'name': name,
                    'email': email,
                    'url': URL
            }
            #list_person.append(data)

            json_db(data=data)
    print(f'Perfiles con emails: {str(count)}')
    page_number = page_number + 1

#save_info(nombre='international_resultados', extension='json',data=json.dumps(list_person))
