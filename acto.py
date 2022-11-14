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
import re
import json
from json_db import json_db

headers = {
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def save_info(nombre, extension, data):
    with open(f'{nombre}.{extension}', 'w', encoding='utf-8') as f:
        f.write(data)

# data -> pagination -> current_page != total_pages
# data -> users -> [?] -> profile_url


def get_profiles():
    page_number = 1
    list_profile = []
    while True:
        payload = f"directory_id=d3bb7&page={page_number}&search=&sorting=&gmt_offset=-3&post_refferer=12970&nonce=ae56239154&action=um_get_members"
        page = requests.post(
            'https://www.acto.org.uk/wp-admin/admin-ajax.php', data=payload, headers=headers)
        content = page.json()
        data = content['data']['pagination']
        current_page = data['current_page']
        total_pages = data['total_pages']
        print(f'Pagina actual: {current_page}')
        print(f'Pagina final: {total_pages}')
        if current_page > total_pages:
            print('Programa finalizado')
            break
        users = content['data']['users']
        for user in users:
            profile = user['profile_url']
            print(profile)
            list_profile.append(profile)
        page_number = page_number + 1
    return list_profile


def get_all(list_profile):
    list_person = []
    for profile in list_profile:
        url = profile
        page = requests.get(url)
        tree = html.fromstring(page.content)
        email = tree.xpath(
            '//div[@class="um-field-value"]//a[starts-with(@href,"mailto:")]/text()')
        name = tree.xpath(
            '//h1/text()')
        if not email:
            pass
        else:
            size = len(email)
            print('Encontro')
            email_content = email[0]
            name = name[0]
            print(email_content)
            print(name)
            data = {
                'name': name,
                'email': email_content,
                'url': url
            }

            json_db(data)

            if size > 1 and email[0] != email[1]:
                print('Encontro 2')
                email_content = email[1]
                print(email_content)
                name = name[0]
                print(email)
                print(name)
                data = {
                    'name': name,
                    'email': email,
                    'url': url
                }

                json_db(data)

    return list_person


lista = get_profiles()
obtenido = get_all(lista)
