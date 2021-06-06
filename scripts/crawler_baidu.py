import os
import re
import json
import time
import urllib
import urllib.request

import requests


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
}


def get_image_urls(keyword, num_pages):
    """
    rn 一页包含的图片数量，最多60
    pn 第多少张
    word 搜索的关键字
    """
    url = ("https://image.baidu.com/search/acjson?tn=resultjson_com" +
        "&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1" +
        "&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={word}&s=&se=" +
        "&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn={num_pages}" +
        "&rn=30&gsm=1e00000000001e&1490169411926=")
    url = url.format(word=urllib.request.quote(keyword), num_pages=num_pages)
    url_list = []
    try:
        r = requests.get(url, headers=headers)
        content = re.sub(r'\\(?![/u"])', r"\\\\", r.text)
        data = json.loads(content)['data']
        
        for k, item in enumerate(data):
            thumb_url = item.get('thumbURL')
            if thumb_url:
                url_list.append(thumb_url)
    except:
        pass
    return url_list

    
def download_images(keyword, num_pages, dst_dir):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    current_page, counter = 0, 0
    while current_page < num_pages:
        url_list = get_image_urls(keyword, current_page)
        current_page += 30
        
        for url in url_list:
            time.sleep(1)
            counter += 1
            print('[{}] {}'.format(counter, url))
            fullname = os.path.join(dst_dir, 'baidu_{}_{:05}.jpg'.format(keyword, counter))
            try:
                r = requests.get(url, timeout=30)
                with open(fullname, "wb") as f:
                    f.write(r.content)
            except:
                pass
            
            
def load_list(filename, encoding='utf-8', start=0, stop=None):
    assert isinstance(start, int) and start >= 0
    assert (stop is None) or (isinstance(stop, int) and stop > start)
    
    lines = []
    with open(filename, 'r', encoding=encoding) as f:
        for _ in range(start):
            f.readline()
        for k, line in enumerate(f):
            if (stop is not None) and (k + start > stop):
                break
            lines.append(line.rstrip('\n'))
    return lines

    
if __name__ == '__main__':
    list_filename = 'NAMES.txt'
    dst_dir = 'images'
    num_images = 200

    keywords = load_list(list_filename)
    keywords = [item.split(',')[0] for item in keywords]
    dst_dirs = [os.path.join(dst_dir, item) for item in keywords]
    for k, (keyword, dst_dir) in enumerate(zip(keywords, dst_dirs)):
        print('[{}/{}] {}'.format(k+1, len(keywords), keyword))
        download_images(keyword, num_images, dst_dir)
        
        
