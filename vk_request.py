import requests
from datetime import date
import json

token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
ver = '5.124'

def get_id(screen_name):
    vk_api_resolve_screen_name_url = 'https://api.vk.com/method/utils.resolveScreenName'
    payload = {'screen_name': screen_name, 'access_token': token, 'v': ver}
    r = requests.get(vk_api_resolve_screen_name_url, params = payload)
    if r.json()['response']:
        return str(r.json()['response']['object_id'])
    return ''

name = 'shadow_tm'

vk_api_url = 'https://api.vk.com/method/photos.get'
payload = {'owner_id': get_id(name), 'album_id': 'profile', 'extended': '1', 'photo_sizes': '1', 'access_token': token, 'v': ver}


r = requests.get(vk_api_url, params = payload)


try:
    photo_list = []
    like_list = []
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
except:
    print(r.json()['error']['error_msg'])


photo_names = []
photo_name = {}
for photo in photo_list:
    if  like_list.count(photo['likes']) == 1:
        photo_name = {'file_name': f'{photo["likes"]}', 'size': f'{photo["type"]}'}
    else:
        photo_name = {'file_name': f'{photo["likes"]}_{date.fromtimestamp(photo["date"])}', 'size': f'{photo["type"]}'}
    photo_names.append(photo_name)


with open('photos.json', 'w', encoding='utf-8') as f:
    json.dump(photo_names, f, indent=2)
