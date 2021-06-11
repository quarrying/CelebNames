import os
import re
import glob
import time
import random
from collections import OrderedDict

import khandy
import requests
from bs4 import BeautifulSoup


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
}


def get_background_image_url(response):
    pattern = re.compile("background-image: url\('(.*)'\);")
    try:
        image_url = pattern.search(response.text).groups()[0]
        image_url = image_url.split('?')[0]
        return image_url
    except Exception as e:
        print(e)
        return None
    
    
def get_summary_image_url(url):
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    summary_pic_tag = soup.find("div", {"class": "summary-pic"})
    if summary_pic_tag is None:
        image_url = get_background_image_url(response)
        return image_url
    summary_img_tag = summary_pic_tag.find('img')
    if summary_img_tag is None:
        return None
    image_url = summary_img_tag['src'].split('?')[0]
    return image_url
    
    
def download_image(url, filename):
    try:
        with open(filename, "wb") as f:
            f.write(requests.get(url, timeout=30).content)
    except Exception as e:
        print(e)


def get_name_by_record(record):
    if record == '' or record.startswith(('#', ' ')):
        return None
    name = record.split(',')[0].strip()
    name = name.split('|')[0].strip()
    return name


def get_name_url_dict(filename):
    name_url_dict = OrderedDict()
    records = khandy.load_list(filename)
    last_name = None
    for record in records:
        name = get_name_by_record(record)
        if name is None:
            if ((last_name is not None) and
                (record.strip().startswith('https://baike.baidu.com/item')) and 
                (last_name in record)):
                name_url_dict[last_name] = record.strip()
        else:
            last_name = name
    return name_url_dict
    
    
if __name__ == '__main__':
    failed_records = []
    dst_dir_root = r'../_local/gallery_images'
    list_filenames = glob.glob(r'../names/chinese/*.txt')
    for k, list_filename in enumerate(list_filenames):
        name_url_dict = get_name_url_dict(list_filename)
        dst_dir = os.path.join(dst_dir_root, khandy.get_path_stem(list_filename))
        os.makedirs(dst_dir, exist_ok=True)
        for i, (name, url) in enumerate(name_url_dict.items()):
            print('[{}/{}][{}/{}] {} {}'.format(k+1, len(list_filenames), 
                                                i+1, len(name_url_dict), name, url))
            dst_filename = os.path.join(dst_dir, name + '.jpg')
            image_url = get_summary_image_url(url)
            time.sleep(random.uniform(1, 3))
            if image_url is not None:
                download_image(image_url, dst_filename)
            else:
                print('get_summary_image_url failed!')
                failed_records.append('{},{}'.format(name, url))
    khandy.save_list(os.path.join(dst_dir_root, 'failed_records.txt'), failed_records)
    
    