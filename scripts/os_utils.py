#!/usr/bin/env python3


import glob
import os


def findByExtension(path, extension):
    return glob.glob(f"{os.path.abspath(path)}/**/*.{extension}", recursive=True)


if __name__ == "__main__":
    print("findByExtension:")
    print(findByExtension(os.getcwd(),'*'))