import requests
from datetime import date
import os
from tqdm import tqdm


class VkAPI:
    API_URL = 'https://api.vk.com/method'
    TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    VER = '5.124'

    def __init__(self, name):
        self.token = VkAPI.TOKEN
        self.ver = VkAPI.VER
        self.id = self.get_id(name)

    def get_id(self, name):
        """получаем id если пользователь ввел screen_name"""
        endpoint = '/users.get'
        kwargs = {
            'user_ids': name,
            'access_token': self.token,
            'v': self.ver
        }
        response = requests.get(VkAPI.API_URL + endpoint, params=kwargs)
        response.raise_for_status()
        if 'error' in response.json():
            raise requests.RequestException(response.json()['error']['error_msg'])
        return response.json()['response'][0]['id']

    def get_photo_list(self, album, max_last_photos):
        """
        получаем список фотографий профиля,
        выбираем максимальные размеры по типу,
        """
        endpoint = '/photos.get'
        kwargs = {
            'owner_id': self.id,
            'album_id': album,
            'extended': '1',
            'photo_sizes': '1',
            'rev': '1',
            'access_token': self.token,
            'v': self.ver
        }
        response = requests.get(VkAPI.API_URL + endpoint, params=kwargs)
        response.raise_for_status()
        if 'error' in response.json():
            raise requests.RequestException(response.json()['error']['error_msg'])
        photo_list = []
        for item in tqdm(response.json()['response']['items'], initial=1, desc='Preparing URLs  '):
            max_not_found = True
            for type_ in 'wzyxms':
                for size in item['sizes']:
                    if max_not_found and type_ == size['type']:
                        max_not_found = False
                        photo = {'likes': item['likes']['count'], 'date': item['date'], 'type': size['type'],
                                 'url': size['url'], 'id': item['id']}
                        photo_list.append(photo)
                        break
            max_last_photos -= 1
            if max_last_photos == 0:
                break
        return VkAPI._add_names(photo_list)

    @staticmethod
    def _add_names(photo_list):
        """создаем имена файлов из количества лайков, даты создания и, в крайнем случае, id"""
        names = []
        for photo in photo_list:
            file_name = f'{photo["likes"]}.' \
                        f'{photo["url"].split("?")[0].rsplit(".")[-1]}'
            if file_name in names:
                file_name = f'{photo["likes"]}_' \
                            f'{date.fromtimestamp(photo["date"])}.' \
                            f'{photo["url"].split("?")[0].rsplit(".")[-1]}'
            if file_name in names:
                file_name = f'{photo["likes"]}_' \
                            f'{date.fromtimestamp(photo["date"])}_' \
                            f'{photo["id"]}.' \
                            f'{photo["url"].split("?")[0].rsplit(".")[-1]}'
            photo['file_name'] = file_name
            names.append(file_name)
        return photo_list


class YandexAPI:
    API_URL = 'https://cloud-api.yandex.net/v1/disk/resources'
    API_ERRORS = {
        200: "OK",
        201: "OK",
        400: "Некорректные данные",
        401: "Не авторизован",
        403: "API недоступно",
        404: "Не удалось найти запрошенный ресурс",
        406: "Ресурс не может быть представлен в запрошенном формате",
        409: "Ресурс уже существует",
        423: "Ресурс заблокирован",
        429: "Слишком много запросов",
        503: "Сервис временно недоступен",
        507: "Недостаточно свободного места"
    }

    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path, data):
        """Метод загруджает данные в file_path на яндекс диск"""
        endpoint = '/upload'
        auth_header = {'Authorization': self.token}
        kwargs = {'path': '/' + file_path.rsplit(os.path.sep)[-1]}
        upload_response = requests.get(YandexAPI.API_URL + endpoint, headers=auth_header, params=kwargs)
        if upload_response.status_code != 200:
            return upload_response.status_code
        response = requests.put(upload_response.json()['href'], data)
        response.raise_for_status()
        return response.status_code

    def create_folder(self, folder):
        """Метод создает папку на яндекс диск. По умолчанию VK_photos+<сегодняшняя дата>"""
        auth_header = {'Authorization': self.token}
        kwargs = {'path': folder}
        response = requests.put(YandexAPI.API_URL, headers=auth_header, params=kwargs)
        response.raise_for_status()
        return f'Folder {kwargs["path"]} created'

    def object_exist(self, path):
        """Метод возвращает True, если объект уже существует"""
        auth_header = {'Authorization': self.token}
        kwargs = {'path': path}
        response = requests.get(YandexAPI.API_URL, headers=auth_header, params=kwargs)
        return True if response.status_code == 200 else False
