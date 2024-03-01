from PySide6 import QtCore, QtWidgets
from chat.plainTextEditRewite import MyPlainTextEdit
from PySide6.QtGui import QFont, QIcon


class ChatWidgetFrame(QtWidgets.QWidget):

    # def __init__(self, parent=None):
    #     super(ChatWidgetFrame, self).__init__(parent)
    #     self.setupUi()

    def setupUi(self):
        """
            structure:
                mainHorizontalLayout
                    1. leftWidget (leftVerticalLayout)
                            outputWidgetFrame (outputVerticalLayout)
                                    leftScrollArea
                                        scrollAreaWidgetContents (scrollAreaVerticalLayout) 
                            inputHorizontalLayout
                                userInput
                                sendBtn
                            btnHorizontalLayout
                    2. rightWidget
        """

        self.resize(1000, 800)

        # set the background color
        self.setStyleSheet("""
                                background-color: rgb(220, 220, 220);
                            """)

        self.mainHorizontalLayout = QtWidgets.QHBoxLayout(self)

        self.leftWidget = QtWidgets.QWidget(self)
        self.leftWidget.setStyleSheet("""
                                        background-color: rgb(255, 255, 255);
                                        border-radius: 30px;
                                    """)

        self.mainHorizontalLayout.addWidget(self.leftWidget)

        self.leftVerticalLayout = QtWidgets.QVBoxLayout(self.leftWidget)
        self.leftVerticalLayout.setContentsMargins(10, 10, 10, 10)
        self.leftVerticalLayout.setSpacing(20)

        self.outputWidgetFrame = QtWidgets.QFrame(self.leftWidget)
        self.outputWidgetFrame.setStyleSheet("""
                                    background-color: rgb(220, 220, 220);
                                    border-radius:20px;
                                    border:3px solid #34495e;
                                """)
        self.outputWidgetFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outputWidgetFrame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.outputVerticalLayout = QtWidgets.QVBoxLayout(
            self.outputWidgetFrame)

        self.leftScrollArea = QtWidgets.QScrollArea(self.outputWidgetFrame)
        self.leftScrollArea.setStyleSheet("""
                                            border:initial;
                                            border: 0px solid;
                                        """)
        self.leftScrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 958, 598))

        self.scrollAreaVerticalLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents)

        self.leftScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.outputVerticalLayout.addWidget(self.leftScrollArea)

        # * belong to left widget
        self.leftVerticalLayout.addWidget(self.outputWidgetFrame)

        self.inputHorizontalLayout = QtWidgets.QHBoxLayout()

        self.userInput = MyPlainTextEdit(self.outputWidgetFrame)
        self.userInput.setStyleSheet("""
                                        QPlainTextEdit{
                                            border-radius: 20px;
                                            border:3px solid #2c3e50;
                                            background-color: rgb(220, 220, 220);
                                            font: 12pt '微软雅黑';
                                            padding:5px;
                                        }
                                        """)

        self.inputHorizontalLayout.addWidget(self.userInput)

        self.sendBtn = QtWidgets.QPushButton(self)
        self.sendBtn.setStyleSheet("color: white; background-color: rgb(65, 105, 225); border-radius: 10px; font-weight: bold;")
        self.sendBtn.setFixedHeight(40)
        sendFont = QFont()
        sendFont.setPointSize(12)
        self.sendBtn.setFont(sendFont)
        self.sendBtn.setIcon(QIcon("./images/send.png"))

        self.inputHorizontalLayout.addWidget(self.sendBtn)
        self.inputHorizontalLayout.setStretch(0, 8)
        self.inputHorizontalLayout.setStretch(1, 1)

        # * belong to left widget
        self.leftVerticalLayout.addLayout(self.inputHorizontalLayout)
        self.leftVerticalLayout.setStretch(0, 5)
        self.leftVerticalLayout.setStretch(1, 1)

        self.rightWidget = QtWidgets.QWidget(self)
        self.rightWidget.setStyleSheet("""
                                        background-color: rgb(255, 255, 255);
                                        border-radius: 30px;
                                        """)
        self.mainHorizontalLayout.addWidget(self.rightWidget)

        self.mainHorizontalLayout.setStretch(0, 6)
        self.mainHorizontalLayout.setStretch(1, 2)
        
        self.btnHorizontalLayout = QtWidgets.QHBoxLayout()
        # self.btnHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btnHorizontalLayout.setSpacing(35)
        
        # * belong to left widget
        self.leftVerticalLayout.addLayout(self.btnHorizontalLayout)
        
        self.newChatBtn = QtWidgets.QPushButton(self.leftWidget)
        self.newChatBtn.setFixedHeight(30)
        self.newChatBtn.setStyleSheet("color: white; background-color: rgb(46, 139, 87); border-radius: 10px; font-weight: bold;")
        self.newChatBtn.setIcon(QIcon("./images/newChat.png"))
        
        self.btnHorizontalLayout.addWidget(self.newChatBtn)

        self.regenerateBtn = QtWidgets.QPushButton(self.leftWidget)
        self.regenerateBtn.setFixedHeight(30)
        self.regenerateBtn.setStyleSheet("color: white; background-color: rgb(65, 105, 225); border-radius: 10px; font-weight: bold;")
        self.regenerateBtn.setIcon(QIcon("./images/recycle.png"))
        
        self.btnHorizontalLayout.addWidget(self.regenerateBtn)

        self.stopOutputBtn = QtWidgets.QPushButton(self.leftWidget)
        self.stopOutputBtn.setFixedHeight(30)
        self.stopOutputBtn.setStyleSheet("color: white; background-color: rgb(220, 80, 100); border-radius: 10px; font-weight: bold;")
        self.stopOutputBtn.setIcon(QIcon("./images/stop.png"))
        # self.stopOutputBtn.hide()
        self.btnHorizontalLayout.addWidget(self.stopOutputBtn)

        self.lastChatBtn = QtWidgets.QPushButton(self.leftWidget)
        self.lastChatBtn.setFixedHeight(30)
        self.lastChatBtn.setStyleSheet("color: white; background-color: rgb(23, 180, 200); border-radius: 10px; font-weight: bold;")
        self.lastChatBtn.setIcon(QIcon("./images/upperArrow.png"))
        
        self.btnHorizontalLayout.addWidget(self.lastChatBtn)

        self.recycleTokensBtn = QtWidgets.QPushButton(self.leftWidget)
        self.recycleTokensBtn.setFixedHeight(30)
        self.recycleTokensBtn.setStyleSheet("color: white; background-color: rgb(123, 104, 238); border-radius: 10px; font-weight: bold;")
        self.recycleTokensBtn.setIcon(QIcon("./images/recycle1.png"))
        
        self.btnHorizontalLayout.addWidget(self.recycleTokensBtn)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "chatWidgetFrame"))
        self.sendBtn.setText(_translate("MainWindow", "Send"))
        self.newChatBtn.setText(_translate("MainWindow", "New chat"))
        self.regenerateBtn.setText(_translate("MainWindow", "Regenerate"))
        self.lastChatBtn.setText(_translate("MainWindow", "Last chat"))
        self.recycleTokensBtn.setText(_translate("MainWindow", "Recycle tokens"))
        self.stopOutputBtn.setText(_translate("MainWindow", "Stop output"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chatWidgetFrame = ChatWidgetFrame()
    chatWidgetFrame.show()
    sys.exit(app.exec())
