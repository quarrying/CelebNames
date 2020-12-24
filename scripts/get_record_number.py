#coding=utf-8
import os
import glob
from collections import OrderedDict


def parse_list_file(filename, prefix='', offset=0, max_num=0):
    lines = []
    with open(filename, 'r', encoding='utf8') as f:
        for _ in range(offset):
            f.readline()
        for k, line in enumerate(f):
            if max_num > 0 and k >= max_num:
                break
            lines.append(prefix + line.rstrip())
    return lines
  

def get_all_records(filenames):
    records = []
    for _, filename in enumerate(filenames):
        if os.path.exists(filename):
            records += parse_list_file(filename)
    return records


def get_record_number(records):
    number = 0
    for record in records:
        if record == '':
            pass
        elif record.startswith('#'):
            pass
        elif record.startswith(' '):
            pass
        else:
            number += 1
    return number


def get_record_number_with_desc(records):
    number = 0
    for record in records:
        record = record.strip()
        if record == '':
            pass
        elif record.startswith('#'):
            pass
        else:
            parts = record.split(',')
            if len(parts) > 1 and len(parts[1]) > 1:
                number += 1
    return number


if __name__ == '__main__':
    parent_dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_dir = os.path.join(parent_dirname, 'names')

    tags_dict = OrderedDict()
    tags_dict['chinese'] = ['businessman_chinese',  
                            'hot_chinese',
                            'liberal_arts_chinese',
                            'politican_chinese', 
                            'scientist_chinese',
                            'star_chinese']
    tags_dict['east-asian'] = ['businessman_east_asian',  
                               'liberal_arts_east_asian',
                               'politican_east_asian', 
                               'scientist_east_asian',
                               'star_east_asian']
    tags_dict['others'] = ['businessman_others',  
                           'politican_others',
                           'scientist_others',
                           'star_others']
    all_records = []
    for subdir, tags in tags_dict.items():
        for tag in tags:
            filenames = glob.glob(os.path.join(src_dir, subdir, '{}*.txt'.format(tag)))
            records = get_all_records(filenames)
            print('{:<30}: {}'.format(tag, get_record_number(records)))
            all_records += records
        
    print('{:<30}: {}'.format('total', get_record_number(all_records)))
    print('{:<30}: {}'.format('total with desc', get_record_number_with_desc(all_records)))
    
    