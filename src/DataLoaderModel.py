from PyQt5.QtCore import pyqtSignal, QObject
import unittest
import os
import re


class DataLoaderModel(QObject):
    s_update_dataFileDict = pyqtSignal()

    def __init__(self):
        super(DataLoaderModel, self).__init__()
        self._dataFilesDict = {}
        self._selectedDataFile = ''

    @property
    def dataFilesDict(self):
        return self._dataFilesDict

    @property
    def selectedDataFile(self):
        return self._selectedDataFile

    @selectedDataFile.setter
    def selectedDataFile(self, value):
        # do some filtering here
        self._selectedDataFile = value

    def add_dataFile(self, absPath: str):
        if absPath not in self._dataFilesDict.items():
            number = len(self._dataFilesDict)
            extension = re.search("(?<=\.)([a-zA-Z0-9_]+$)", absPath)
            if extension is None:
                raise NotImplementedError
            extension = extension[0]
            name = re.search("([a-zA-Z0-9_])+(?=\.[a-zA-Z0-9_]+$)", str(absPath))
            if name is None:
                raise NotImplementedError
            name = name[0]
            self._dataFilesDict["{}".format(number)] = {"name": "{}".format(name), "absolutePath": absPath,
                                                            "extension": extension}
            self.s_update_dataFileDict.emit()
        else:
            pass

    def delete_dataFile(self):
        pass


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
