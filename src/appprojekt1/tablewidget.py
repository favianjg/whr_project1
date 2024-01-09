try:
    from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
except ModuleNotFoundError:
    from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.df = None

        self.cellChanged[int, int].connect(self.update_df)

    def display_data(self, df):
        """
        Puts all the data from the data set (.csv file) we opened into a tableWidget.
        """
        # assign the dataFrame object
        self.df = df

        # set table dimension to the size of the dataFrame object
        n_rows, n_columns = self.df.shape
        self.setColumnCount(n_columns)
        self.setRowCount(n_rows)

        # set the "names" of the columns of the dataFrame as the title in the table
        self.setHorizontalHeaderLabels(self.df.columns)
        # set the "names" of the rows of the dataFrame as the title in the table
        if isinstance(self.df.index[0], str):
            self.setVerticalHeaderLabels(self.df.index)
        # set selection mode to column selection
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        # allow multiple columns to be selected
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

        # copy all the data from the dataFrame to the table
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))

        self.show()

    def get_selected_columns(self):
        """
        Returns the selected columns that the user clicked on in the table.
        """
        # this creates a list of the indexes of all the selected columns
        # example: Column number 0, 5 and 9 got selected, this method returns:
        # [0, 5, 9]
        columns = [idx.column() for idx in self.selectionModel().selectedColumns()]
        return columns

    def update_df(self, row, column):
        """
        When the user edits and element in the table we have to update the dataFrame object accordingly.
        """
        # get new value
        text = self.item(row, column).text()

        # convert numeric values to floats
        try:
            text = float(text)
        except ValueError:
            pass

        self.df.iloc[row, column] = text

    def delete_columns(self, selected_columns):
        """
        Deletes the currently selected columns from the DataFrame object.
        """
        self.df.drop(columns=selected_columns)

    def clear(self):
        """
        Clears the table content and the column names.
        """
        # do not forget to clear the data variable!
        self.df = None

        # setting the numbers of rows and columns to show in the table to 0
        # 'clears' the content by not showing it at all
        self.setRowCount(0)
        self.setColumnCount(0)
