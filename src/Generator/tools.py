from os import path as p
from os import makedirs

def set_directory(path:str): makedirs(path,0o777) if not p.exists(path) else print(path + 'directory already exist')
    
def get_file(path:str): return open(path,"x") if not p.exists(path) else open(path,"a")