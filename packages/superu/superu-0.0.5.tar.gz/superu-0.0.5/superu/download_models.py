import requests
import os

class FileDownloader:
    def __init__(self):
        self.downloading_files = ["binary_model_06022024_v1.pth" , "merged_data.csv" , "no_api_model_06022024_v1.pth"]
        self.base_url = "https://static.pathora.in/user_intent_profiling/"

    def download_file(self, url, destination):
        response = requests.get(url)
        if response.status_code == 200:
            with open(destination, 'wb') as f:
                f.write(response.content)
            print("File downloaded successfully!", destination)
        else:
            print("Failed to download file. Status code:", response.status_code)

    def check_and_download_file(self, url, destination):
        if os.path.exists(destination):
            print("File already exists.", destination)
        else:
            print("Downloading file...", destination)
            self.download_file(url, destination)

    def download_files(self):
        for file_name in self.downloading_files:
            if os.path.exists("data"):
                print("Folder Exists")
            else:
                os.mkdir("data")
            destination = "data/" + file_name
            url = self.base_url + file_name
            self.check_and_download_file(url, destination)