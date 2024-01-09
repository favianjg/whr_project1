"""
Created by:

Hier die Antworten zu den Theoriefragen:
...

"""
import sys
import pandas as pd
from pathlib import Path

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
        # main window attributes: create class instances (objects) of our custom modules
        super(MainWindow, self).__init__()
        self.data = None
        self.filename = None
        self.selected_columns = []
        self.filehandler = files.FileHandler()
        self.fileDialog = FileDialog()

        # get current working directory
        self.current_wd = Path.cwd().as_posix()

        # load the GUI file from QtDesigner
        self.main_window = uic.loadUi(str(self.current_wd)+'/appprojekt1/resources/window.ui', self)
        if self.filename is None:
            self.main_window.lblFileName.setText("noch kein File ausgewählt")
        self.button_handler()

        # call the UI button handler

        # display the GUI
        self.show()

    def button_handler(self):
        """
        Handles all the UI button callbacks
        means: which function is called for which button press.
        """
        self.main_window.btnOpenFile.clicked.connect(self.open_data)
        self.main_window.btnPlotData.clicked.connect(self.visualize_data)
        self.main_window.btnExportFile.clicked.connect(self.export_data)
        self.main_window.btnShowStatistics.clicked.connect(self.show_statistics)
        self.main_window.btnShowCorrelations.clicked.connect(self.show_correlation_matrix)
        # self.main_window.btnDeleteColumns.clicked.connect(self.tableWidget.delete_columns)
        self.main_window.btnClear.clicked.connect(self.clear_all)

    def open_data(self):
        """
        Wrapper for the open data method in file handler.
        """
        self.filename = self.fileDialog.open_file_name_dialog()
        if self.filename is not None:
            self.main_window.lblFileName.setText(self.filename)
            self.data = self.filehandler.open_file(self.filename)

        if self.data is not None:
            self.tableData.display_data(df=self.data)

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
        if self.data is None:
            show_message("Kein File ausgewählt. Öffnen Sie bitte erst ein CSV File")
        else:
            self.selected_columns = [
                self.data.columns[columns_index] for columns_index in self.tableData.get_selected_columns()
            ]
            if len(self.selected_columns) != 2:
                show_message("Sie müssen genau 2 Spalten auswählen. Bitte korrigieren Sie ihre Auswahl")
            else:
                self.mplWidget.scatter_plot(
                    x=self.data[self.selected_columns[0]], y=self.data[self.selected_columns[1]],
                    x_label=self.selected_columns[0], y_label=self.selected_columns[1], title='Interesting'
                )
                self.rbScatterPlot.setChecked(True)
                self.mplWidget.show()

    def show_statistics(self):
        """
        Calculates the statistic values of the loaded data set and plots them
        to another table.
        """
        if self.data is not None:
            pd.set_option('display.precision', 3)
            self.tableStatistics.display_data(df=self.data.describe())

    def show_correlation_matrix(self):
        """
        Computes the correlation matrix for a DataFrame object
        and displays it in a custom tableWidget.
        """
        if self.data is not None:
            correlations = self.data.corr(method='pearson')
            correlations.style.background_gradient(cmap='viridis').set_precision(2)
            self.tableCorrelations.display_data(
                df=correlations
            )

    def clear_all(self):
        """
        Clears the UI tables and the graph
        """
        ...

    def closeEvent(self, event):
        """
        Window that pops up when the red x in the corner is clicked.
        """
        reply = QMessageBox.question(self, 'Nachricht',
                                     'Sind Sie sicher, dass Sie beenden möchten?',
                                     QMessageBox.Yes | QMessageBox.No)

        self.when_closing(reply, event)

    def when_closing(self, reply, event):
        """
        Is called when the app is closed.
        """
        if reply == QMessageBox.Yes:
            print('App schließt jetzt ab')
            event.accept()
        else:
            print('Abgebrochen')
            event.ignore()


def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setWindowTitle('App Projekt 1')

    if PYQTV == 5:
        sys.exit(app.exec_())
    else:
        sys.exit(app.exec())

