import requests

vk_api_url = 'https://api.vk.com/method/photos.get'
payload = {'album_id': 'profile', 'extended': '1', 'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008', 'v': '5.124'}

r = requests.get(vk_api_url, params = payload)
for item in r.json()['response']['items']:
    for size in item['sizes']:
        print(size['type'], size['url'])
    print(item['likes']['count'], item['date'])

