from collections import defaultdict
import json
import os

def getFileName(lists, directory):
  object = os.scandir(directory)
  for n in object :
    if n.is_file():
      lists[directory.path].append(n.name)
  object.close()

def get_lists():
  path_of_the_directory = r'C:\Users\nano\Documents\OCR\listas'
  object = os.scandir(path_of_the_directory)
  print("Files and Directories in '% s':" % path_of_the_directory)
  lists=defaultdict(list)
  for n in object :
    if n.is_dir():
      getFileName(lists,n)
  object.close()
  return lists
def getCover(path):
  return path+'\\'+'cover.jpg'