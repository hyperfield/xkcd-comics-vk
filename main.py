#!/usr/bin/env python3

from dotenv import load_dotenv
from os import getenv, remove
import logging
from pathlib import Path
from random import randint
import requests
import urllib3
from urllib.parse import urlsplit, unquote


def fetch_image(img_url, file_name, folder='.'):
    file_path = Path(folder, file_name)
    if file_path.is_file():
        logging.info(
            f"fetch_image(): {file_path} already exists, not fetching it"
        )
        return file_path

    img_response = requests.get(img_url, verify=False)
    img_response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(img_response.content)
    return file_path


def get_photo_publish_address(vk_access_token, vk_group_id, vk_api_ver):
    photo_upload_api_url = "https://api.vk.com/method/photos.getWallUploadServer"
    photo_upload_params = {"access_token": vk_access_token,
                           "group_id": vk_group_id, "v": vk_api_ver}
    photo_upload_url_response = requests.get(photo_upload_api_url,
                                             params=photo_upload_params)
    photo_upload_url_response.raise_for_status()
    return photo_upload_url_response.json()['response']['upload_url']


def upload_photo_vk(file_path, photo_upload_addr):
    with open(file_path, 'rb') as file:
        files = {
            'file1': file,
        }
        response = requests.post(photo_upload_addr, files=files)
        response.raise_for_status()
        return response.json()


def save_photo_vk(vk_access_token, vk_group_id, vk_api_ver, vk_photo_param,
                  vk_server_param, vk_hash, photo_caption):
    photo_save_api_url = "https://api.vk.com/method/photos.saveWallPhoto"
    photo_save_params = {"access_token": vk_access_token,
                         "v": vk_api_ver, "group_id": vk_group_id,
                         "photo": vk_photo_param, "server": vk_server_param,
                         "hash": vk_hash, "caption": photo_caption}
    photo_save_response = requests.post(photo_save_api_url,
                                        params=photo_save_params)
    photo_save_response.raise_for_status()
    return photo_save_response.json()


def publish_photo_vk(vk_access_token, vk_api_ver, owner_id, from_group,
                     message, photo_owner_id, photo_media_id):
    photo_publish_api_url = "https://api.vk.com/method/wall.post"
    photo_publish_params = {"access_token": vk_access_token,
                            "v": vk_api_ver, "owner_id": -int(owner_id),
                            "message": message, "from_group": from_group,
                            "attachments":
                                [f"photo{photo_owner_id}_{photo_media_id}"]}
    photo_publish_reponse = requests.post(photo_publish_api_url,
                                          params=photo_publish_params)
    photo_publish_reponse.raise_for_status()
    return photo_publish_reponse.json()


def post_photo_vk(vk_access_token, vk_group_id, vk_api_ver, img_file_name,
                  comic_comment):
    photo_upload_addr = get_photo_publish_address(vk_access_token,
                                                  vk_group_id, vk_api_ver)
    vk_photo_upload_response = upload_photo_vk(img_file_name,
                                               photo_upload_addr)
    vk_save_photo_response = save_photo_vk(vk_access_token, vk_group_id,
                                           vk_api_ver,
                                           vk_photo_upload_response["photo"],
                                           vk_photo_upload_response["server"],
                                           vk_photo_upload_response["hash"],
                                           comic_comment)
    vk_publish_photo = publish_photo_vk(
        vk_access_token, vk_api_ver, vk_group_id, 1,
        vk_save_photo_response["response"][0]["text"],
        vk_save_photo_response["response"][0]["owner_id"],
        vk_save_photo_response["response"][0]["id"]
        )
    return vk_publish_photo


def post_comic_vk(vk_access_token, vk_group_id, vk_api_ver,
                  latest_comic_number=0, comic_response=None):

    if comic_response is None:
        random_comic_number = randint(0, latest_comic_number)
        comic_response = requests.get(
            f"https://xkcd.com/{random_comic_number}/info.0.json"
            )
        comic_response.raise_for_status()
        comic_response = comic_response.json()
    comic_img_url = comic_response["img"]
    comic_comment = comic_response["alt"]
    relative_img_path = urlsplit(comic_img_url).path
    img_file_name = unquote(relative_img_path.split('/')[-1])
    fetch_image(comic_img_url, img_file_name)
    vk_response = post_photo_vk(vk_access_token, vk_group_id, vk_api_ver,
                                img_file_name, comic_comment)
    remove(img_file_name)
    return vk_response


def main():
    load_dotenv()
    vk_access_token = getenv("VK_ACCESS_TOKEN")
    vk_api_ver = getenv("VK_API_VER")
    vk_group_id = getenv("VK_GID")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    comic_response = requests.get("https://xkcd.com/info.0.json")
    comic_response.raise_for_status()
    latest_comic_number = comic_response.json()["num"]

    # Post a random comic
    post_comic_vk(vk_access_token, vk_group_id, vk_api_ver,
                  latest_comic_number)


if __name__ == '__main__':
    main()
