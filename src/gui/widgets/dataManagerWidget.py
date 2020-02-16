import os
from PyQt5 import uic
from PyQt5.QtWidgets import QTableView, QApplication, QSizePolicy, QHeaderView, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QAbstractTableModel, QObject
import sys
import logging

log = logging.getLogger(__name__)
dataManagerWidgetPath = os.path.dirname(os.path.realpath(__file__)) + '\\dataManagerWidgetUi.ui'
Ui_dataManagerWidget, QtBaseClass = uic.loadUiType(dataManagerWidgetPath)


class DataManagerWidget(QWidget, Ui_dataManagerWidget): # type: class
    def __init__(self):

        super(DataManagerWidget, self).__init__()
        self.setupUi(self)

    def mimeTypes(self):
        mimetypes = super().mimeTypes()
        mimetypes.append('text/plain')
        return mimetypes

    def dropMimeData(self, index, data, action):
        if data.hasText():
            self.addItem(data.text())
            return True
        else:
            return super().dropMimeData(index, data, action)


class DataLoaderWidget(QWidget):
    def __init__(self):
        super(DataLoaderWidget, self).__init__()
        self.tableWidget = QTableView()
        self.tableModel = FormTableModel()
        self.tableWidget.setModel(self.tableModel)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tableWidget)


class FormTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(FormTableModel, self).__init__(parent)
        self.headerText = ["DataSet Indicator", "DataSet Name", "Extension", "Plot"]
        self.data = [[]]
        self.rowAmount = 1

    def rowCount(self, parent=None):
        return self.rowAmount

    def columnCount(self, parent=None):
        return len(self.headerText)

    def headerData(self, col, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headerText[col]

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.data[index.row()][index.column()]

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True


class AbstractTableView(QObject):

    def __init__(self, parent, table_model):
        super(AbstractTableView, self).__init__()
        self.tableView = QTableView(parent)
        self.table_model = table_model

        # Set behaviour of table
        self.tableView.setAlternatingRowColors(True)

        # Set model # do not add sorting without handling buttons sorting
        self.tableView.setModel(self.table_model)

        # add row PushButton
        # self.insert_button()

        # styleofmytable
        self.tableView.setStyleSheet('''

    QWidget {
    background-color: #EFF6EE;
    color: #191712;
}

QHeaderView::section {
    background-color: #233043;
    color: #EFF6EE;
    padding: 4px;
    border: 1px solid #fffff8;
    font-size: 14pt;
}

QTableWidget {
    gridline-color: #fffff8;
    font-size: 12pt;
}

QTableWidget QTableCornerButton::section {
    background-color: #646464;
    border: 1px solid #fffff8;
}

''')
        self.tableView.setStyleSheet(''' ''')

        # Set Column size
        self.tableView.setSortingEnabled(False)
        self.tableView.verticalHeader().hide()
        self.tableView.setColumnWidth(0, 90)
        self.tableView.setColumnWidth(1, 190)
        self.tableView.setColumnWidth(2, 550)
        self.tableView.setColumnWidth(3, 270)
        self.tableView.setColumnWidth(4, 110)
        self.tableView.setColumnWidth(5, 120)
        self.tableView.setColumnWidth(6, 162)

        # column behaviour
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

        # Set Size Policy
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        # self.setSizePolicy(sizePolicy)

    @property
    def table_model(self):
        return self._table_model

    @table_model.setter
    def table_model(self, value):
        self._table_model = value
        self.tableView.setModel(value)

    def table_content_changed(self):
        self.tableView.resizeColumnsToContents()

    # def insert_button(self):
    #     button = QItemDelegate(self.tableView)
    #     self.tableView.setItemDelegateForColumn(len(self.table_model.table_definition()) - 1, button)
    #     button.s_button.connect(self.button_clicked)

    def button_clicked(self, row):
        pass

