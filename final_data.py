import json
import time
import requests
from tqdm import tqdm


class VkUser:
    def __init__(self, token_, version):
        self.params = {'access_token': token_, 'v': version}

    def pictures_get(self, id_of_owner):
        while True:
            numbers = int(input("How many pictures you like to transfer? Enter numbers and press 'ENTER': "))
            params = {
                'owner_id': id_of_owner,
                'album_id': "profile",
                'count': numbers,
                'extended': 1
            }
            pictures_data = requests.get(URL_VK + 'photos.get', params={**self.params, **params}).json()['response']
            if numbers not in range(pictures_data['count'] + 1):
                print(f"Please note - there are {pictures_data['count']} pictures on account!")
            else:
                pictures_list = []
                for pictures in pictures_data['items']:
                    corrected_data = {'likes': pictures['likes']['count'],
                                      'url': pictures['sizes'][- 1]['url'],
                                      'size': pictures['sizes'][- 1]['type']}
                    pictures_list.append(corrected_data)
                return pictures_list


class YaUser:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                        'Authorization': f'OAuth {self.token}'}

    def create_folder(self):
        folder_name = input("Enter folder name for Yandex Disc: ")
        params = {'path': folder_name}
        requests.put(URL_YU, headers=self.headers, params=params)
        return folder_name

    def upload_file(self, pictures_list):
        folder_name = self.create_folder()
        final_json_file = []
        for pictures in tqdm(pictures_list):
            time.sleep(0.1)
            file_name = f"{pictures['likes']}.jpg"
            pictures_list = {'file_name': file_name, 'size': pictures['size']}
            final_json_file.append(pictures_list)
            params = {"path": f'{folder_name}/{file_name}.jpg', "url": pictures['url']}
            response_upload = requests.post(URL_YU + '/upload', headers=self.headers, params=params)
            response_upload.raise_for_status()
        print("Your files have been uploaded successfully.")

        return json.dumps(final_json_file, indent=2)


if __name__ == '__main__':
    URL_VK = 'https://api.vk.com/method/'
    URL_YU = "https://cloud-api.yandex.net/v1/disk/resources"
    with open('token.txt', 'r') as file_object:
        Vk_token = file_object.read().strip()
    with open('token_yandex.txt', 'r') as file_object:
        Ya_token = file_object.read().strip()
    try:
        profile_id = input("Enter id number and press 'ENTER': ")  # 552934290
        my_vk = VkUser(Vk_token, '5.131')
        my_yd = YaUser(Ya_token)
        pictures__list = my_vk.pictures_get(profile_id)
        print(my_yd.upload_file(pictures__list))
    except KeyError as e:
        print("Wrong id number. Account is out of order.")
