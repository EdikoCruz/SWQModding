#!/usr/bin/env python3

"""
.impak files are zip files renamed.

when compressing, will search for a *.impak.lock files.
when decompressing, will create a fileName.impak.lock file.
"""


import os
import sys
import zipfile


def decompress(filePath):
    lockPath = f"{filePath}.lock"
    dir = os.path.dirname(filePath)

    with zipfile.ZipFile(filePath, "r") as file:
        with open(lockPath, "w") as lock:
            for name in file.namelist():
                lock.write(f"{name}\r\n")

        file.extractall(dir)

    os.remove(filePath)

def compress(lockPath):
    filePath = lockPath[:-5]
    dir = os.path.dirname(filePath)
    with open(lockPath, "r") as lock:
        fileList = lock.readlines()
        with zipfile.ZipFile(filePath, "w") as file:
            for line in fileList:
                relativeFilePath = line.strip()
                absoluteFilePath = os.path.join(dir, relativeFilePath)
                file.write(absoluteFilePath, relativeFilePath)
                os.remove(absoluteFilePath)
    os.remove(lockPath)

def __getFilesPathFrom(dirPath):
    filesPath = []
    for fileName in os.listdir(dirPath):
        filePath = os.path.join(dirPath, fileName)
        if os.path.isfile(filePath):
            filesPath.append(filePath)
        else:
            filesPath.extend(__getFilesPathFrom(filePath))
    return filesPath


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: impakFile.py <impakFilePath|impakLockFilePath>")
        exit(1)

    path = os.path.abspath(sys.argv[1])
    if not os.path.isfile(path):
        print(f"{path} is not a file")
        exit(1)
    
    if not (path.endswith(".impak") or path.endswith(".impak.lock")):
        print("must be a .impak or .impak.lock file")
        exit(1)

    if path.endswith(".impak"):
        decompress(path)
        print(f"{path} decompressed")
    else:
        compress(path)
        print(f"{path} compressed")
