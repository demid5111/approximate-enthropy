import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QTextEdit, QLabel, QVBoxLayout, QFileDialog


class FileChooserWidget(QWidget):
    new_files_chosen = pyqtSignal()
    erased_files = pyqtSignal()

    def __init__(self, parent, file_name):
        super(QWidget, self).__init__(parent)
        self.file_name = file_name
        self.init_ui()

    def init_ui(self):
        fileNamesOpen = QPushButton('Open files', self)
        fileNamesOpen.clicked.connect(self.show_file_chooser)

        fileNamesClean = QPushButton('Clean files', self)
        fileNamesClean.clicked.connect(self.clean_file_names)

        file_chooser_group = QGridLayout()
        fileNamesLabel = QLabel('Files to analyze')
        self.file_names_edit = QTextEdit('')

        file_buttons_group = QVBoxLayout()
        file_buttons_group.addWidget(fileNamesOpen)
        file_buttons_group.addWidget(fileNamesClean)

        file_chooser_group.addWidget(fileNamesLabel, 0, 0)
        file_chooser_group.addWidget(self.file_names_edit, 0, 1)
        file_chooser_group.addLayout(file_buttons_group, 0, 2)

        self.setLayout(file_chooser_group)

    def clean_file_names(self):
        self.file_names_edit.clear()
        self.erased_files.emit()

    def show_file_chooser(self):
        path = ""
        try:
            with open(self.file_name, 'r') as f:
                path = f.readline().strip()
        except FileNotFoundError:
            pass
        fname = QFileDialog.getOpenFileNames(self, 'Open file', path, 'DAT (*.dat, *.txt, *.DAT, *.TXT)',
                                             'Text files (*.txt *.TXT, *.dat, *.DAT)')
        self.file_names_edit.setText("")
        print(fname)
        for name in fname[0]:
            self.file_names_edit.append(name)
        self.memorize_last_path()
        self.new_files_chosen.emit()

    def memorize_last_path(self):
        if not self.file_names_edit:
            return
        path = os.path.dirname(self.file_names_edit.toPlainText().split('\n')[0])
        with open(self.file_name, 'w') as f:
            f.write(path + '/')

    def get_file_names(self):
        return [x for x in self.file_names_edit.toPlainText().split('\n') if x]
