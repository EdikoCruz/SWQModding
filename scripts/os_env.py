#!/usr/bin/env python3


import os

class Env:
    def __init__(self, path=None):
        self.NAMESPACE = "SWQModding"

        if not path:
            path = os.getcwd()

        self.__loadFromFile(self.__getEnvFilePath(path))

    def get(self, key):
        return os.environ[self.__formatKey(key)]
    
    def keys(self):
        keys = []
        for key in os.environ.keys():
            if key.startswith(self.NAMESPACE):
                keys.append(self.__unformatKey(key))
        return keys
    
    def __formatKey(self, key):
        return f"{self.NAMESPACE}_{key}"

    def __unformatKey(self, key):
        return key[len(self.NAMESPACE) + len("_"):]
    
    def __loadFromFile(self, path):
        with open(path, "r") as file:
            for line in file.readlines():
                line = line.strip()

                if line.startswith("#") or not line:
                    continue

                key, value = line.split("=", 1)
                os.environ[self.__formatKey(key)] = value

    def __getEnvFilePath(self, dirPath):
        envFilePath = os.path.join(dirPath, ".env")

        if not os.path.isfile(envFilePath):
            print("WARNING: .env not found")
            print("WARNING: trying .env.default")
            envFilePath = f"{envFilePath}.default"

        if not os.path.isfile(envFilePath):
            raise RuntimeError(f"ERROR: {envFilePath} not found")

        return envFilePath


if __name__ == "__main__":
    env = Env()
    for key in env.keys():
        print(f"key: {key}, value: {env.get(key)}")
