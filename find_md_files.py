import sys
import os
from os import listdir, getcwd, chdir, makedirs
from os.path import isdir, isfile, join, expanduser
from shutil import copyfile

list_of_md_files = []
file_matches = 0
name_matches = 0

def find_md_files(sourcePath):
    for item in listdir(sourcePath):
        itemPath = join(sourcePath,item)
        if isfile(itemPath) and item.endswith(".md"):
            original_name = item.replace('_zh_CN','')
            list_of_md_files.append(original_name)

        if isdir(itemPath):
            find_md_files(itemPath)

def find_md_matches(sourcePath):
    global file_matches
    global name_matches

    for item in listdir(sourcePath):
        itemPath = join(sourcePath,item)
        if isfile(itemPath) and item.endswith(".md"):
            counter = 0
            with open(itemPath) as f:
                lines = f.readlines()
                for line in lines:
                    for md_file in list_of_md_files:
                        md_name = md_file.replace('.md','')
                        if md_file in line:
                            print(md_file + " md file name match in " + itemPath + " at line " + str(counter))
                            print(line)
                            file_matches += 1
                        elif md_name in line:
                            if counter != 0:
                                print(md_name + " ref name match found in " + itemPath + " at line " + str(counter))
                                print(line)
                                name_matches += 1
                    counter += 1

        if isdir(itemPath):
            find_md_matches(itemPath)

path = "."

find_md_files(path)
print(list_of_md_files)
find_md_matches(path)
print(str(file_matches) + " md file matches found.")
print(str(name_matches) + " name matches found.")