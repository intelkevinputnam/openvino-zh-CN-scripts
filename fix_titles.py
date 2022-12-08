import sys
import os
from os import listdir, getcwd, chdir, makedirs
from os.path import isdir, isfile, join, expanduser
from shutil import copyfile

def fix_files(sourcePath):
    for item in listdir(sourcePath):
        itemPath = join(sourcePath,item)
        if isfile(itemPath) and item.endswith(".md"):
            title = ''
            lines = []
            with open(itemPath) as f:
                lines = f.readlines()
                if lines[0].endswith('}\n'):
                    title_pieces = lines[0].split('{')
                    title = title_pieces[-1].replace('}\n','')
                    print("filename: " + itemPath)
                    print("old title: " + title)
                    print("new title: " + title + "_zh_CN")
                    lines[0] = lines[0].replace(title,title +"_zh_CN")
                    print(lines[0])

            with open(itemPath,'w') as f2:
                for line in lines:
                    f2.write(line)

        if isdir(itemPath):
            fix_files(itemPath)

path = "."

fix_files(path)
