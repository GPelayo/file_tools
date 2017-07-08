import os
import tqdm
from dupe_checker import Hasher
import re


def get_hash_dict(cache_filename):
    try:
        if cache_filename:
            with open(cache_filename, 'r+') as size_file:
                return {s.split(',')[0].strip(): ",".join(s.split(',')[1:]).strip() for s in size_file.readlines()}
    except FileNotFoundError:
        print("No file named {}".format(cache_filename))
    return {}


def save_file_hashes(search_dir, output_dir, initial_cache_path=None, ):
    size_list = get_hash_dict(initial_cache_path)
    file_lst = []

    for direc in os.walk(search_dir):
        for fle in direc[2]:
            file_lst.append((os.path.join(direc[0], fle), fle))

    for file_dir, nm_dir in tqdm.tqdm(file_lst):
        h = Hasher()
        identifier = h.crc32_hash(file_dir)
        if identifier not in size_list.keys():
            size_list[identifier] = file_dir

    with open(output_dir, 'w+') as cache_file:
        cache_file.write("\n".join(["{},{}".format(s, size_list[s]) for s in size_list]))


def remove_tags(filename):
    tag_less = filename
    brack_re = re.compile('\[.*\](?=\.[a-z0-9]{3,})')
    if re.findall(brack_re, filename):
        for target in re.findall(brack_re, filename):
            tag_less = tag_less.replace(' ' + target + ' ', '').replace(' ' + target, '').replace(target + ' ', '').replace(target, '')

    return tag_less


