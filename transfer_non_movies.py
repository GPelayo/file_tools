import os
import shutil


def transfer_all_files_with_type(root_folder, dst_dir, type_extension):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    for direc in os.walk(root_folder):
        for fle in direc[2]:
            file_name = os.path.join(direc[0], fle)
            f_splt = file_name.split('.')
            if len(f_splt) > 1:
                if f_splt[-1] == type_extension:
                    name = os.path.basename(file_name)
                    dest_name = os.path.join(os.path.join(dst_dir, name))
                    copy_int = 1
                    while True:
                        try:
                            shutil.move(file_name, os.path.join(dest_name))
                            break
                        except FileExistsError:
                            dest_name = dest_name + " ({})".format(copy_int)
                            copy_int += 1
                        except PermissionError:
                            print(file_name)
                            break


def transfer_ghosts(root_folder, dst_dir):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)
    for direc in os.walk(root_folder):
        for fle in direc[2]:
            file_name = os.path.join(direc[0], fle)
            name = os.path.basename(file_name)
            if name[0] == ".":
                dest_name = os.path.join(os.path.join(dst_dir, name))
                safely_move(dest_name, os.path.join(dst_dir, name))


def transfer_empty_dirs(root_folder, dst_dir):
    if not os.path.isdir(dst_dir):
        os.makedirs(dst_dir)

    for direc in os.walk(root_folder):
        if len(direc[2]) + len(direc[1]) == 0:
            file_name = direc[0]
            dest_name = os.path.basename(file_name)
            print(os.path.join(dest_name))

            dest_path = os.path.join(dst_dir, dest_name)
            safely_move(file_name, dest_path)


def safely_move(file_name, dest_path):
    real_path = dest_path
    copy_int = 1
    while True:
        if os.path.isdir(real_path):
            copy_int += 1
            real_path = dest_path + " [{}]".format(copy_int)
        else:
            try:
                shutil.move(file_name, real_path)
                break
            except PermissionError:
                print(file_name)
                break


def get_all_types(root_folder):
    types = set()
    for direc in os.walk(root_folder):
        for fle in direc[2]:
            file_name = os.path.join(direc[0], fle)
            x, ext = os.path.splitext(file_name)

            if not ext:
                print(file_name)
            types.add(ext.lower())
    print(types)



