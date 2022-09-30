import requests
from bs4 import BeautifulSoup
import os
import threading


pre_url = "https://danbooru.donmai.us/"
tags = ""
start_page = 1
end_page = 20

# Create folder
img_folder = tags
if not os.path.isdir(img_folder):
    os.mkdir(img_folder)


def crawl_img(id_url):
    print("Crawling  page", id_url, "/", end_page)
    url = pre_url + "/posts?page={}&tags={}".format(id_url, tags)
    response = requests.get(url)
    html = BeautifulSoup(response.text, 'html.parser')
    preview_img = html.find_all('a', attrs={"class": "post-preview-link"})
    for img in preview_img:
        source = pre_url + img['href']
        try:
            # Requests to image source
            img_response = requests.get(source)
            img_html = BeautifulSoup(img_response.text, 'html.parser')
            img = img_html.find('img', attrs={"id": "image"})
            img_source = img['src']

            # Write on file
            img_path = img_source.replace("https://", "")
            img_path = img_path.replace("http://", "")
            img_path = img_path.replace("/", "-")
            if not os.path.exists(img_path):
                img = requests.get(img_source).content
                with open(img_folder + "/" + img_path, "wb+") as f:
                    f.write(img)
        except:
            print(end='')
    print("Crawl successfull page", id_url, "/", end_page)


threads = []
for id in range(start_page, end_page+1):
    t = threading.Thread(target=crawl_img, args=(id,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
