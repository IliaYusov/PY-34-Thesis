from api import VkAPI, YandexAPI
from datetime import date
import json
import os

TODAY = date.today()


def save_output(files_list):
    with open('photos.json', 'w', encoding='utf-8') as f:
        json.dump(files_list, f, indent=2)


def main(
        vk_name,
        folder=f'VK_photos_{TODAY}',
        album='profile',
        max_last_photos=5
):
    vk = VkAPI(vk_name)
    ya = YandexAPI()
    ya.create_folder(folder)
    photo_list = vk.get_photo_list(album, max_last_photos)
    files_list = ya.upload_photos(photo_list, folder)
    save_output(files_list)


if __name__ == '__main__':
    VK_NAME = os.environ.get('VK_NAME')
    main(VK_NAME, 'TestFolder', 'wall', 20)
