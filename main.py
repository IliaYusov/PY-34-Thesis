from api import VkAPI, YandexAPI
import requests
from datetime import date
import json


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
