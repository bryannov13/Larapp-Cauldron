from os import path as p
from os import makedirs

def set_directory(path): makedirs(path,0o777) if not p.exists(path) else print(path + 'directory already exist')
    
def get_file(path): return open(path,"x") if not p.exists(path) else open(path,"a")