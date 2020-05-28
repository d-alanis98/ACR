import pathlib

class FileManager:

    DEFAULT_BYTES = 1024

    def __init__(self, fileName, filePath):
        self.file = None
        self.fileName = fileName
        self.filePath = filePath

    
    def openFile(self, mode = 'rb'):
        self.file = open(self.filePath, mode)


    def getFileBytes(self):
        return self.file.read(self.DEFAULT_BYTES)

    def closeFile(self):
        self.file.close()


    def processFile(self):
        self.openFile()


