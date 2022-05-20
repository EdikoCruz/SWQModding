import os
import zipfile
import zlib

from os_utils import findByExtension


"""
.impak files are zip files renamed.
"""
class ImpakHandler:
    def __init__(self, path):
        self.isFile = os.path.isfile(path)
        self.isDir = os.path.isdir(path)
        self.path = path

    def unpackAll(self):
        if not self.isDir:
            return

        for path in findByExtension(self.path, 'impak'):
            self.__unpack(path)
    
    def unpack(self):
        if not self.isFile:
            return

        if not self.path.endswith('.impak'):
            return

        self.__unpack(self.path)

    def __unpack(self, path):
        lockPath = f"{path}.lock"
        dir = os.path.dirname(path)

        with zipfile.ZipFile(path, "r") as file:
            with open(lockPath, "w") as lock:
                for name in file.namelist():
                    lock.write(f"{name}\r\n")

            file.extractall(dir)

        os.remove(path)

    def packAll(self):
        if not self.isDir:
            return

        for path in findByExtension(self.path, 'impak.lock'):
            self.__pack(path)

    def pack(self):
        if not self.isFile:
            return

        if not self.path.endswith('.impak.lock'):
            return

        self.__pack(self.path)
    
    def __pack(self, path):
        filePath = path[:-5]
        dir = os.path.dirname(filePath)

        with open(path, "r") as lock:
            fileList = lock.readlines()
            with zipfile.ZipFile(filePath, "w") as file:
                for line in fileList:
                    relativeFilePath = line.strip()
                    absoluteFilePath = os.path.join(dir, relativeFilePath)
                    file.write(absoluteFilePath, relativeFilePath)
                    os.remove(absoluteFilePath)

        os.remove(path)


"""
.z files is a single file zlib compressed with a 4 bits header, the header has
the uncompressed file's size.
"""
class ZHandler:
    def __init__(self, path):
        self.isFile = os.path.isfile(path)
        self.isDir = os.path.isdir(path)
        self.path = path

    def unpackAll(self):
        if not self.isDir:
            return

        for path in findByExtension(self.path, 'z'):
            self.__unpack(path)

    def unpack(self):
        if not self.isFile:
            return

        if not self.path.endswith('.z'):
            return

        self.__unpack(self.path)

    def __unpack(self, path):
        inFilePath = path
        outFilePath = path[:-2]

        open(f"{inFilePath}.lock", 'a').close()

        with open(inFilePath, "rb") as inFile:
            with open(outFilePath, "wb") as outFile:
                # skipping header
                inFile.seek(4)
                # adding file
                compressed_data = inFile.read()
                decompressed_data = zlib.decompress(compressed_data)
                outFile.write(decompressed_data)

        inFileSizeAsBytes = self.__getSizeFromCompressedFile(inFilePath)
        inFileSize = self.__sizeFromBytesToInt(inFileSizeAsBytes)
        outFileSize = self.__getSizeFromUncompressedFile(outFilePath)

        if (inFileSize != outFileSize):
            print(f"WARNING: header mismatch for {inFilePath}")
            print(f".z file's header : {inFileSize}")
            print(f"dest file's header: {outFileSize}")

        os.remove(inFilePath)

    def packAll(self):
        if not self.isDir:
            return

        for path in findByExtension(self.path, 'z.lock'):
            self.__pack(path)
    
    def pack(self):
        if not self.isFile:
            return

        if not self.path.endswith('.z.lock'):
            return

        self.__pack(self.path)
    
    def __pack(self, path):
        inFilePath = path[:-7]
        outFilePath = f"{inFilePath}.z"

        with open(inFilePath, "rb") as inFile:
            with open(outFilePath, "wb") as outFile:
                # adding header        
                inFileSize = self.__getSizeFromUncompressedFile(inFilePath)
                inFileSizeAsBytes = self.__sizeFromIntToBytes(inFileSize)
                outFile.write(inFileSizeAsBytes)
                # adding file
                uncompressedData = inFile.read()
                compressedData = zlib.compress(uncompressedData)            
                outFile.write(compressedData)

        os.remove(path)
        os.remove(inFilePath)

    def __sizeFromIntToBytes(self, size):
        return size.to_bytes(4, "little")

    def __sizeFromBytesToInt(self, size):
        return int.from_bytes(size, "little")

    def __getSizeFromUncompressedFile(self, path):
        return os.path.getsize(path)

    def __getSizeFromCompressedFile(self, path):
        size = None
        with open(path, "rb") as inFile:
            size = inFile.read(4)
        return size
