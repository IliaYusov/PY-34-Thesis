import requests
from datetime import date
import json

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
ver = '5.124'


def get_id(screen_name):
    vk_api_resolve_screen_name_url = 'https://api.vk.com/method/utils.resolveScreenName'
    vk_api_resolve_screen_name_params = {'screen_name': screen_name, 'access_token': token, 'v': ver}
    r = requests.get(vk_api_resolve_screen_name_url, params=vk_api_resolve_screen_name_params)
    if r.json()['response']:
        return str(r.json()['response']['object_id'])
    return ''


name = 'shadow_tm'

vk_api_url = 'https://api.vk.com/method/photos.get'
payload = {'owner_id': get_id(name), 'album_id': 'profile', 'extended': '1', 'photo_sizes': '1', 'access_token': token, 'v': ver}


r = requests.get(vk_api_url, params=payload)
status = r.status_code


photo_list = []
like_list = []
if status == 200:
    for item in r.json()['response']['items']:
        max_not_found = True
        for type_ in 'wzyxms':
            for size in item['sizes']:
                if max_not_found and type_ == size['type']:
                    max_not_found = False
                    photo = {'likes': item['likes']['count'], 'date': item['date'], 'type': size['type'], 'url': size['url']}
                    photo_list.append(photo)
                    like_list.append(item['likes']['count'])
                    break
else:
    print(r.json()['error']['error_msg'])

for photo in photo_list:
    if like_list.count(photo['likes']) == 1:
        photo['file_name'] = f'{photo["likes"]}.{photo["url"].split("?")[0].rsplit(".")[-1]}'
    else:
        photo['file_name'] = f'{photo["likes"]}_{date.fromtimestamp(photo["date"])}.{photo["url"].split("?")[0].rsplit(".")[-1]}'


photo_files = []
for photo in photo_list:
    r = requests.get(photo['url'])
    img = r.content
    if r.status_code == 200:
        with open(photo['file_name'], 'wb') as f:
            f.write(img)
        print(f'{photo["file_name"]:_<20}Ok')
        photo_files.append({'file_name': photo['file_name'], 'size': photo['type']})
    else:
        print(f'{photo["file_name"]:_<20}{r.text.split("<title>")[1].split("</title>")[0]}')

with open('photos.json', 'w', encoding='utf-8') as f:
    json.dump(photo_files, f, indent=2)
