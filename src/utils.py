from sys import argv
from os import makedirs
from os.path import exists, dirname, realpath, join

APP_DIR: str = dirname(realpath(argv[0])).removesuffix('/src')

def read(filepath: str) -> str | None:
  filepath = join(APP_DIR, filepath)

  if not exists(filepath):
    return None
  
  with open(filepath, 'r') as file:
    return file.read()

def write(filepath: str, content: str) -> bool:
  filepath = join(APP_DIR, filepath)
  folder_path: str = "/".join(filepath.split('/')[:-1])
  
  if not exists(folder_path):
    makedirs(folder_path, exist_ok=True)
  
  with open(filepath, 'w') as file:
    file.write(content)
  
  return True
