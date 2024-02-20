import os
from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize)
from PySide6.QtGui import (QAction, QIcon)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QMenu, QMenuBar, QLabel, QStatusBar, QStackedWidget)
from paper.paperManageWidget import PaperManageWidget
from settingPage.paperCatelogManageWidget import PaperCatelogManageWidget
from settingPage.gptSetting.gptSettingWidget import GptSettingWidget

PDF_DIRECTORY = "./pdfFiles"


class MainWindow_(QMainWindow):

    def __init__(self):
        super(MainWindow_, self).__init__()
        # fixed window size
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)


        # set up the user interface from Designer
        self.setupUi()

        # set up the central widget
        self.stack = QStackedWidget()

        self.paperManage = PaperManageWidget()

        self.stack.addWidget(self.paperManage)
        self.stack.setCurrentWidget(self.paperManage)

        self.setCentralWidget(self.stack)

        # init setting widget
        self.paperCatelogManage: QWidget = PaperCatelogManageWidget()
        self.gptSetting: QWidget = GptSettingWidget()
        self.paperCatelogManage.closeSignal.connect(self.paperManage.initPaperCatelogCbx)

    def setupUi(self):
        self.resize(1000, 800)

        # ? menu bar
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        self.setMenuBar(self.menubar)

        # ? menu
        # GPT
        self.menuGpt = QMenu(self.menubar)
        self.menuGpt.setObjectName(u"menuGpt")

        # database
        self.menuDataBase = QMenu(self.menubar)
        self.menuDataBase.setObjectName(u"menuDataBase")

        # setting
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        # self.menuSETTING.setSeparatorsCollapsible(False)
        # self.menuSETTING.setToolTipsVisible(True)

        # ? action
        # GPT setting
        self.GPT_SETTING = QAction(self)
        self.GPT_SETTING.setObjectName(u"GptSetting")
        icon = QIcon()
        icon.addFile(u"./images/Setting1.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.GPT_SETTING.setIcon(icon)

        # manage paper type information
        self.paperTypeInfoManage = QAction(self)
        self.paperTypeInfoManage.setObjectName(
            u"paper_type_information_manage")
        icon = QIcon()
        icon.addFile(u"./images/manage.png", QSize(), QIcon.Normal, QIcon.Off)
        self.paperTypeInfoManage.setIcon(icon)

        # ? add action to menu
        # menuebar add menu
        self.menubar.addAction(self.menuGpt.menuAction())
        self.menubar.addAction(self.menuDataBase.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())

        # menu setting add action
        self.menuSetting.addAction(self.paperTypeInfoManage)
        self.menuSetting.addAction(self.GPT_SETTING)

        # ! menu setting connect action
        self.menuSetting.triggered.connect(self.openSettingPage)

        # ? status bar
        statusbar_label = QLabel("status bar")
        statusbar_label.setText(
            "author: gchen | email: gchenn@mail.ustc.edu.cn")
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.addWidget(statusbar_label)
        self.setStatusBar(self.statusbar)

        # ? others
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            QCoreApplication.translate("MainWindow", u"GPaper", None))

        # bar
        self.GPT_SETTING.setText(QCoreApplication.translate(
            "MainWindow", u"Gpt Setting", None))
        self.paperTypeInfoManage.setText(QCoreApplication.translate(
            "MainWindow", u"Catelog Information Manage", None))
        self.menuGpt.setTitle(
            QCoreApplication.translate("MainWindow", u"GPT", None))
        self.menuDataBase.setTitle(
            QCoreApplication.translate("MainWindow", u"DATABASE", None))
        self.menuSetting.setTitle(
            QCoreApplication.translate("MainWindow", u"SETTING", None))

    def openSettingPage(self, m):
        if m.text() == "Catelog Information Manage":
            self.paperCatelogManage.show()
        if m.text() == "Gpt Setting":
            self.gptSetting.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = MainWindow_()
    main.show()

    sys.exit(app.exec())
