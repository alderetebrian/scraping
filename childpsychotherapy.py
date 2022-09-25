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

headers = {
	'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

def save_info(nombre,extension,data):
    with open(f'{nombre}.{extension}', 'w', encoding='utf-8') as f:
        f.write(data)

def get_profiles():
	page_number = 0
	list_profile = []
	while True:
		print(f'Pagina actual numero: {page_number}')
		payload = f"page={page_number}&view_name=civicrm_contact_distance_search&view_display_id=block_2&languages_spoken_18=All"
		page = requests.post('https://childpsychotherapy.org.uk/views/ajax',data=payload,headers=headers)
		content = page.json()
		data = content[1]['data']
		regex_profile =  '<a href="(/member_details/\d+)">'
		match_profile = re.findall(regex_profile,data)
		if not match_profile:
			break
		list_profile = list_profile + match_profile
		page_number = page_number + 1
	return list_profile

def get_all(list_profile):
	list_person = []
	for profile in list_profile:
		url = 'https://childpsychotherapy.org.uk' + profile
		page = requests.get(url)
		tree = html.fromstring(page.content)
		email = tree.xpath('//div[@class="views-field views-field-email"]//a[starts-with(@href,"mailto:")]/text()')
		name = tree.xpath('//div[@class="views-field views-field-display-name"]//h2/text()')
		if not email:
			pass
		else:
			print('Encontro')
			email = email[0]
			name = name[0]
			data = {
				'name': name,
				'email': email,
				'url': url
			}

			list_person.append(data)
	return list_person

lista = get_profiles()
obtenido = get_all(lista)
save_info(nombre='childpsychotherapy_resultados',extension='json',data=json.dumps(obtenido))
