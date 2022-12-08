import sys

from os import listdir, getcwd, chdir, makedirs
from os.path import isdir, isfile, join, expanduser, normpath, basename, dirname
from shutil import copyfile

import re

md_files = []
ref_targets = []
source_path = "source"
output_path = "zh_CN"
md_matches = 0
md_references = 0

def fix_toctree_indents(lines):
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

def fix_doxygen_targets(lines):
    new_lines = []
    counter = 0
    for line in lines:
        new_line = line
        if line.endswith('}\n') and '{#' in line:
            target_pieces = line.split('{')
            target = target_pieces[-1].replace('}\n','')
            target = target.replace('#','')
            ref_targets.append(target)
            new_target = target + '_zh_CN'
            #print('    target (line ' + str(counter) + '): ' + target)
            #print(new_target)
            new_line = new_line.replace(target,new_target)
        new_lines.append(new_line)
        counter += 1
    return new_lines

def fix_target_refs(lines):
    new_lines = []
    for line in lines:
        new_line = line
        for ref in ref_targets:
            if "@ref " + ref in line:
                new_line = line.replace("@ref " + ref, "@ref " + ref + "_zh_CN")
                #print("ref (" + ref + "): " + new_line)
        new_lines.append(new_line)
    return new_lines

def fix_filename_refs(localpath,lines):
    global md_matches
    global md_references

    new_lines = []
    for line in lines:
        new_line = line
        result = re.findall(r']\((.*?)\)', line)
        for r in result:
            if r.endswith('.md') and not r.startswith("http"):
                md_references += 1
                file_ref_rel_path = normpath(join(localpath,r))
                base = basename(r)
                newbase = base.replace('.md','')
                newbase = newbase + '_zh_CN.md'
                file_ref_rel_path_zh_CN = file_ref_rel_path.replace(base,newbase)
                if isfile(file_ref_rel_path_zh_CN):
                    md_matches += 1
                    new_line = line.replace(base,newbase)
                    #print("Match relative path: " + file_ref_rel_path)
                    #print("    newline: " + new_line)
                else:
                    print("    " + r)
        new_lines.append(new_line)
    return new_lines

def first_pass(sourcePath,outputPath):
    for item in listdir(sourcePath):
        itemPath = join(sourcePath,item)
        outputItemPath = join(outputPath,item)
        if isfile(itemPath) and item.endswith(".md"):
            corrected_lines = []
            md_files.append(item)
            with open(itemPath) as f:
                stuff = f.readlines()
                # make changes to content
                # corrected_lines = fix_toctree_indents(stuff)
                corrected_lines = fix_doxygen_targets(stuff)
            newFilePath = join(outputPath,item.replace('.md','')+'_zh_CN.md')
            makedirs(dirname(newFilePath), exist_ok=True)
            with open(newFilePath,'w') as f2:
                for line in corrected_lines:
                    f2.write(line)

        if isdir(itemPath):
            first_pass(itemPath,outputItemPath)

def second_pass(dirPath):
    for item in listdir(dirPath):
        itemPath = join(dirPath,item)
        if isfile(itemPath) and item.endswith(".md"):
            corrected_lines = []
            with open(itemPath) as f:
                stuff = f.readlines()
                # make changes to content
                print(itemPath)
                corrected_lines = fix_target_refs(stuff)
                corrected_lines = fix_filename_refs(dirPath,corrected_lines)
            with open(itemPath,'w') as f2:
                for line in corrected_lines:
                    f2.write(line)

        if isdir(itemPath):
            second_pass(itemPath)

first_pass(source_path,output_path)
second_pass(output_path)
print("Number of markdown references: " + str(md_references))
print("Number of markdown reference matches: " + str(md_matches))