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
        # intialisiert den Anfangszustand der Variable
        self.data = None
        self.filename = None
        self.modifiedFileName = None
        self.selected_columns = []
        self.filehandler = files.FileHandler()
        self.fileDialog = FileDialog()

        # get current working directory
        self.current_wd = Path.cwd().as_posix()

        # load the GUI file from QtDesigner
        # das Design wurde im QtDesigner erstellt und hier geladen
        self.main_window = uic.loadUi(str(self.current_wd)+'/appprojekt1/resources/window.ui', self)
        # am Anfang ist noch keine Datei ausgewählt
        if self.filename is None:
            self.main_window.lblFileName.setText("noch kein File ausgewählt")

        # call the UI button handler
        self.button_handler()

        # display the GUI
        self.show()

    def button_handler(self):
        """
        Handles all the UI button callbacks
        means: which function is called for which button press.
        """
        self.main_window.btnOpenFile.clicked.connect(self.open_data)
        self.main_window.btnPlotData.clicked.connect(self.visualize_data)
        self.main_window.rbScatterPlot.clicked.connect(self.visualize_data)
        self.main_window.rbLinePlot.clicked.connect(self.visualize_data)
        self.main_window.btnExportFile.clicked.connect(self.export_data)
        self.main_window.btnShowStatistics.clicked.connect(self.show_statistics)
        self.main_window.btnShowCorrelations.clicked.connect(self.show_correlation_matrix)
        self.main_window.btnDeleteColumns.clicked.connect(self.delete_columns)
        self.main_window.btnClear.clicked.connect(self.clear_all)

    def open_data(self):
        """
        Wrapper for the open data method in file handler.
        """
        # nutzt den fileDialog Widget um den Nutzer nach dem File nachzufragen
        self.filename = self.fileDialog.open_file_name_dialog()
        # wenn der User eine Datei ausgewählt hat, mach den Inhalt der Datei mit Hilfe des Filehandlers auf
        # und überschreibt den Label mit dem Dateinamen
        if self.filename is not None:
            self.data = self.filehandler.open_file(self.filename)
            self.main_window.lblFileName.setText(self.filename)

        # wenn der Inhalt vorhanden ist, stellt er in der Tabelle dar
        if self.data is not None:
            self.tableData.display_data(df=self.data)

    def export_data(self):
        """
        Wrapper for the save file method in FileHandler. Takes the file path and
        adds "_modified" to the filename and saves the DataFrame object to this .csv.
        """
        # den User nach einem neuen Dateinamen nachfragen
        self.modifiedFileName = self.fileDialog.save_file_dialog()
        # wenn der User einen neuen Namen eingibt, und der Inhalt nicht leer ist, speichere die Datei
        if self.modifiedFileName and self.modifiedFileName != self.filename and self.data:
            self.filehandler.save_file(file_path=self.modifiedFileName)
        else:
            # wenn nicht, wirf einen Fehler zurück
            show_message("Die Datei wurde nicht gespeichert. Bitte prüfen Sie ihre Eingabe")

    def visualize_data(self):
        """
        Call the open_data() method and creates a plot.
        """
        # Prüf ob einen Datei-Inhalt vorhanden ist, wenn nicht wirf einen Fehler
        if self.data is None:
            show_message("Kein File ausgewählt. Öffnen Sie bitte erst ein CSV File")
        else:
            # wenn der Datei-Inhalt geladen wurde, prüf welche Spalte wurden ausgewählt
            # mit Hilfe der "get_selected_columns" Funktion in TableWidget
            self.selected_columns = [
                self.data.columns[columns_index] for columns_index in self.tableData.get_selected_columns()
            ]
            # prüf ob genau 2 Spalten ausgewählt wurden
            if len(self.selected_columns) != 2:
                show_message("Sie müssen genau 2 Spalten auswählen. Bitte korrigieren Sie ihre Auswahl")
            else:
                # Prüf ob der Scatterbutton aktiviert worden ist, wenn ja dann stellt es auf ein Line-Plot um
                if self.main_window.rbScatterPlot.isChecked():
                    self.mplWidget.line_plot(
                        x=self.data[self.selected_columns[0]], y=self.data[self.selected_columns[1]],
                        x_label=self.selected_columns[0], y_label=self.selected_columns[1], title='Interesting'
                    )
                    self.main_window.rbLinePlot.setChecked(True)
                else:
                    # sonst stellt eine ScatterPlot dar
                    self.mplWidget.scatter_plot(
                        x=self.data[self.selected_columns[0]], y=self.data[self.selected_columns[1]],
                        x_label=self.selected_columns[0], y_label=self.selected_columns[1], title='Interesting'
                    )
                    self.main_window.rbScatterPlot.setChecked(True)
                self.mplWidget.show()

    def show_statistics(self):
        """
        Calculates the statistic values of the loaded data set and plots them
        to another table.
        """
        if self.data is not None:
            # setzt die Pandaseinstellung um die Statistiken darzustellen
            pd.set_option('display.precision', 3)
            statistics = self.data.describe()
            # set the "names" of the rows of the dataFrame as the title in the table
            self.tableStatistics.display_data(df=statistics)
            # prüf ob der Name der Reihe eine String ist, wenn ja setzt das als der Label der Reihe
            if isinstance(statistics.index[0], str):
                self.tableStatistics.setVerticalHeaderLabels(statistics.index)

    def show_correlation_matrix(self):
        """
        Computes the correlation matrix for a DataFrame object
        and displays it in a custom tableWidget.
        """
        if self.data is not None:
            # Filtert die nicht revelante Spalte raus
            irrelevant_columns = ['Country', 'Region', 'Happiness Rank', 'Standard Error']
            # Lösch die nicht relevante Spalte aus dem Datei-Inhalt
            self.data.drop(columns=irrelevant_columns)
            # stell die Korrelation Tabelle dar
            correlations = self.data.corr(method='pearson', numeric_only=True).round(1)
            self.tableCorrelations.display_data(
                df=correlations
            )

    def delete_columns(self):
        """
        Wrapper for deleting columns, check if requirements are met
        """
        # Prüf ob der User mindestens 1 Spalte der Tabelle gewählt hat
        if len(self.tableData.get_selected_columns()) < 1:
            show_message("Sie müssen mindestens 1 Spalte auswählen. Bitte korrigieren Sie ihre Eingabe")
        else:
            # Lösch die Spalte aus der Tabelle
            self.selected_columns = [
                self.data.columns[columns_index] for columns_index in self.tableData.get_selected_columns()
            ]
            self.tableWidget.delete_columns(self.selected_columns)

    def clear_all(self):
        """
        Clears the UI tables and the graph
        """
        # setzt alle benutzten Variablen wieder zurück
        self.data = None
        self.filename = None
        self.modifiedFileName = None
        self.selected_columns = []
        self.main_window.rbLinePlot.setChecked(False)
        self.main_window.rbScatterPlot.setChecked(False)
        self.tableData.clear()
        self.tableStatistics.clear()
        self.tableCorrelations.clear()
        self.mplWidget.clear()

    def closeEvent(self, event):
        """
        Window that pops up when the red x in the corner is clicked.
        """
        # Öffne ein Fenster beim Schließen um den User nochmal wegen dem Beenden nachzufragen
        reply = QMessageBox.question(self, 'Nachricht',
                                     'Sind Sie sicher, dass Sie beenden möchten?',
                                     QMessageBox.Yes | QMessageBox.No)

        self.when_closing(reply, event)

    def when_closing(self, reply, event):
        """
        Is called when the app is closed.
        """
        # Schließ das App, wenn ja ausgewählt wurde, sonst ignorieren
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

