from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(5, 3)  # 假设你有5行3列
        self.setHorizontalHeaderLabels(['Column1', 'Column2', 'Column3'])

        # 设置表头第二列的样式和初始状态
        self.horizontalHeaderItem(1).setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.horizontalHeaderItem(1).setCheckState(Qt.Unchecked)

        # 处理表头复选框点击事件
        self.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

    def on_header_clicked(self, logicalIndex):
        if logicalIndex == 1:
            state = Qt.Checked if self.horizontalHeaderItem(1).checkState() == Qt.Unchecked else Qt.Unchecked
            for row in range(self.rowCount()):
                item = self.item(row, 1)
                if item is not None:
                    item.setCheckState(state)

if __name__ == "__main__":
    app = QApplication([])

    table = TableWidget()

    # 添加数据并显示窗口
    for row in range(table.rowCount()):
        checkbox_item = QTableWidgetItem()
        checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemIsUserCheckable)
        table.setItem(row, 1, checkbox_item)

    widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(table)
    widget.setLayout(layout)
    widget.show()

    app.exec_()