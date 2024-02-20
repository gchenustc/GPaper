from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Table Widget Example')

        self.setGeometry(100, 100, 600, 400)
        
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.populate_table()

    def populate_table(self):
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(3)

        for row in range(3):
            for col in range(3):
                item = QTableWidgetItem(f'Item {row},{col}')
                self.table_widget.setItem(row, col, item)

                push_button = QPushButton('Get Info')
                push_button.clicked.connect(self.get_info)
                self.table_widget.setCellWidget(row, col, push_button)

            self.table_widget.setRowHeight(row, 30)

    def get_info(self):
        push_button = self.sender()
        if isinstance(push_button, QPushButton):
            # 获取PushButton所在的单元格行和列
            index = self.table_widget.indexAt(push_button.pos())
            row = index.row()
            print(row)
            # 获取该行每一列的信息
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item is not None:
                    print(item.text())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()