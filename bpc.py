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

def save_info(nombre,extension,data):
    with open(f'{nombre}.{extension}', 'w', encoding='utf-8') as f:
        f.write(data)

MAIN_URL = "https://www.bpc.org.uk"

HEADERS = {
	'User-agent': "Mozilla/5.0 (Android; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"
}

page_number = 1
list_person = []
while True:
	PAGE_URL = f"/information-support/find-a-therapist-or-clinic/page/{page_number}/"
	URL = MAIN_URL + PAGE_URL
	page = requests.get(URL, headers=HEADERS)
	tree = html.fromstring(page.content)

	profiles = tree.xpath('//div[@class="people__person"]')

	print(f'Pagina actual: {URL}')
	print(f'Perfiles encontrados: {str(len(profiles))}')
	
	count = 0
	for profile in profiles:
		name = profile.xpath('.//h3/text()')
		email = profile.xpath('.//p[@class="people__email"]/a/text()')
		name = name[0]
		if not email:
			pass
		else:
			count = count + 1
			email = email[0]
			data = {
				'name': name,
				'email': email,
				'url': URL
			}
			
			list_person.append(data)
	print(f'Perfiles con emails: {str(count)}')	
	page_number = page_number + 1
	if 'No therapists or clinics found.' in page.text:
		print('Proceso terminado...')	
		break

save_info(nombre='resultados',extension='json',data=str(list_person))

