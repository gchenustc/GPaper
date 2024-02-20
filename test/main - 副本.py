import os
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Signal, Slot, QThread, Signal, QRunnable, QThreadPool, QObject)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
                           QCursor, QFont, QFontDatabase, QGradient,
                           QIcon, QImage, QKeySequence, QLinearGradient,
                           QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform, QStandardItemModel)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
                               QLabel, QSizePolicy, QStatusBar, QWidget,  QTabWidget, QTreeView, QAbstractItemView, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox, QListWidget, QListWidgetItem, QStackedWidget, QRadioButton, QCheckBox, QButtonGroup, QSpinBox, QDoubleSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit, QDial, QScrollBar, QSlider, QProgressBar, QCommandLinkButton, QToolButton, QStyleFactory, QTextEdit, QPlainTextEdit, QTextBrowser, QLineEdit, QSpinBox, QDoubleSpinBox, QFontComboBox, QSizePolicy, QSlider, QScrollBar, QProgressBar, QInputDialog, QHeaderView, QFileDialog, QProgressDialog)

from paperType import paperTypeManage
from dao import paperCatelogDao, paperDao
from entity.paperModel import Paper
from entity.paperCatelogModel import PaperCatelog
from main_.threadWork import QThreadWorker
from paper.paperTableOperation import initPaperTable, paperTableHeaderClicked, adjustPaperTableColumn, OperatedCellWidget, getRowCheckedState, getRowItem, paperTableCellChanged
from util import osUtil
from func_timeout import func_timeout, FunctionTimedOut

PDF_DIRECTORY = "./pdfFiles"


