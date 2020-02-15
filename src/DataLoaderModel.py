from PyQt5.QtCore import pyqtSignal, QObject
import unittest
import os
import re
from tools.generalTools import *


class DataFile(QObject):
    def __init__(self, filepath):
        super(DataFile, self).__init__()
        self._content = {'filepath': '', 'name': '', 'extension': '', 'data': ''}

        if checkRealPath(filepath):
            self.update_content(filepath)

        else:
            del self

    def update_content(self, filepath):
        extension = re.search("(?<=\.)([a-zA-Z0-9_]+$)", filepath)
        name = re.search("([a-zA-Z0-9_])+(?=\.[a-zA-Z0-9_]+$)", filepath)
        with open(self._filePath, 'r') as file:
            data = file.readlines()
            print(data)
            self._content['filepath'] = filepath
            self._content['name'] = name
            self._content['extension'] = extension
            self._content['data'] = data

    @property
    def filePath(self):
        return self.content['filepath']

    @property
    def name(self):
        return self._content['name']

    @property
    def extension(self):
        return self._content['extension']

    @property
    def data(self):
        return self._content['data']


class DataLoaderModel(QObject):
    s_update_dataFileDict = pyqtSignal()

    def __init__(self):
        super(DataLoaderModel, self).__init__()
        self._dataFilesList = []
        self._selectedDataFile = None

    @property
    def dataFilesDict(self):
        return self._dataFilesList

    @property
    def selectedDataFile(self):
        return self._selectedDataFile

    @selectedDataFile.setter
    def selectedDataFile(self, value):
        self._selectedDataFile = value

    def add_dataFile(self, dataFile:DataFile):
        if dataFile not in self._dataFilesList:
            self._dataFilesList.append(dataFile)
            self.s_update_dataFileDict.emit()
        else:
            pass

    def delete_dataFile(self):
        del self._selectedDataFile


class Test_DataLoaderModel(unittest.TestCase):
    def setUp(self):
        self.DataLoader = DataLoaderModel()

    def test_regex_filename(self):
        string = "C:\\test\\testFile.txt"
        name = re.search("([a-zA-Z0-9_])+(?=\.[a-zA-Z0-9_]+$)", string)
        nameToMatch = "testFile"
        self.assertEqual(nameToMatch, name[0])

    def test_add_dataFile___basic(self):
        self.DataLoader.add_dataFile("C://users//nothing//hello0.png")
        testDict = {"0": {"name": "hello0", "absolutePath": "C://users//nothing//hello0.png", "extension": "png"}}
        self.assertEqual(testDict, self.DataLoader._dataFilesDict)

    def test_add_datafile___not_empty(self):
        self.DataLoader.add_dataFile("C://users//nothing//hello0.png")
        self.DataLoader.add_dataFile("C://users//nothing//hello1.png")
        testDict = {"0": {"name": "hello0", "absolutePath": "C://users//nothing//hello0.png", "extension": "png"},
                    "1": {"name": "hello1", "absolutePath": "C://users//nothing//hello1.png", "extension": "png"}}
        self.assertEqual(testDict, self.DataLoader._dataFilesDict)

    def test_add_datafile___with_real_files(self):
        pathToTest0 = os.path.abspath("\\test\\testFile0.txt")
        pathToTest1 = os.path.abspath("/test/testFile1.txt")
        self.DataLoader.add_dataFile(pathToTest0)
        self.DataLoader.add_dataFile(pathToTest1)
        testDict = {"0": {"name": "testFile0", "absolutePath": pathToTest0, "extension": "txt"},
                    "1": {"name": "testFile1", "absolutePath": pathToTest1, "extension": "txt"}}
        self.assertEqual(testDict, self.DataLoader._dataFilesDict)


if __name__ == "__main__":
    unittest.main()
