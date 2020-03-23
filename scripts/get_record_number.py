#coding=utf-8
import os
import glob


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
    for k, filename in enumerate(filenames):
        if os.path.exists(filename):
            records += parse_list_file(filename)
    return records


def get_record_number(records):
    number = 0
    for record in records:
        record = record.strip()
        if record == '':
            pass
        elif record.startswith('#'):
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
    src_dir = r'F:\_Datasets_self\CelebNames\names'
    tags = ['businessman_chinese', 'businessman_japan_korea', 'businessman_others', 
            'liberal_arts_chinese', 'liberal_arts_japan_korea',
            'politican_chinese', 'politican_japan_korea_vn_sg', 'politican_others',
            'scientist_chinese', 'scientist_others',
            'star_chinese', 'star_japan_korea', 'star_others']
    all_records = []
    for tag in tags:
        filenames = glob.glob(os.path.join(src_dir, '{}*.txt'.format(tag)))
        records = get_all_records(filenames)
        print('{:<30}: {}'.format(tag, get_record_number(records)))
        all_records += records
    print('{:<30}: {}'.format('total', get_record_number(all_records)))
    print('{:<30}: {}'.format('total with desc', get_record_number_with_desc(all_records)))
    
    