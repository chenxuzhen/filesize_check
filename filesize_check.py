# the script was written to loop through a folder check sizes of all files
# multi-threading is turned on to speed up process

import os
import threading
# from PIL import Image
from sys import argv
import time

def filewrite(filepath):
    with open('filesize_list.txt', 'a') as f:
        f.write(os.path.abspath(filepath))
        f.write('\n')

def sizeCheck(files):
    thr_name = threading.current_thread().name
    print(f'{thr_name} is processing {len(files)} files')
    for file in files:
        file_path = os.path.join(root,file)
        # file_path = os.path.abspath(file)
        filesize = os.stat(file_path).st_size/1024/1024
        if filesize > 3072:
            print(f'threading: {file}, {file_path}, {int(filesize)}MB')
            # lock.acquire()
            filewrite(file_path)
            # lock.release()
            
def split_files(file_list, split_num):
    thread_list = []
    # list size each thread has to process
    list_size = (len(file_list) // split_num) if (len(file_list) % split_num == 0) else ((len(file_list) // split_num) + 1)
    print(f'num of files to check {list_size}')
    # start thread
    for i in range(split_num):
        # get url that current thread need to process
        file_list_split = file_list[
                         i * list_size:(i + 1) * list_size if len(file_list) > (i + 1) * list_size else len(file_list)]
        thread = threading.Thread(target=sizeCheck, args=(file_list_split,))
        thread.setName("Thread" + str(i))
        thread_list.append(thread)
        # start in thread
        thread.start()
        # print(thread.getName() + "started")
    # combine at the end of the job
    for _item in thread_list:
        _item.join()
        
if __name__ == "__main__":
    t1 = time.time()
    thread_num = 6
    lock = threading.Lock()
    print("add the directory where you want to check filesizes or leave it to default:") 
    if len(argv) > 1:
        dirs_to_check = [','.join(argv[i]) for i in range(len(argv))]        
        print(f'num of folders to check: {dirs_to_check}  {len(dirs_to_check)}')
    else:
        dirs_to_check = ['D:\\', 'E:\\', 'F:\\', 'G:\\']
    file_list_ = []
    for dir_to_check in dirs_to_check:      
        print(f'dir_to_check {dir_to_check}')
        for root, dirs, files in os.walk(dir_to_check):
            # print(root, dirs, files, len(files))
            for i in files:
                file_list_.append(''.join(root + '\\'+ i))
    print(f'num of files to scan: {len(file_list_)}')
    split_files(file_list_, thread_num) # thread_num
    t2 = time.time()
    print(f'time lapsed: {t2-t1}, num of threads used: {thread_num}')
            
         
