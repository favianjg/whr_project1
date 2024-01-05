"""
Created by:

Hier die Antworten zu den Theoriefragen:
...

"""
import sys
import pathlib

PYQTV = None

try:
    from PyQt5 import QtWidgets, uic
    from PyQt5.QtWidgets import QMessageBox
    from PyQt5.QtGui import QPixmap, QImage
    PYQTV = 5

except ModuleNotFoundError:
    from PyQt6 import QtWidgets, uic
    from PyQt6.QtWidgets import QMessageBox
    from PyQt6.QtGui import QPixmap, QImage
    PYQTV = 6

import appprojekt1.filehandling as files
from appprojekt1.fileDialog import FileDialog
from appprojekt1.popUpWindow import show_message


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # main window attributes: create class instances (objects) of our custom modules
        ...

        # get current working directory
        ...

        # load the GUI file from QtDesigner
        ...

        # call the UI button handler
        ...
        # display the GUI
        ...

    def button_handler(self):
        """
        Handles all the UI button callbacks
        means: which function is called for which button press.
        """
        ...

    def open_data(self):
        """
        Wrapper for the open data method in file handler.
        """
        ...

    def export_data(self):
        """
        Wrapper for the save file method in FileHandler. Takes the file path and
        adds "_modified" to the filename and saves the DataFrame object to this .csv.
        """
        ...

    def visualize_data(self):
        """
        Call the open_data() method and creates a plot.
        """
        ...

    def show_statistics(self):
        """
        Calculates the statistic values of the loaded data set and plots them
        to another table.
        """
        ...

    def show_correlation_matrix(self):
        """
        Computes the correlation matrix for a DataFrame object
        and displays it in a custom tableWidget.
        """
        ...

    def clear_all(self):
        """
        Clears the UI tables and the graph
        """
        ...

    def closeEvent(self, event):
        """
        Window that pops up when the red x in the corner is clicked.
        """
        ...

    def when_closing(self, reply, event):
        """
        Is called when the app is closed.
        """
        ...


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle('App Projekt 1')

    if PYQTV == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())

