#coding=utf-8
import os
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


def write_list_file(filename, written_list, append_break=True):
    with open(filename, 'w', encoding='utf8') as f:
        if append_break:
            for item in written_list:
                f.write(item + '\n')
        else:
            for item in written_list:
                f.write(item)
                
                
def get_id_func(record):
    return record.split(',')[0]
    

def _get_length(obj):
    if hasattr(obj, '__len__'):
        return len(obj)
    else:
        return 0
    
    
def get_max_length_item(list_obj):
    assert isinstance(list_obj, (tuple, list))
    assert len(list_obj) > 0
    
    max_index = 0
    max_length = _get_length(list_obj[0])
    for k, item in enumerate(list_obj[1:], 1):
        if len(item) > max_length:
            max_length = max(_get_length(item), max_length)
            max_index = k
    return list_obj[max_index]


def keep_one_record(class_dict):
    new_class_dict = {}
    for key, vals in class_dict.items():
        if len(vals) == 1:
            new_class_dict[key] = vals
        elif len(vals) > 1:
            new_class_dict[key] = [get_max_length_item(vals)]
    return new_class_dict


def create_class_dict_by_name(name_list, func=None):
    func = func or (lambda x: x)
    class_dict = {}
    for name in name_list:
        label = func(name)
        class_dict.setdefault(label, []).append(name)
    return class_dict


def sort_class_dict(class_dict, reverse=False):
    sorted_keys = sorted(class_dict.keys(), reverse=reverse)
    sorted_dict = OrderedDict()
    for key in sorted_keys:
        sorted_dict[key] = class_dict[key]
    return sorted_dict


if __name__ == '__main__':
    root_dir = r'F:\_Datasets_self\CelebNames\names'
    for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        filename = os.path.join(root_dir, 'star_chinese_{}.txt'.format(char))
        print(filename)
        if not os.path.exists(filename):
            continue
        records = parse_list_file(filename)
        class_dict = create_class_dict_by_name(records, get_id_func)
        class_dict = keep_one_record(class_dict)
        class_dict = sort_class_dict(class_dict)
        new_records = sum(class_dict.values(), [])
        write_list_file(os.path.basename(filename), new_records)
        
        