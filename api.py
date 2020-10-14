import requests
from datetime import date
import json
import os
import tqdm


class VkAPI:
    API_URL = 'https://api.vk.com/method'
    TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    VER = '5.124'

    def __init__(self, screen_name: str):
        self.token = VkAPI.TOKEN
        self.name = screen_name
        self.ver = VkAPI.VER

    def get_id(self, screen_name):  # проверить screen_name или id
        endpoint = '/utils.resolveScreenName'
        kwargs = {
            'screen_name': screen_name,
            'access_token': self.token,
            'v': self.ver
        }
        response = requests.get(VkAPI.API_URL + endpoint, params=kwargs)
        response.raise_for_status()
        if response.json()['response']:
            return str(response.json()['response']['object_id'])
        return ''  # хрень

    def get_photo_list(self):
        endpoint = '/photos.get'
        kwargs = {
            'owner_id': self.get_id(self.name),
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': self.ver
        }
        response = requests.get(VkAPI.API_URL + endpoint, params=kwargs)
        response.raise_for_status()
        photo_list = []
        like_list = []
        for item in response.json()['response']['items']:
            max_not_found = True
            for type_ in 'wzyxms':
                for size in item['sizes']:
                    if max_not_found and type_ == size['type']:
                        max_not_found = False
                        photo = {'likes': item['likes']['count'], 'date': item['date'], 'type': size['type'],
                                 'url': size['url']}
                        photo_list.append(photo)
                        like_list.append(item['likes']['count'])
                        break
        for photo in photo_list:
            if like_list.count(photo['likes']) == 1:
                photo['file_name'] = f'{photo["likes"]}.{photo["url"].split("?")[0].rsplit(".")[-1]}'
            else:
                photo['file_name'] = f'{photo["likes"]}_{date.fromtimestamp(photo["date"])}.{photo["url"].split("?")[0].rsplit(".")[-1]}'
        return photo_list


class YandexAPI:
    API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path, data):
        """Метод загруджает данные в file_path на яндекс диск"""
        endpoint = '/upload'
        auth_header = {'Authorization': self.token}
        kwargs = {'path': '/' + file_path.rsplit(os.path.sep)[-1]}
        upload_response = requests.get(YandexAPI.API_URL + endpoint, headers=auth_header, params=kwargs)
        upload_response.raise_for_status()
        response = requests.put(upload_response.json()['href'], data)
        response.raise_for_status()
        return response.status_code

    def create_folder(self, folder=f'VK_photos_{date.today()}'):
        """Метод создает папку на яндекс диск. По умолчанию VK_photos+<сегодняшняя дата>"""
        auth_header = {'Authorization': self.token}
        kwargs = {'path': folder}
        response = requests.put(YandexAPI.API_URL, headers=auth_header, params=kwargs)
        response.raise_for_status()
        return f'Folder {kwargs["path"]} created'


def write_list_to_file(photo_list: list, yandex_handler: YandexAPI, folder=f'VK_photos_{date.today()}'):
    photo_files = []
    for photo in photo_list:
        response = requests.get(photo['url'])
        img = response.content
        if response.status_code == 200:
            yandex_handler.upload(folder + '/' + photo['file_name'], img)
            print(f'{photo["file_name"]:_<20}Ok')
            photo_files.append({'file_name': photo['file_name'], 'size': photo['type']})
        else:
            print(f'{photo["file_name"]:_<20}{response.text.split("<title>")[1].split("</title>")[0]}')
    with open('photos.json', 'w', encoding='utf-8') as f:
        json.dump(photo_files, f, indent=2)


if __name__ == '__main__':
    yandex = YandexAPI('<TOKEN>')
    vk = VkAPI('shadow_tm')
    try:
        yandex.create_folder()
        write_list_to_file(vk.get_photo_list(), yandex)
    except requests.HTTPError as http_error:
        print(http_error)