import os
import platform
import subprocess
from PySide6.QtWidgets import QWidget, QComboBox, QTableWidget, QTableWidgetItem, QPushButton,  QHBoxLayout, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtCore import Qt
from dao import paperCatelogDao, paperDao
from paper.paperDetailManageWidget import PaperDetailManageWidget
from paper.paperTextManageWidget import PaperTextManageWidget


class OperatedCellWidget(QWidget):
    def __init__(self, paperTable: QTableWidget, paperCatelogCbx: QComboBox, rowIndex: int):
        super(OperatedCellWidget, self).__init__()

        self.paperTable = paperTable
        self.paperCatelogCbx = paperCatelogCbx
        self.rowIndex = rowIndex
        
        self.setupUi()

        # clicked signal
        self.DetailBtn.clicked.connect(self.DetailBtnClicked)
        self.OpenTextBtn.clicked.connect(self.openTextClicked)
        self.OpenPdfBtn.clicked.connect(self.openPdfClicked)

    def setupUi(self):
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(7, 0, 7, 0)
        self.layout.setSpacing(17)

        self.DetailBtn = QPushButton("Detail")
        self.DetailBtn.setStyleSheet(
            "color: white; background-color: rgb(0, 190, 200); border-radius: 5px; font-weight: bold;")
        self.DetailBtn.setFixedHeight(23)

        self.OpenTextBtn = QPushButton("Text")
        self.OpenTextBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 5px; font-weight: bold;")
        self.OpenTextBtn.setFixedHeight(23)
        
        self.OpenPdfBtn = QPushButton("PDF")
        self.OpenPdfBtn.setStyleSheet(
            "color: white; background-color: rgb(123, 104, 238); border-radius: 5px; font-weight: bold;")
        self.OpenPdfBtn.setFixedHeight(23)

        self.layout.addWidget(self.DetailBtn)
        self.layout.addWidget(self.OpenTextBtn)
        self.layout.addWidget(self.OpenPdfBtn)

    @Slot()
    def DetailBtnClicked(self):
        paperId = self.paperTable.paperId[self.rowIndex]
        self.paperDetailManage: QWidget = PaperDetailManageWidget(
            paperTable=self.paperTable, paperId=paperId)
        self.paperDetailManage.editChangedSignal.connect(
            lambda: initPaperTable(self.paperTable, self.paperCatelogCbx))
        self.paperDetailManage.show()

    @Slot()
    def openTextClicked(self):
        paperId = self.paperTable.paperId[self.rowIndex]
        self.paperTextManage: QWidget = PaperTextManageWidget(
            paperTable=self.paperTable, paperId=paperId)
        self.paperTextManage.editChangedSignal.connect(
            lambda: initPaperTable(self.paperTable, self.paperCatelogCbx))
        self.paperTextManage.show()

    @Slot()
    def openPdfClicked(self):
        paperId = self.paperTable.paperId[self.rowIndex]

        paper = paperDao.getPaperFromId(paperId)[0]
        folderPath = paper.folderPath
        fileName = paper.fileName
        print(folderPath, fileName)

        if (not folderPath) or (not fileName):
            QMessageBox.information(
                self, "Information", "The pdf file does not exist.")
            return

        filePath = os.path.join(folderPath, fileName)

        if platform.system() == "Darwin":  # macOS
            subprocess.run(["open", filePath])
        elif platform.system() == "Windows":  # Windows
            subprocess.run(["start", "", filePath], shell=True)
        else:  # Linux
            subprocess.run(["xdg-open", filePath])


def clearPaperTable(paperTable: QTableWidget):
    paperTable.clearContents()
    paperTable.setRowCount(0)


def initPaperTable(paperTable: QTableWidget, paperCatelogCbx: QComboBox, fuzzyInfo: str = ""):
    # ! paper table cell changed signal
    # if QTableWidget has been set cellChanged signal, it will be disconnected
    paperTable.blockSignals(True)

    clearPaperTable(paperTable)

    paperCatelogName = paperCatelogCbx.currentText()
    paperCatelogList = paperCatelogDao.getPaperCatelogFromName(
        paperCatelogName)
    if not paperCatelogList:
        return

    paperCatelogId = paperCatelogList[0][0]
    papers = paperDao.getPaperFromTypeFuzzyInfo(
        paperCatelogId, fuzzyInfo, True)
    if not papers:
        clearPaperTable(paperTable)
        return

    row = len(papers)
    paperTable.setRowCount(row)  # row

    # set style
    for i in range(row):
        paperTable.setRowHeight(i, 35)

    paperTable.paperId = {}
    # set data
    for i in range(row):
        # * set paper id
        paperTable.paperId[i] = papers[i].id

        # * set checkbox
        checkbox_item = QTableWidgetItem()
        checkbox_item.setFlags(checkbox_item.flags()
                               | Qt.ItemIsUserCheckable)
        checkbox_item.setCheckState(Qt.Unchecked)
        paperTable.setItem(i, 0, checkbox_item)

        # * set paper data
        # paper name
        data = QTableWidgetItem(papers[i].paperName)
        data.setTextAlignment(Qt.AlignCenter)
        paperTable.setItem(i, 1, data)

        # title
        data = QTableWidgetItem(papers[i].title)
        data.setTextAlignment(Qt.AlignCenter)
        paperTable.setItem(i, 2, data)

        # author
        data = QTableWidgetItem(papers[i].author)
        data.setTextAlignment(Qt.AlignCenter)
        paperTable.setItem(i, 3, data)

        # journal
        data = QTableWidgetItem(papers[i].journal)
        data.setTextAlignment(Qt.AlignCenter)
        paperTable.setItem(i, 4, data)

        # date
        data = QTableWidgetItem(papers[i].date)
        data.setTextAlignment(Qt.AlignCenter)
        paperTable.setItem(i, 5, data)

        # * operate
        operationCell = OperatedCellWidget(
            paperTable, paperCatelogCbx, rowIndex=i)
        paperTable.setCellWidget(i, 6, operationCell)

    paperTable.blockSignals(False)


