import os
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect,
                            QSize, QModelIndex, Signal)
from PySide6.QtGui import (QFont, QIcon)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QHeaderView, QLabel, QLineEdit, QPushButton,
                               QSizePolicy, QTableWidget, QTableWidgetItem, QTextEdit, QWidget, QAbstractItemView, QMessageBox)
from dao import paperCatelogDao, paperDao
from entity.paperCatelogModel import PaperCatelog


class PaperCatelogManageWidget(QWidget):

    closeSignal = Signal()

    def __init__(self):
        super(PaperCatelogManageWidget, self).__init__()
        
        self.setupUi()

        # clicked signal
        self.searchBtn.clicked.connect(self.searchBtnClicked)
        self.addBtn.clicked.connect(self.addBtnClicked)
        self.deleteBtn.clicked.connect(self.delBtnClicked)
        self.modifyBtn.clicked.connect(self.tableClicked)
        self.catelogTable.clicked.connect(self.showInfo)
        
        self.initCatelogTable()

    def setupUi(self):
        self.resize(1000, 760)

        font = QFont()
        font.setPointSize(12)

        # ? search group
        self.searchGroup = QGroupBox(self)
        self.searchGroup.setObjectName(u"searchGroup")
        self.searchGroup.setGeometry(QRect(135, 20, 721, 71))
        self.searchGroup.setFont(QFont("Arial", 12))
        # self.searchGroup.setStyleSheet("font-weight: bold;")

        self.searchInput = QLineEdit(self.searchGroup)
        self.searchInput.setObjectName(
            u"paperCatelogLineEditSearch")
        self.searchInput.setGeometry(QRect(260, 20, 201, 31))

        self.searchLabel = QLabel(self.searchGroup)
        self.searchLabel.setObjectName(
            u"paperCatelogNameLabelSearch")
        self.searchLabel.setGeometry(QRect(125, 20, 100, 31))
        self.searchLabel.setFont(font)

        self.searchBtn = QPushButton(self.searchGroup)
        self.searchBtn.setObjectName(u"searchButton")
        self.searchBtn.setGeometry(QRect(500, 20, 91, 31))
        self.searchBtn.setFont(font)
        icon = QIcon()
        icon.addFile(u"../images/search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.searchBtn.setIcon(icon)

        # ? information group
        self.informationGroup = QGroupBox(self)
        self.informationGroup.setObjectName(u"jnformationGroup")
        self.informationGroup.setGeometry(QRect(135, 540, 721, 201))
        self.informationGroup.setFont(font)
        # self.informationGroup.setStyleSheet("font-weight: bold;")

        self.sortedIdInput = QLineEdit(self.informationGroup)
        self.sortedIdInput.setObjectName(
            u"paperCatelogIdLineEditInfo")
        self.sortedIdInput.setGeometry(QRect(120, 20, 101, 31))
        self.sortedIdInput.setReadOnly(True)
        self.sortedIdInput.setStyleSheet(u"background-color: grey")

        self.nameInput = QLineEdit(self.informationGroup)
        self.nameInput.setObjectName(u"paperCatelogNameLineEdit")
        self.nameInput.setGeometry(QRect(460, 20, 231, 31))

        self.DescInput = QTextEdit(self.informationGroup)
        self.DescInput.setObjectName(u"paperCatelogDescTextEdit")
        self.DescInput.setGeometry(QRect(120, 60, 571, 91))

        self.sortedIdLabel = QLabel(self.informationGroup)
        self.sortedIdLabel.setObjectName(u"paperTypeIdlabel")
        self.sortedIdLabel.setGeometry(QRect(50, 20, 21, 31))
        self.sortedIdLabel.setFont(font)

        self.nameLabel = QLabel(self.informationGroup)
        self.nameLabel.setObjectName(u"paperCatelogNameLabelInfo")
        self.nameLabel.setGeometry(QRect(330, 20, 91, 31))
        self.nameLabel.setFont(font)

        self.descLabel = QLabel(self.informationGroup)
        self.descLabel.setObjectName(u"paperTypeDescLabel")
        self.descLabel.setGeometry(QRect(20, 90, 91, 31))
        self.descLabel.setFont(font)

        # horizontal layout
        self.horizontalLayoutWidget = QWidget(self.informationGroup)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(170, 160, 350, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(50)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # add button
        self.addBtn = QPushButton(self.horizontalLayoutWidget)
        self.addBtn.setObjectName(u"paperCatelogAddLabel")
        self.addBtn.setFont(font)
        icon = QIcon()
        icon.addFile(u"./images/add.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.addBtn.setIcon(icon)

        self.horizontalLayout.addWidget(self.addBtn)

        # delete button
        self.deleteBtn = QPushButton(self.horizontalLayoutWidget)
        self.deleteBtn.setObjectName(u"paperCatelogDeleteLabel")
        self.deleteBtn.setFont(font)
        icon1 = QIcon()
        icon1.addFile(u"./images/delete.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.deleteBtn.setIcon(icon1)

        self.horizontalLayout.addWidget(self.deleteBtn)

        # modify button
        self.modifyBtn = QPushButton(self.horizontalLayoutWidget)
        self.modifyBtn.setObjectName(u"paperCatelogModifyLabel")
        self.modifyBtn.setFont(font)
        icon2 = QIcon()
        icon2.addFile(u"./images/modify.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.modifyBtn.setIcon(icon2)

        self.horizontalLayout.addWidget(self.modifyBtn)

        # ? information table
        self.catelogTable = QTableWidget(self)
        self.catelogTable.setObjectName(u"paperCatelogTable")
        self.catelogTable.setGeometry(QRect(135, 110, 721, 411))
        self.catelogTable.setShowGrid(False)   # hide grid
        self.catelogTable.setStyleSheet(
            "QTableWidget { border: none; }")  # hide border
        self.catelogTable.verticalHeader().setVisible(False)  # hide vertical header
        self.catelogTable.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)  # disable edit
        self.catelogTable.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # expanding
        self.catelogTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)  # stretch header
        self.catelogTable.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)  # select rows

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Manage catelog information ", None))
        self.searchGroup.setTitle(
            QCoreApplication.translate("MainWindow", u"Search", None))
        self.searchLabel.setText(
            QCoreApplication.translate("MainWindow", u"Catelog", None))
        self.searchBtn.setText(
            QCoreApplication.translate("MainWindow", u"Search", None))
        self.informationGroup.setTitle(
            QCoreApplication.translate("MainWindow", u"Information", None))
        self.sortedIdLabel.setText(
            QCoreApplication.translate("MainWindow", u"ID", None))
        self.nameLabel.setText(
            QCoreApplication.translate("MainWindow", u"Catelog", None))
        self.descLabel.setText(
            QCoreApplication.translate("MainWindow", u"Description", None))
        self.deleteBtn.setText(
            QCoreApplication.translate("MainWindow", u"Delete", None))
        self.modifyBtn.setText(
            QCoreApplication.translate("MainWindow", u"Modify", None))
        self.addBtn.setText(
            QCoreApplication.translate("MainWindow", u"Add", None))

    def initCatelogTable(self, fuzzyTypeName=""):
        # reset the sortedId
        self.sortCatelog()

        catelogList = paperCatelogDao.getPaperCatelogFromFuzzyName(
            fuzzyTypeName)
        row = len(catelogList) if catelogList else 0

        self.catelogTable.setColumnCount(3)
        self.catelogTable.setRowCount(row)
        self.catelogTable.setHorizontalHeaderLabels(
            ['id', 'name', 'description'])

        for i in range(row):
            sortedId = QTableWidgetItem(str(catelogList[i][1]))
            catelogName = QTableWidgetItem(str(catelogList[i][2]))
            catelogDesc = QTableWidgetItem(str(catelogList[i][3]))
            self.catelogTable.setItem(i, 0, sortedId)
            self.catelogTable.setItem(i, 1, catelogName)
            self.catelogTable.setItem(i, 2, catelogDesc)

    def searchBtnClicked(self):
        fuzzyTypeName = self.searchInput.text()
        self.initCatelogTable(fuzzyTypeName)

    def showInfo(self, index: QModelIndex):
        rowIndex = index.row()
        sortedId = self.catelogTable.item(rowIndex, 0).text()
        catelogName = self.catelogTable.item(rowIndex, 1).text()
        catelogDesc = self.catelogTable.item(rowIndex, 2).text()
        self.sortedIdInput.setText(sortedId)
        self.nameInput.setText(catelogName)
        self.DescInput.setText(catelogDesc)

    def sortCatelog(self):
        # get all catelog from database
        catelogList = paperCatelogDao.getPaperCatelogFromFuzzyName()

        if not catelogList:
            return

        # reset the sortedId
        sortedCatelogList = sorted(catelogList, key=lambda x: x[1])

        totalCatelog = len(catelogList)
        for i in range(totalCatelog):
            catelog = PaperCatelog(
                i, sortedCatelogList[i][2], sortedCatelogList[i][3])
            catelog.id_construct(sortedCatelogList[i][0])
            paperCatelogDao.modityPaperCatelogFromId(catelog)

    def resetInfo(self):
        self.catelogTable.clearSelection()
        self.sortedIdInput.clear()
        self.nameInput.clear()
        self.DescInput.clear()

    def addBtnClicked(self):
        catelogName = self.nameInput.text().strip()
        catelogDesc = self.DescInput.toPlainText().strip()
        if catelogName == "":
            QMessageBox.warning(
                self, "warning", "catelog name can not be empty")
            return

        # get all catelog from database
        catelogList = paperCatelogDao.getPaperCatelogFromFuzzyName()

        sortedId = len(catelogList) if catelogList else 0

        # add new catelog to database
        newCatelog = PaperCatelog(sortedId, catelogName, catelogDesc)

        if not paperCatelogDao.addPaperCatelog(newCatelog):
            QMessageBox.information(
                self, "warning", "failed to add catelog, may be there are the same name in the database, please try again")
            return

        QMessageBox.information(self, "info", "add catelog success")
        self.initCatelogTable()
        
        self.resetInfo()

    def tableClicked(self):
        if self.sortedIdInput.text().strip() == "":
            QMessageBox.information(self, "info", "please select a catelog")
            return
        sortedId = self.sortedIdInput.text().strip()
        catelogName = self.nameInput.text().strip()
        catelogDesc = self.DescInput.toPlainText().strip()
        catelog = PaperCatelog(sortedId, catelogName, catelogDesc)
        if not paperCatelogDao.modityPaperCatelogFromSortedId(catelog):
            QMessageBox.information(
                self, "warning", "failed to modify catelog, please try again")
            return
        QMessageBox.information(self, "info", "modify catelog success")
        self.initCatelogTable()
        
        self.resetInfo()

    def delBtnClicked(self):
        sortedId = self.sortedIdInput.text().strip()

        if sortedId == "":
            QMessageBox.information(self, "info", "please select a catelog")
            return

        # get the each paper for current catelog
        papers = paperDao.getPaperFromPaperCatelogId(sortedId)

        for paper in papers:

            # paper info
            folderPath = paper.folderPath
            fileName = paper.fileName
            paperName = paper.paperName

            # delete paper from database
            if not paperDao.delPaperFromId(paper):
                QMessageBox.information(
                    self, "warning", f"delete database record for paper - {paperName} failed")
                continue

            # delete the file from disk
            if (not folderPath) or (not fileName):
                continue

            filePath = os.path.join(folderPath, fileName)

            if os.path.exists(filePath):
                try:
                    os.remove(filePath)
                except Exception as e:
                    QMessageBox.information(
                        self, "warning", f"delete file from disk for paper - {paperName} failed - {e}")
                    continue

        # delete catelog from database
        if not paperCatelogDao.delPaperCatelogFromSortedId(sortedId, True):
            QMessageBox.information(
                self, "warning", "delete failed, please try again")
            return

        QMessageBox.information(self, "info", "delete success")
        
        self.initCatelogTable()
        
        self.resetInfo()

    def closeEvent(self, event):
        self.closeSignal.emit()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = PaperCatelogManageWidget()
    main.show()

    sys.exit(app.exec())
