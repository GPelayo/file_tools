import os
import hashlib
import tqdm
import datetime
import zlib
import shutil


class Hasher:
    elapsed = []
    byte_size = 65536

    def sha1_hash(self, filepath):
        return self.hashlib_hash(filepath, hashlib.sha1())

    def crc32_hash(self, filepath):
        with open(filepath, 'rb') as crcfile:
            start_time = datetime.datetime.now()
            file_data = crcfile.read(self.byte_size)
            last = 0
            while file_data:
                last = zlib.crc32(file_data, last)
                file_data = crcfile.read(self.byte_size)
        hash_code = "%X" % (last & 0xFFFFFFFF)
        self.elapsed = (datetime.datetime.now() - start_time).total_seconds()
        return hash_code

    def md5_hash(self, filepath):
        return self.hashlib_hash(filepath, hashlib.md5())

    def hashlib_hash(self, filepath, func):
        with open(filepath, 'rb') as zfile:
            start_time = datetime.datetime.now()
            size = self.byte_size
            hasher = func
            bf = zfile.read(size)
            while len(bf) > 0:
                hasher.update(bf)
                bf = zfile.read(size)
        hash_code = hasher.hexdigest()
        self.elapsed = (datetime.datetime.now() - start_time).total_seconds()
        return hash_code

    def single_chunk(self, filepath):
        with open(filepath, 'rb') as zfile:
            start_time = datetime.datetime.now()
            hasher = hashlib.md5()
            hash_code = hasher.hexdigest(zfile)
        self.elapsed = (datetime.datetime.now() - start_time).total_seconds()
        return hash_code


def find_dupes(search_directory):
    hash_dict = {}
    file_lst = []
    dupes = {}
    for direc in os.walk(search_directory):
        for fle in direc[2]:
            file_lst.append((os.path.join(direc[0], fle), fle))

    for file_dir, nm_dir in tqdm.tqdm(file_lst):
        h = Hasher()
        file_hash = h.crc32_hash(file_dir)
        if file_hash in hash_dict.keys():
            name = os.path.basename(file_dir)
            if name.split('.')[1] != "lnk":
                dupes[file_hash] = hash_dict[file_hash]
        else:
            hash_dict[file_hash] = file_dir

    return dupes


def move_files(filename_list, dupe_folder):
    for directory in filename_list:
        shutil.move(directory, os.path.join(dupe_folder, directory))


def find_dupes_by_name(search_directory):
    names = []

    for direc in os.walk(search_directory):
        for fle in direc[2]:
            if fle in names:
                print(os.path.join(direc[0], fle))
            else:
                names.append(fle)


def check_exists(root_dir, hash_list, result_file):
    file_lst = []

    for direc in os.walk(root_dir):
        for fle in direc[2]:
            file_lst.append((os.path.join(direc[0], fle), fle))

    for file_dir, nm_dir in tqdm.tqdm(file_lst):
        h = Hasher()
        file_hash = h.crc32_hash(file_dir)
        with open(result_file, 'a') as result:
            if file_hash in hash_list:
                result.write("{}\n".format(file_dir))


def save_file_hashes(search_dir, output_dir, size_list_path=None, ):
    size_list = {}
    file_lst = []
    try:
        if size_list_path:
            with open(size_list_path, 'r+') as size_file:
                size_list = {s.split(',')[0].strip(): ",".join(s.split(',')[1:]).strip() for s in size_file.readlines()}
    except FileNotFoundError:
        pass

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
