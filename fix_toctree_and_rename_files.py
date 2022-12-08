import sys

from os import listdir, getcwd, chdir, makedirs
from os.path import isdir, isfile, join, expanduser
from shutil import copyfile

def fix_toctree(lines):
    new_lines = []
    sphinx_directive = False
    tab = ''
    for line in lines:
        if line.startswith('@sphinxdirective'):
            sphinx_directive = True
        elif sphinx_directive and line.startswith('.. toctree::'):
            new_lines.append(line)
            tab = '    '
            continue
        elif sphinx_directive and '@endsphinxdirective' in line:
            sphinx_directive = False
            tab = ''
        new_lines.append(tab+line)
    return new_lines

def find_files(sourcePath):
    for item in listdir(sourcePath):
        itemPath = join(sourcePath,item)
        if isfile(itemPath) and item.endswith(".md"):
            corrected_lines = []
            with open(itemPath) as f:
                stuff = f.readlines()
                corrected_lines = fix_toctree(stuff)
            newFilePath = join(sourcePath,item.replace('.md','')+'_zh_CN.md')
            with open(newFilePath,'w') as f2:
                for line in corrected_lines:
                    f2.write(line)

        if isdir(itemPath):
            find_files(itemPath)

path = "2022.2_zh-CN_md"

find_files(path)