class GPaperMainWindow(QMainWindow):
    UPDATA_PROGRESS_SIGNAL = Signal(int)
    PAPER_TABLE_INIT_SIGNAL = Signal()

    def __init__(self):
        super(GPaperMainWindow, self).__init__()
        # fixed window size
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)

        # set up the user interface from Designer
        self.setupUi()

        # init paper type combobox - for select paper type
        self.initPaperTypeCbx()

        # ! paper type combobox signal
        self.paperTypeCbx.currentTextChanged.connect(
            lambda text: self.paperTypeCbxChanged(text))

        initPaperTable(self)

        self.importThreadPool = QThreadPool()

        self.UPDATA_PROGRESS_SIGNAL.connect(self.updataProgressDialog)
        self.PAPER_TABLE_INIT_SIGNAL.connect(lambda: initPaperTable(self))

    def setupUi(self):
        self.resize(1000, 800)

        # ? menu bar
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        self.setMenuBar(self.menubar)

        # ? menu
        self.menuGpt = QMenu(self.menubar)
        self.menuGpt.setObjectName(u"menuGpt")

        self.menuDataBase = QMenu(self.menubar)
        self.menuDataBase.setObjectName(u"menuDataBase")

        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        icon = QIcon()
        icon.addFile(u"./images/Setting.png", QSize(), QIcon.Normal, QIcon.Off)
        self.menuSetting.setIcon(icon)
        # self.menuSETTING.setSeparatorsCollapsible(False)
        # self.menuSETTING.setToolTipsVisible(True)

        self.menuPaper_type = QMenu(self.menuDataBase)
        self.menuPaper_type.setObjectName(u"menupaper_type")
        icon = QIcon()
        icon.addFile(u"./images/bookshelf.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.menuPaper_type.setIcon(icon)

        # database - child menu
        # ? action
        # GPT setting
        self.GPT_SETTING = QAction(self)
        self.GPT_SETTING.setObjectName(u"GPT_SETTING")
        icon = QIcon()
        icon.addFile(u"./images/Setting1.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.GPT_SETTING.setIcon(icon)

        # manage paper type information
        self.paper_type_information_manage = QAction(self)
        self.paper_type_information_manage.setObjectName(
            u"paper_type_information_manage")
        icon = QIcon()
        icon.addFile(u"./images/manage.png", QSize(), QIcon.Normal, QIcon.Off)
        self.paper_type_information_manage.setIcon(icon)

        # ? add action to menu
        # menuebar add menu
        self.menubar.addAction(self.menuGpt.menuAction())
        self.menubar.addAction(self.menuDataBase.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        # menu database add action
        self.menuDataBase.addAction(self.menuPaper_type.menuAction())
        self.menuPaper_type.addAction(self.paper_type_information_manage)

        self.menuSetting.addAction(self.GPT_SETTING)

        # ? status bar
        statusbar_label = QLabel("status bar")
        statusbar_label.setText(
            "author: gchen | email: gchenn@mail.ustc.edu.cn")
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.addWidget(statusbar_label)
        self.setStatusBar(self.statusbar)

        # ? central widget
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        # self.centralwidget.setStyleSheet(
        #     "border-image: url(./images/blue_background.png)")
        self.setCentralWidget(self.centralwidget)

        self.paperTypeLabel = QLabel(self)
        self.paperTypeLabel.setObjectName(u"paperTypeLabel")
        self.paperTypeLabel.setGeometry(QRect(20, 45, 71, 21))
        self.paperTypeLabel.setStyleSheet("font-weight: bold;")

        self.paperTypeCbx = QComboBox(self)
        self.paperTypeCbx.setObjectName(u"PaperTypeCbx")
        self.paperTypeCbx.setGeometry(QRect(90, 40, 101, 32))

        self.paperNameLineEdit = QLineEdit(self)
        self.paperNameLineEdit.setObjectName(u"PaperNameLineEdit")
        self.paperNameLineEdit.setGeometry(QRect(200, 40, 191, 32))

        self.searchBtn = QPushButton(self)
        self.searchBtn.setObjectName(u"searchBtn")
        self.searchBtn.setGeometry(QRect(410, 43, 75, 28))
        self.searchBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 5px; font-weight: bold;")

        # ! search button signal
        self.searchBtn.clicked.connect(self.on_searchBtnClicked)

        self.deleteBtn = QPushButton(self)
        self.deleteBtn.setObjectName(u"deleteBtn")
        self.deleteBtn.setGeometry(QRect(545, 43, 70, 28))
        self.deleteBtn.setStyleSheet(
            "color: white; background-color: rgb(255, 100, 70); border-radius: 5px; font-weight: bold;")
        self.deleteBtn.setIcon(QIcon("./images/delete.png"))

        # ! delete button signal
        self.deleteBtn.clicked.connect(self.on_delPaper)

        self.createNewBtn = QPushButton(self)
        self.createNewBtn.setObjectName(u"createNewBtn")
        self.createNewBtn.setGeometry(QRect(625, 43, 110, 28))
        self.createNewBtn.setStyleSheet(
            "color: white; background-color: rgb(46, 139, 87); border-radius: 5px; font-weight: bold;")
        self.createNewBtn.setIcon(QIcon("./images/add.png"))

        # ! create new button signal
        self.createNewBtn.clicked.connect(self.on_createNewPaper)

        self.importPdfBtn = QPushButton(self)
        self.importPdfBtn.setObjectName(u"importPdfBtn")
        self.importPdfBtn.setGeometry(QRect(745, 43, 100, 28))
        self.importPdfBtn.setStyleSheet(
            "color: white; background-color: rgb(46, 139, 87); border-radius: 5px; font-weight: bold;")
        self.importPdfBtn.setIcon(QIcon("./images/pdf.png"))

        # ! import pdf button signal
        self.importPdfBtn.clicked.connect(self.on_importPdf)

        self.ImportFolderBtn = QPushButton(self)
        self.ImportFolderBtn.setObjectName(u"ImportFolderBtn")
        self.ImportFolderBtn.setGeometry(QRect(855, 43, 115, 28))
        self.ImportFolderBtn.setStyleSheet(
            "color: white; background-color: rgb(46, 139, 87); border-radius: 5px; font-weight: bold;")
        self.ImportFolderBtn.setIcon(QIcon("./images/folder.png"))

        # ! import folder button signal
        self.ImportFolderBtn.clicked.connect(self.on_importFolder)

        # ?  paper table widget
        self.paperTable = QTableWidget(self.centralwidget)
        self.paperTable.setObjectName(u"listWidget")
        self.paperTable.setGeometry(QRect(20, 70, 960, 640))

        headerLabels = ['✓', 'Paper Name',
                        'Title', 'Author', 'Journal', 'Date', 'Operate']
        column = len(headerLabels)

        self.paperTable.setColumnCount(column)  # column

        # set header
        self.paperTable.setHorizontalHeaderLabels(
            headerLabels)  # create header
        self.paperTable.setColumnWidth(0, 20)
        self.paperTable.setColumnWidth(1, 165)
        self.paperTable.setColumnWidth(2, 180)
        self.paperTable.setColumnWidth(3, 150)
        self.paperTable.setColumnWidth(4, 150)
        self.paperTable.setColumnWidth(6, 170)
        # self.paperTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.paperTable.horizontalHeader().setSectionsMovable(True)
        self.paperTable.totalWidth = sum(self.paperTable.columnWidth(
            i) for i in range(self.paperTable.columnCount()))

        # ! paper table cell changed signal
        self.paperTable.cellChanged.connect(
            lambda row, column: paperTableCellChanged(self, row, column))

        # ! set paper table size changed signal
        self.paperTable.horizontalHeader().sectionResized.connect(lambda index: adjustPaperTableColumn(
            self, index))  # keep the total width of the table dischanged

        # set header checkbox initial state
        self.paperTable.horizontalHeaderItem(0).setFlags(
            Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.paperTable.horizontalHeaderItem(0).setCheckState(Qt.Unchecked)
        self.paperTable.horizontalHeader().sectionClicked.connect(
            lambda index: paperTableHeaderClicked(self, index))

        self.connectPdfBtn = QPushButton(self)
        self.connectPdfBtn.setObjectName(u"extractSourceBtn")
        self.connectPdfBtn.setGeometry(QRect(570, 750, 90, 28))
        self.connectPdfBtn.setStyleSheet(
            "color: white; background-color: rgb(46, 139, 87); border-radius: 5px; font-weight: bold;")

        # ! connect pdf button signal
        self.connectPdfBtn.clicked.connect(self.on_connectPdf)

        self.extractSourceBtn = QPushButton(self)
        self.extractSourceBtn.setObjectName(u"extractSourceBtn")
        self.extractSourceBtn.setGeometry(QRect(680, 750, 122, 28))
        self.extractSourceBtn.setStyleSheet(
            "color: white; background-color: rgb(0, 190, 200); border-radius: 5px; font-weight: bold;")

        # ! extract source button signal
        self.extractSourceBtn.clicked.connect(self.on_extractSource)

        self.vectorizeBtn = QPushButton(self)
        self.vectorizeBtn.setObjectName(u"vectorizeBtn")
        self.vectorizeBtn.setGeometry(QRect(820, 750, 71, 28))
        self.vectorizeBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 5px; font-weight: bold;")

        self.GptChatBtn = QPushButton(self)
        self.GptChatBtn.setObjectName(u"GptChatBtn")
        self.GptChatBtn.setGeometry(QRect(910, 750, 71, 28))
        self.GptChatBtn.setStyleSheet(
            "color: white; background-color: rgb(123, 104, 238); border-radius: 5px; font-weight: bold;")

        """
        # vertical layout
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 21, 151, 759))
        self.verticalLayoutWidget.setStyleSheet(
            "border-image: url(./images/blue_background.png)")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(50)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # ? tree nevigation
        self.treeNevigation = QTreeWidget(self.verticalLayoutWidget)
        self.treeNevigation.setObjectName(u"treeNevigation")
        self.treeNevigation.setGeometry(QRect(0, 21, 151, 500))
        self.treeNevigation.setSortingEnabled(True)
        self.treeNevigation.setAnimated(True)
        self.treeNevigation.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # expanding
        self.treeNevigation.setStyleSheet(
            "QTableWidget { border: none; }")  # hide border
        self.treeNevigation.setHeaderLabels(['Sort'])
        self.treeNevigation.setRootIsDecorated(False)

        self.verticalLayout.addWidget(self.treeNevigation)
        """

        # ? others
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        # ! menu DataBase signal
        self.menuDataBase.triggered.connect(self.openDataBaseWidget)

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"GPaper", None))

        # bar
        self.GPT_SETTING.setText(QCoreApplication.translate(
            "MainWindow", u"GPT SETTING", None))
        self.paper_type_information_manage.setText(QCoreApplication.translate(
            "MainWindow", u"Catelog information manage", None))
        self.menuGpt.setTitle(
            QCoreApplication.translate("MainWindow", u"GPT", None))
        self.menuDataBase.setTitle(
            QCoreApplication.translate("MainWindow", u"DATABASE", None))
        self.menuPaper_type.setTitle(
            QCoreApplication.translate("MainWindow", u"Catelog", None))
        self.menuSetting.setTitle(
            QCoreApplication.translate("MainWindow", u"SETTING", None))

        # main
        self.paperTypeLabel.setText(QCoreApplication.translate(
            "MainWindow", u"Catelog", None))
        self.searchBtn.setText(QCoreApplication.translate(
            "MainWindow", u"search", None))
        self.deleteBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Delete", None))
        self.createNewBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Create New", None))
        self.importPdfBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Import PDF", None))
        self.ImportFolderBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Import Folder", None))
        self.connectPdfBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Connect PDF", None))
        self.extractSourceBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Extract Source Data", None))
        self.vectorizeBtn.setText(QCoreApplication.translate(
            "MainWindow", u"Vectorize", None))
        self.GptChatBtn.setText(QCoreApplication.translate(
            "MainWindow", u"GPT Chat", None))

    def openDataBaseWidget(self, m):
        if m.text() == "Catelog information manage":
            self.paperTypeManage: QMainWindow = paperTypeManage.PaperTypeManage()
            self.paperTypeManage.closeSignal.connect(self.initPaperTypeCbx)
            self.paperTypeManage.show()

    def initPaperTypeCbx(self):

        self.paperTypeCbx.clear()

        _paperTypeList = paperCatelogDao.getPaperCatelogFromFuzzyName()
        paperTypeList = sorted(_paperTypeList, key=lambda x: x[3])

        if not paperTypeList:
            return

        for item in paperTypeList:
            self.paperTypeCbx.addItem(item[1])

        self.paperTypeCbx.show()

    def paperTypeCbxChanged(self, text):
        self.paperTypeCbx.blockSignals(True)

        # get all paper Type from database
        paperTypeList = paperCatelogDao.getPaperCatelogFromFuzzyName()

        for paperTypeInfo in paperTypeList:
            if paperTypeInfo[1] == text:
                paperType = PaperCatelog(
                    paperTypeInfo[1], paperTypeInfo[2], 0)
            else:
                paperType = PaperCatelog(
                    paperTypeInfo[1], paperTypeInfo[2], paperTypeInfo[3] + 1)
            paperType.id_construct(paperTypeInfo[0])
            try:
                paperCatelogDao.modityPaperCatelogFromId(paperType)
            except Exception as e:
                QMessageBox.critical(
                    None, "Error", f"Failed to modify paper type - {paperType.catelogName} - {e}")

        self.initPaperTypeCbx()
        initPaperTable(self)

        self.paperTypeCbx.blockSignals(False)

    def on_createNewPaper(self):
        paperTypeName = self.paperTypeCbx.currentText()
        if not paperTypeName:
            QMessageBox.information(
                self, "information", "please create a catelog first")
            return

        text, ok = QInputDialog.getText(
            self, "input dialog", "please input paper name")
        if (not ok) or (not text):
            return

        paperTypeId = paperCatelogDao.getPaperCatelogFromName(paperTypeName)[
            0][0]
        newPaperName = text

        paper = Paper(paperName=newPaperName, paperCatelogId=paperTypeId)

        if paperDao.addPaper(paper):
            QMessageBox.information(self, "information", "create success")
            initPaperTable(self)
        else:
            QMessageBox.information(self, "information", "create failed")

    def isPaperTypeExist(self, popUp=False):
        # get the current paper type
        paperTypeName = self.paperTypeCbx.currentText()
        if not paperTypeName:
            if popUp:
                QMessageBox.information(
                    self, "information", "please create a catelog first")
            return False
        return True

    def initProgressDialog(self, totalSteps):
        # create progress dialog
        self.progressDialog = QProgressDialog(
            "processing, waiting...", "cancel", 0, totalSteps, self)
        self.progressDialog.setWindowTitle("processing...")
        self.progressDialog.setWindowModality(Qt.WindowModal)
        self.progressDialog.setSizeGripEnabled(False)
        self.progressDialog.canceled.connect(self.progressDialog.close)
        self.UPDATA_PROGRESS_SIGNAL.emit(0)  # start progress

    @Slot(int)
    def updataProgressDialog(self, step):
        self.progressDialog.setValue(step)
        if step == -1:
            self.progressDialog.close()

    def on_importPdf(self):
        if not self.isPaperTypeExist():
            QMessageBox.information(
                self, "information", "please create a catelog first")
            return

        paperTypeName = self.paperTypeCbx.currentText()

        pdf_path, _ = QFileDialog.getOpenFileName(
            None, "import pdf files", "../", "PDF Files (*.pdf)")

        # if the user cancel the file dialog
        if not pdf_path:
            return

        if self.importPdf(pdf_path, paperTypeName, popUp=True):
            QMessageBox.information(self, "information", "import success")
            initPaperTable(self)

    def importPdf(self, pdf_path, paperTypeName, popUp=False):

        paperTypeId = paperCatelogDao.getPaperCatelogFromName(paperTypeName)[
            0][0]

        # move pdf to dest folder
        destPath = os.path.join(PDF_DIRECTORY, paperTypeName)

        fileName = osUtil.movePdfToDestFolder(pdf_path, destPath)
        if not fileName:
            if popUp:
                QMessageBox.information(
                    self, "information", f"move {pdf_path} to {destPath} failed")
            return False

        paperName = fileName.split('.')[0]

        # extract pdf text
        formattedText = ""
        doi = ""
        try:
            oriText = func_timeout(
                20, lambda: osUtil.pdf2Text(os.path.join(destPath, fileName)))  # 20s timeout
            filteredText = osUtil.filterText(oriText, 2)  # for extract doi
            formattedText = osUtil.filterText(oriText, 4)  # for display
            doi = osUtil.extractDoi(filteredText)
        except FunctionTimedOut as e:
            if popUp:
                QMessageBox.information(
                    self, "information", f"extract {pdf_path} text timeout - {e}")
            return False
        except Exception as e:
            if popUp:
                QMessageBox.information(
                    self, "information", f"extract {pdf_path} text failed - {e}")
            return False

        paper = Paper(paperName=paperName, paperCatelogId=paperTypeId,
                      folderPath=destPath, fileName=fileName, text=formattedText, doi=doi)

        if not paperDao.addPaper(paper):
            if popUp:
                QMessageBox.information(
                    self, "information", f"import {pdf_path} into sqlite failed")
            return False

        return True

    def on_importFolder(self):
        if not self.isPaperTypeExist(popUp=True):
            return

        directoryPath = QFileDialog.getExistingDirectory(
            None,  "select a directory", "../", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        # if the user cancel the file dialog
        if not directoryPath:
            return

        paperTypeName = self.paperTypeCbx.currentText()

        importFolderTotalSteps = len(
            [file for file in os.listdir(directoryPath) if file.endswith(".pdf")])

        self.initProgressDialog(importFolderTotalSteps)

        # create thread
        importFolderWorker = QThreadWorker(
            self.importFolder, directoryPath, paperTypeName)

        # start thread - import pdf
        self.importThreadPool.start(importFolderWorker)

        if self.progressDialog.exec() == 0:
            QMessageBox.information(self, "information", "import complete")

    def importFolder(self, directoryPath, paperTypeName):
        pdf_list = [file for file in os.listdir(
            directoryPath) if file.endswith(".pdf")]
        pdf_path_list = [os.path.join(directoryPath, pdf) for pdf in pdf_list]

        if not pdf_path_list:
            QMessageBox.information(
                self, f"information", "no pdf file in the directory - {directory_path}")
            return

        for idx, pdf_path in enumerate(pdf_path_list):

            if self.progressDialog.wasCanceled():
                print("import folder cancelled")
                break

            self.importPdf(pdf_path, paperTypeName)

            # send signal to update the paper table and progress dialog
            self.PAPER_TABLE_INIT_SIGNAL.emit()
            self.UPDATA_PROGRESS_SIGNAL.emit(idx + 1)

            # debug
            print(os.path.basename(pdf_path), idx + 1, len(pdf_path_list))

        # -1 is the label for the end of the progress
        self.UPDATA_PROGRESS_SIGNAL.emit(-1)

    def on_extractSource(self):
        # get the checked row list
        checkedRowList = getRowCheckedState(self.paperTable)
        if not checkedRowList:
            QMessageBox.information(
                self, "information", "please select as least one paper checkbox first")
            return

        # process dialog's total steps
        extractSourceTotalSteps = len(checkedRowList)

        self.initProgressDialog(extractSourceTotalSteps)

        # create thread
        extractSourceWorker = QThreadWorker(
            self.extractSource, checkedRowList)

        # start thread - import pdf
        self.importThreadPool.start(extractSourceWorker)

        if self.progressDialog.exec() == 0:
            QMessageBox.information(self, "information", "extract complete")

    def extractSource(self, checkedRowList):
        itemDataRoleList = getRowItem(self.paperTable, checkedRowList)

        for idx, itemDataRole in enumerate(itemDataRoleList):
            # from the paperTable'id to get the paper total info
            id = itemDataRole[0]

            paper = paperDao.getPaperFromId(id, True)[0]

            doi = paper.doi
            if not doi:
                # debug
                print(paper.paperName + f"- have doi writted",
                      idx + 1, len(checkedRowList))
                continue

            # get paper info by doi
            paperInfoDict = osUtil.getArticalInfoByDoi(doi)

            # make the dict elements to string
            for key in paperInfoDict:
                paperInfoDict[key] = str(paperInfoDict[key])

            paper.title = paperInfoDict["title"]
            paper.author = paperInfoDict["author"]
            paper.abstract = paperInfoDict["abstract"]
            paper.journal = paperInfoDict["journal"]
            paper.issue = paperInfoDict["issue"]
            paper.volume = paperInfoDict["volume"]
            paper.page = paperInfoDict["page"]
            paper.date = paperInfoDict["date"]
            paper.url = paperInfoDict["url"]
            paper.issn = paperInfoDict["issn"]
            paper.isReferencedByCount = paperInfoDict["isReferencedByCount"]

            if not paperDao.modifyPaper(paper):
                # debug
                print("modify paper database failed")

            # send signal to update the paper table and progress dialog
            self.PAPER_TABLE_INIT_SIGNAL.emit()
            self.UPDATA_PROGRESS_SIGNAL.emit(idx + 1)

            # debug
            print(paper.paperName, idx + 1, len(checkedRowList))

        # -1 is the label for the end of the progress
        self.UPDATA_PROGRESS_SIGNAL.emit(-1)

    def on_delPaper(self):
        checkedRowList = getRowCheckedState(self.paperTable)
        if not checkedRowList:
            QMessageBox.information(
                self, "information", "please select a paper")
            return

        # reminder the user to confirm the delete operation
        reply = QMessageBox.question(
            self, "warning", "Are you sure to delete the selected paper?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if not reply == QMessageBox.Yes:
            return

        itemDataRoleList = getRowItem(self.paperTable, checkedRowList)

        # delete the paper from database
        for itemDataRole in itemDataRoleList:

            # paper info
            id = itemDataRole[0]
            paper = paperDao.getPaperFromId(id)[0]
            folderPath = paper.folderPath
            fileName = paper.fileName
            paperName = paper.paperName

            # delete the paper from database
            if not paperDao.delPaperFromId(id):
                QMessageBox.warning(
                    self, "error", f"delete database record for paper - {paperName} failed")
                continue

            initPaperTable(self)

            # delete the file from disk
            if (not folderPath) or (not fileName):
                continue

            filePath = os.path.join(folderPath, fileName)

            if os.path.exists(filePath):
                try:
                    os.remove(filePath)
                except Exception as e:
                    QMessageBox.warning(
                        self, "error", f"delete file from desk for paper - {paperName} failed - {e}")
                    continue

    def on_connectPdf(self):
        # get the checked row list
        checkedRowList = getRowCheckedState(self.paperTable)
        if len(checkedRowList) != 1:
            QMessageBox.information(
                self, "information", "please select only one paper checkbox first")
            return

        paperId = getRowItem(self.paperTable, checkedRowList)[0][0]

        paper = paperDao.getPaperFromId(paperId)[0]
        folderPath = paper.folderPath
        fileName = paper.fileName

        if folderPath and fileName:
            # ask the user if continue
            reply = QMessageBox.question(
                self, "warning", "This paper haspdf file connected, are you sure to connect another?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return

        pdf_path, _ = QFileDialog.getOpenFileName(
            None, "import pdf files", "../", "PDF Files (*.pdf)")

        folderPath = os.path.dirname(pdf_path)
        fileName = os.path.basename(pdf_path)

        paper.folderPath = folderPath
        paper.fileName = fileName

        reply = QMessageBox.question(
            self, "warning", "if to extract the current pdf text to replace the original text content?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                oriText = func_timeout(
                    20, lambda: osUtil.pdf2Text(pdf_path))
                filteredText = osUtil.filterText(oriText, 2)  # for extract doi
                formattedText = osUtil.filterText(oriText, 4)  # for display
                doi = osUtil.extractDoi(filteredText)
            except FunctionTimedOut as e:
                QMessageBox.information(
                    self, "information", f"extract {pdf_path} text timeout - {e}")
                return
            except Exception as e:
                QMessageBox.information(
                    self, "information", f"extract {pdf_path} text failed - {e}")
                return
            paper.text = formattedText

            if doi:
                paper.doi = doi

        if not paperDao.modifyPaper(paper):
            QMessageBox.information(self, "information", "connect pdf failed")
            return

        QMessageBox.information(self, "information", "connect pdf success")

    def on_searchBtnClicked(self):
        fuzzyInfo = self.paperNameLineEdit.text()
        initPaperTable(self, fuzzyInfo)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = GPaperMainWindow()
    main.show()

    sys.exit(app.exec())
