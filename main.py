from PySide6 import QtCore
from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize)
from PySide6.QtGui import (QAction, QIcon)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QWidget, QMenu, QMenuBar, QLabel, QStatusBar, QStackedWidget)
from chat.chatWidget import ChatWidget
from paper.paperManageWidget import PaperManageWidget
from settingPage.paperCatelogManageWidget import PaperCatelogManageWidget
from settingPage.gptSetting.gptSettingWidget import GptSettingWidget
import sys
import os
from util.dbUtil import initDb, DB_NAME

PDF_DIRECTORY = "./pdfFiles"


class MainWindow_(QMainWindow):

    def __init__(self):
        super(MainWindow_, self).__init__()
        # fixed window size
        self.setWindowFlag(QtCore.Qt.WindowType.MSWindowsFixedSizeDialogHint)

        # set up the user interface from Designer
        self.setupUi()

        # menu widget
        self.paperManageWidget = PaperManageWidget()
        self.chatWidget = ChatWidget()

        # set up the central widget
        self.stack = QStackedWidget()
        self.stack.addWidget(self.paperManageWidget)
        self.stack.addWidget(self.chatWidget)

        # self.stack.setCurrentWidget(self.paperManage)
        self.setCentralWidget(self.stack)

        # init setting widget
        self.paperCatelogManageWidget: QWidget = PaperCatelogManageWidget()
        self.gptSettingWidget: QWidget = GptSettingWidget()

        # ! menu connect action
        self.chatMenu.aboutToShow.connect(
            lambda: self.stack.setCurrentWidget(self.chatWidget))
        self.paperMenu.aboutToShow.connect(
            lambda: self.stack.setCurrentWidget(self.paperManageWidget))

        # ! paper catelog manage connect action
        self.paperCatelogManageWidget.closeSignal.connect(
            self.paperManageWidget.initPaperCatelogCbx)

        # ! menu setting connect action
        self.settingMenu.triggered.connect(self.openSettingPage)

    def setupUi(self):
        self.resize(1000, 800)

        # ? menu bar
        self.menubar = QMenuBar(self)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 22))
        self.setMenuBar(self.menubar)

        # ? menu
        # GPT
        self.chatMenu = QMenu(self.menubar)
        self.chatMenu.setObjectName(u"chatMenu")

        # database
        self.paperMenu = QMenu(self.menubar)
        self.paperMenu.setObjectName(u"paperMenu")

        # setting
        self.settingMenu = QMenu(self.menubar)
        self.settingMenu.setObjectName(u"settingMenu")

        # ? action
        # GPT setting
        self.gptSetting = QAction(self)
        self.gptSetting.setObjectName(u"gptSetting")
        icon = QIcon()
        icon.addFile(u"./images/Setting1.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.gptSetting.setIcon(icon)

        # manage paper type information
        self.paperCatelogManage = QAction(self)
        self.paperCatelogManage.setObjectName(
            u"paperCatelogManage")
        icon = QIcon()
        icon.addFile(u"./images/manage.png", QSize(), QIcon.Normal, QIcon.Off)
        self.paperCatelogManage.setIcon(icon)

        # ? add action to menu
        # menuebar add menu
        self.menubar.addAction(self.chatMenu.menuAction())
        self.menubar.addAction(self.paperMenu.menuAction())
        self.menubar.addAction(self.settingMenu.menuAction())

        # menu setting add action
        self.settingMenu.addAction(self.paperCatelogManage)
        self.settingMenu.addAction(self.gptSetting)

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
        self.gptSetting.setText(QCoreApplication.translate(
            "MainWindow", u"Gpt Setting", None))
        self.paperCatelogManage.setText(QCoreApplication.translate(
            "MainWindow", u"Catelog Manage", None))
        self.chatMenu.setTitle(
            QCoreApplication.translate("MainWindow", u"Chat", None))
        self.paperMenu.setTitle(
            QCoreApplication.translate("MainWindow", u"Paper", None))
        self.settingMenu.setTitle(
            QCoreApplication.translate("MainWindow", u"Setting", None))

    def openSettingPage(self, m):
        if m.text() == "Catelog Manage":
            self.paperCatelogManageWidget.show()
        if m.text() == "Gpt Setting":
            self.gptSettingWidget.show()


if __name__ == "__main__":

    if not os.path.exists(DB_NAME):
        try:
            initDb(DB_NAME)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"init db error: {str(e)}")

    app = QApplication(sys.argv)

    main = MainWindow_()
    main.show()

    sys.exit(app.exec())