def paperTableHeaderClicked(paperTable: QTableWidget, logicalIndex: int):
    if logicalIndex == 0:
        state = Qt.Checked if paperTable.horizontalHeaderItem(
            0).checkState() == Qt.Unchecked else Qt.Unchecked
        paperTable.horizontalHeaderItem(0).setCheckState(
            Qt.Checked) if state == Qt.Checked else paperTable.horizontalHeaderItem(0).setCheckState(Qt.Unchecked)
        for row in range(paperTable.rowCount()):
            item = paperTable.item(row, 0)
            if item is not None:
                item.setCheckState(state)


def adjustPaperTableColumn(paperTable: QTableWidget, logicalIndex: int):

    paperTable.horizontalHeader().sectionResized.disconnect()

    currentWidth = sum(paperTable.columnWidth(i)
                       for i in range(paperTable.columnCount()))
    # diff = newSize - oldSize
    totalWidth = paperTable.totalWidth
    if paperTable.rowCount() >= 10:
        totalWidth -= 15
    if paperTable.rowCount() >= 100:
        totalWidth -= 15
    diff = totalWidth - currentWidth

    currentColHeaderLabel = paperTable.horizontalHeaderItem(
        logicalIndex).text()
    for columnIndex in range(paperTable.columnCount()):
        # ['✓', 'Paper Name', Title', 'Author', 'Journal', 'Date', 'Operate']
        headerLabel = paperTable.horizontalHeaderItem(
            columnIndex).text()
        if headerLabel not in ['✓', 'Operate', currentColHeaderLabel]:
            newColWidth = paperTable.columnWidth(
                columnIndex) + diff / (paperTable.columnCount() - 3)
            paperTable.paperTable.setColumnWidth(columnIndex, newColWidth)

    paperTable.horizontalHeader().sectionResized.connect(
        lambda index: adjustPaperTableColumn(paperTable, index))


def getRowCheckedState(paperTable: QTableWidget) -> list[int]:
    ret = []
    for idx, row in enumerate(range(paperTable.rowCount())):
        item = paperTable.item(row, 0)

        if item.checkState() == Qt.Checked:
            ret.append(idx)
    return ret


def getRowItem(paperTable: QTableWidget, rowList: list[int]) -> list[list]:
    ret = []
    for row in rowList:
        rowInfo = []
        rowInfo.append(paperTable.paperId[row])
        for col in range(paperTable.columnCount()):
            item = paperTable.item(row, col)
            if item is not None:
                rowInfo.append(item.data(Qt.ItemDataRole.DisplayRole))
            else:
                rowInfo.append(None)
        ret.append(rowInfo)
    return ret


def paperTableCellChanged(paperTable: QTableWidget, row, col):

    if col in [0, 6]:
        return

    headerLabel = paperTable.horizontalHeaderItem(col).text()

    paperId = getRowItem(paperTable, [row])[0][0]

    paper = paperDao.getPaperFromId(paperId)[0]

    if headerLabel.replace(" ", "").lower() == "papername":
        paper.paperName = paperTable.item(row, col).text().strip()
    if headerLabel.replace(" ", "").lower() == "title":
        paper.title = paperTable.item(row, col).text().strip()
    if headerLabel.replace(" ", "").lower() == "author":
        paper.author = paperTable.item(row, col).text().strip()
    if headerLabel.replace(" ", "").lower() == "journal":
        paper.journal = paperTable.item(row, col).text().strip()
    if headerLabel.replace(" ", "").lower() == "date":
        paper.date = paperTable.item(row, col).text().strip()

    if not paperDao.modifyPaper(paper):
        QMessageBox.critical(paperTable, "Error",
                             f"Failed to modify paper - {paper.paperName}")
        return
