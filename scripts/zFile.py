#!/usr/bin/env python3

"""
.z files is a single file zlib compressed with a 4 bits header, the header has
the uncompressed file's size.

when compressing, will search for a *.z.lock files.
when decompressing, will create a fileName.z.lock file.
"""


import os
import sys
import zlib


def decompress(filePath):
    inFilePath = filePath
    outFilePath = filePath[:-2]

    open(f"{inFilePath}.lock", 'a').close()

    with open(inFilePath, "rb") as inFile:
        with open(outFilePath, "wb") as outFile:
            # skipping header
            inFile.seek(4)
            # adding file
            compressed_data = inFile.read()
            decompressed_data = zlib.decompress(compressed_data)
            outFile.write(decompressed_data)

    inFileSizeAsBytes = __getSizeFromCompressedFile(inFilePath)
    inFileSize = __sizeFromBytesToInt(inFileSizeAsBytes)
    outFileSize = __getSizeFromUncompressedFile(outFilePath)

    if (inFileSize != outFileSize):
        print(f"WARNING: header mismatch for {inFilePath}")
        print(f".z file's header : {inFileSize}")
        print(f"dest file's header: {outFileSize}")
    
    os.remove(inFilePath)

def compress(lockPath):
    inFilePath = lockPath[:-7]
    outFilePath = f"{inFilePath}.z"

    with open(inFilePath, "rb") as inFile:
        with open(outFilePath, "wb") as outFile:
            # adding header        
            inFileSize = __getSizeFromUncompressedFile(inFilePath)
            inFileSizeAsBytes = __sizeFromIntToBytes(inFileSize)
            outFile.write(inFileSizeAsBytes)
            # adding file
            uncompressedData = inFile.read()
            compressedData = zlib.compress(uncompressedData)            
            outFile.write(compressedData)
    os.remove(lockPath)
    os.remove(inFilePath)


# size --------
def __sizeFromIntToBytes(size):
    return size.to_bytes(4, "little")

def __sizeFromBytesToInt(size):
    return int.from_bytes(size, "little")

def __getSizeFromUncompressedFile(filePath):
    return os.path.getsize(filePath)

def __getSizeFromCompressedFile(filePath):
    size = None
    with open(filePath, "rb") as inFile:
        size = inFile.read(4)
    return size

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage: zFile.py filePath")
        exit(1)

    path = os.path.abspath(sys.argv[1])

    if not os.path.isfile(path):
        print(f"{path} is not a file")
        exit(1)
    
    if not (path.endswith(".z") or path.endswith(".z.lock")):
        print("must be a .z or .z.lock file")
        exit(1)

    if path.endswith(".z"):
        decompress(path)
        print(f"{path} decompressed")
    else:
        compress(path)
        print(f"{path} compressed")
