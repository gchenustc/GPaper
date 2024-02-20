    for row in range(table.rowCount()):
        checkbox_item = QTableWidgetItem()
        checkbox_item.setFlags(checkbox_item.flags() | Qt.ItemIsUserCheckable)
        table.setItem(row, 1, checkbox_item)
        
        