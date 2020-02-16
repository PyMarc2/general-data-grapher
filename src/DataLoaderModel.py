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

