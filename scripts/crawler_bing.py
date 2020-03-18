#coding=utf-8
import os
import time
import urllib
import requests
import urllib.request
from bs4 import BeautifulSoup


COUNT_PER_PAGE = 35

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
}


def get_image_urls(keyword, first):
    url = ("http://cn.bing.com/images/async?q={word}&first={first}&count={count}&relp={count}"
           "&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0")
    url = url.format(word=urllib.request.quote(keyword), first=first, count=COUNT_PER_PAGE)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    url_list = []
    for item in soup.select('.mimg'):
        link = item.attrs['src']
        # NB: 
        url_list.append(link.split('&')[0])

    return url_list

    
def download_images(keyword, last, dst_dir, first=1):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    current_first = first
    image_name_first = (first - 1) * COUNT_PER_PAGE + 1
    while current_first < last:
        url_list = get_image_urls(keyword, current_first)
        
        for url in url_list:
            time.sleep(1)
            
            print('[{}] {}'.format(image_name_first, url))
            fullname = os.path.join(dst_dir, 'bing_{}_{:05}.jpg'.format(keyword, image_name_first))
            try:
                with open(fullname, "wb") as f:
                    f.write(requests.get(url, timeout=30).content)
            except:
                pass
            image_name_first += 1
        current_first += COUNT_PER_PAGE
        
        
def parse_list_file(filename, prefix='', offset=0, max_num=0):
    lines = []
    with open(filename, 'r') as f:
        for _ in range(offset):
            f.readline()
        for k, line in enumerate(f):
            if max_num > 0 and k >= max_num:
                break
            lines.append(prefix + line.rstrip())
    return lines

    
if __name__ == '__main__':
    keywords = parse_list_file('tbd_names.txt')
    keywords = [item.split(',')[0] for item in keywords]
    dst_dirs = [os.path.join('images_bing', item) for item in keywords]
    for k, (keyword, dst_dir) in enumerate(zip(keywords, dst_dirs)):
        print('[{}/{}] {}'.format(k+1, len(keywords), keyword))
        download_images(keyword, 200, dst_dir)
        
        
