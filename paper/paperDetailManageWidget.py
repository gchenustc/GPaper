from PySide6.QtCore import (Signal, QCoreApplication, QMetaObject, QRect,
                            QSize)
from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (
    QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QVBoxLayout, QWidget)
from dao import paperDao


class PaperDetailManageWidget(QWidget):
    editChangedSignal = Signal()

    def __init__(self, paperTable=None, paperId=-1):
        super().__init__()

        self.paperTable = paperTable
        self.paperId = paperId

        self.setupUi()

        self.confirmBtn.clicked.connect(self.confrimBtnClicked)
        
        self.inputDict = {"abstract": self.abstractTextEdit, "paperName": self.paperNameLineEdit, "title": self.titleLineEdit, "author": self.authorLineEdit, "journal": self.journalLineEdit, "issue": self.issueLineEdit,
                         "volume": self.volumeLineEdit, "page": self.pageLineEdit, "date": self.dateLineEdit, "url": self.urlLineEdit, "doi": self.doiLineEdit, "issn": self.issnLineEdit, "isReferencedByCount": self.isReferenceByCountLineEdit}
        
        self.initPaperDetail()

    def setupUi(self):
        lineEditHight = 25

        self.setObjectName(u"Form")
        self.resize(1000, 760)
        self.abstractTextEdit = QTextEdit(self)
        self.abstractTextEdit.setObjectName(u"abstractTextEdit")
        self.abstractTextEdit.setGeometry(QRect(111, 30, 849, 230))

        self.abstractLabel = QLabel(self)
        self.abstractLabel.setObjectName(u"abstractLabel")
        self.abstractLabel.setGeometry(QRect(20, 120, 51, 31))

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 270, 81, 441))

        self.labelVerticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.labelVerticalLayout.setSpacing(0)
        self.labelVerticalLayout.setObjectName(u"labelVerticalLayout")
        self.labelVerticalLayout.setContentsMargins(0, 0, 0, 0)

        self.paperNameLabel = QLabel(self.verticalLayoutWidget)
        self.paperNameLabel.setObjectName(u"paperNameLabel")

        self.labelVerticalLayout.addWidget(self.paperNameLabel)

        self.TitleLabel = QLabel(self.verticalLayoutWidget)
        self.TitleLabel.setObjectName(u"TitleLabel")

        self.labelVerticalLayout.addWidget(self.TitleLabel)

        self.authorLabel = QLabel(self.verticalLayoutWidget)
        self.authorLabel.setObjectName(u"authorLabel")

        self.labelVerticalLayout.addWidget(self.authorLabel)

        self.JournalLabel = QLabel(self.verticalLayoutWidget)
        self.JournalLabel.setObjectName(u"JournalLabel")

        self.labelVerticalLayout.addWidget(self.JournalLabel)

        self.IssueLabel = QLabel(self.verticalLayoutWidget)
        self.IssueLabel.setObjectName(u"IssueLabel")

        self.labelVerticalLayout.addWidget(self.IssueLabel)

        self.VolumeLabel = QLabel(self.verticalLayoutWidget)
        self.VolumeLabel.setObjectName(u"VolumeLabel")

        self.labelVerticalLayout.addWidget(self.VolumeLabel)

        self.pageLabel = QLabel(self.verticalLayoutWidget)
        self.pageLabel.setObjectName(u"pageLabel")

        self.labelVerticalLayout.addWidget(self.pageLabel)

        self.dateLabel = QLabel(self.verticalLayoutWidget)
        self.dateLabel.setObjectName(u"dateLabel")

        self.labelVerticalLayout.addWidget(self.dateLabel)

        self.urlLabel = QLabel(self.verticalLayoutWidget)
        self.urlLabel.setObjectName(u"urlLabel")

        self.labelVerticalLayout.addWidget(self.urlLabel)

        self.doiLabel = QLabel(self.verticalLayoutWidget)
        self.doiLabel.setObjectName(u"doiLabel")

        self.labelVerticalLayout.addWidget(self.doiLabel)

        self.issnLabel = QLabel(self.verticalLayoutWidget)
        self.issnLabel.setObjectName(u"issnLabel")

        self.labelVerticalLayout.addWidget(self.issnLabel)

        self.isReferenceLabel = QLabel(self.verticalLayoutWidget)
        self.isReferenceLabel.setObjectName(u"isReferenceLabel")
        self.isReferenceLabel.setWordWrap(True)

        self.labelVerticalLayout.addWidget(self.isReferenceLabel)

        self.verticalLayoutWidget_2 = QWidget(self)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(110, 265, 851, 451))
        self.LineEditVerticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.LineEditVerticalLayout.setSpacing(0)
        self.LineEditVerticalLayout.setObjectName(u"LineEditVerticalLayout")
        self.LineEditVerticalLayout.setContentsMargins(0, 0, 0, 0)

        self.paperNameLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.paperNameLineEdit.setObjectName(u"paperNameLineEdit")
        self.paperNameLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.paperNameLineEdit)

        self.titleLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.titleLineEdit.setObjectName(u"titleLineEdit")
        self.titleLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.titleLineEdit)

        self.authorLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.authorLineEdit.setObjectName(u"authorLineEdit")
        self.authorLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.authorLineEdit)

        self.journalLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.journalLineEdit.setObjectName(u"journalLineEdit")
        self.journalLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.journalLineEdit)

        self.issueLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.issueLineEdit.setObjectName(u"issueLineEdit")
        self.issueLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.issueLineEdit)

        self.volumeLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.volumeLineEdit.setObjectName(u"volumeLineEdit")
        self.volumeLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.volumeLineEdit)

        self.pageLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.pageLineEdit.setObjectName(u"pageLineEdit")
        self.pageLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.pageLineEdit)

        self.dateLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.dateLineEdit.setObjectName(u"dateLineEdit")
        self.dateLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.dateLineEdit)

        self.urlLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.urlLineEdit.setObjectName(u"urlLineEdit")
        self.urlLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.urlLineEdit)

        self.doiLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.doiLineEdit.setObjectName(u"doiLineEdit")
        self.doiLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.doiLineEdit)

        self.issnLineEdit = QLineEdit(self.verticalLayoutWidget_2)
        self.issnLineEdit.setObjectName(u"issnLineEdit")
        self.issnLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.issnLineEdit)

        self.isReferenceByCountLineEdit = QLineEdit(
            self.verticalLayoutWidget_2)
        self.isReferenceByCountLineEdit.setObjectName(u"isReferenceLineEdit")
        self.isReferenceByCountLineEdit.setFixedHeight(lineEditHight)

        self.LineEditVerticalLayout.addWidget(self.isReferenceByCountLineEdit)

        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setObjectName(u"pushButton_2")
        self.confirmBtn.setGeometry(QRect(884, 710, 75, 31))
        icon1 = QIcon()
        icon1.addFile(u"./images/confirm.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.confirmBtn.setIcon(icon1)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate(
            "Form", u"Paper Detail", None))
        self.abstractLabel.setText(
            QCoreApplication.translate("Form", u"Abstract", None))
        self.paperNameLabel.setText(
            QCoreApplication.translate("Form", u"Paper Name", None))
        self.TitleLabel.setText(
            QCoreApplication.translate("Form", u"Title", None))
        self.authorLabel.setText(
            QCoreApplication.translate("Form", u"Author", None))
        self.JournalLabel.setText(
            QCoreApplication.translate("Form", u"Journal", None))
        self.IssueLabel.setText(
            QCoreApplication.translate("Form", u"Issue", None))
        self.VolumeLabel.setText(
            QCoreApplication.translate("Form", u"Volume", None))
        self.pageLabel.setText(
            QCoreApplication.translate("Form", u"Page", None))
        self.dateLabel.setText(
            QCoreApplication.translate("Form", u"Date", None))
        self.urlLabel.setText(QCoreApplication.translate("Form", u"Url", None))
        self.doiLabel.setText(QCoreApplication.translate("Form", u"Doi", None))
        self.issnLabel.setText(
            QCoreApplication.translate("Form", u"Issn", None))
        self.isReferenceLabel.setText(QCoreApplication.translate(
            "Form", u"is reference by count", None))
        self.paperNameLineEdit.setText("")
        self.confirmBtn.setText(
            QCoreApplication.translate("Form", u"confirm", None))

    def initPaperDetail(self):
        paper = paperDao.getPaperFromId(self.paperId)[0]
        for key, editTool in self.inputDict.items():
            editTool.setText(str(getattr(paper, key)))

    def confrimBtnClicked(self):
        paper = paperDao.getPaperFromId(self.paperId)[0]

        for key, editTool in self.inputDict.items():
            try:
                text = editTool.text().strip()
            except AttributeError:
                text = editTool.toPlainText().strip()
            if text:
                setattr(paper, key, text)

        if not paperDao.modifyPaper(paper):
            QMessageBox.critical(
                None, "Error", "Failed to modify paper into database")
            return
        QMessageBox.information(None, "Success", "Modify paper successfully")

        self.editChangedSignal.emit()
