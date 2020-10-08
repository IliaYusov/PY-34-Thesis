import requests
from datetime import date

# import urllib
# import httplib
# import json
# import uritemplate
#
# headers = {'Authorization': '<OAuth токен>'}
# connection = httplib.HTTPSConnection('cloud-api.yandex.net')
# resource_url = '/v1/disk/resources'
#
# def request(method, url, query=None):
#     if query:
#         qs = urllib.urlencode(query)
#         url = '%s?%s' % (url, qs)
#     connection.request(method, url, headers=headers)
#     resp = connection.getresponse()
#     content = resp.read()
#     obj = json.loads(content) if content else None
#     status = resp.status
#     if status == 201:
#         # получаем созданный объект
#         obj = request(obj['method'], obj['href'])
#     return obj
#
# if __name__ == '__main__':
#     # создаём папку
#     path = '/foo'
#     folder = request('PUT', resource_url, {'path': path})
#
#     # перемещаем папку и получаем перемещённую
#     new_path = '/bar'
#     folder = request('POST', '%s/move' % resource_url, {'path': new_path, 'from': path})
#
#     # копируем папку и получаем новую папку
#     copy_path = '/foobar'
#     folder_copy = request('POST', '%s/copy' % resource_url, {'path': copy_path, 'from': new_path})
#
#     # удаляем папки
#     request('DELETE', resource_url, {'path': new_path})
#     request('DELETE', resource_url, {'path': copy_path})

yandex_api_url = 'https://cloud-api.yandex.net/v1/disk/resources'
yandex_api_headers = {'Authorization': ''}

payload = {'path': f'/VK_photos_{date.today()}'}

r = requests.put(yandex_api_url, headers=yandex_api_headers, params=payload)
if r.status_code != 201:
    print(r.json()['message'])
else:
    print(f'Папка {payload["path"]} создана')
