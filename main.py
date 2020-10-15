from api import VkAPI, YandexAPI
import requests
from datetime import date
import json
from tqdm import tqdm


def write_photos_to_yandex(vk_name, yandex_token, folder=f'VK_photos_{date.today()}', album='profile', max_last_photos=5):
    """пишем на яндекс.диск и список файлов в photos.json"""
    vk = VkAPI(vk_name)
    ya = YandexAPI(yandex_token)
    if not ya.object_exist(folder):
        print(ya.create_folder(folder))
    else:
        print(f'{folder} folder already exists')
    photo_files = []
    photo_list = vk.get_photo_list(album, max_last_photos)
    log = []
    for photo in tqdm(photo_list, desc='Uploading photos'):
        response = requests.get(photo['url'])
        img = response.content
        if response.status_code == 200:
            status_code = ya.upload(folder + '/' + photo['file_name'], img)
            log.append(f'{photo["file_name"]:_<30}{YandexAPI.API_ERRORS[status_code]}')
            if status_code == 201:
                photo_files.append({'file_name': photo['file_name'], 'size': photo['type']})
        else:
            log.append(f'{photo["file_name"]:_<30}{response.text.split("<title>")[1].split("</title>")[0]}')
    print(*log, sep='\n')
    with open('photos.json', 'w', encoding='utf-8') as f:
        json.dump(photo_files, f, indent=2)


if __name__ == '__main__':
    try:
        write_photos_to_yandex('begemot_korovin', '<TOKEN>')
    except requests.HTTPError as http_error:
        print(http_error)
    except requests.RequestException as requests_error:
        print(requests_error)
