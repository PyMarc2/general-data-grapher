from PyQt5.QtCore import QAbstractTableModel


class DataLoaderWidget(QAbstractTableModel):
    def __init__(self):
        super(DataLoaderWidget, self).__init__()
        self.selected_file = ''

    def setData(self):

