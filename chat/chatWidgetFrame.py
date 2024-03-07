from PySide6 import QtCore, QtWidgets
from chat.widgetRewite import MyPlainTextEdit, SlideCheckBox
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import QSize, QRect, Qt


RIGHT_CBX_STYLE = """
                                QComboBox {
                                    background-color: #eeeeee; /* 灰色背景 */
                                    border: 1px solid #ccc; /* 边框为浅灰色，宽度为1px */
                                    border-radius: 3px; /* 边框圆角为3px */
                                    padding: 5px 10px; /* 内边距，使内容与边框之间有一定的间距 */
                                    min-width: 80px; /* 最小宽度，可根据实际需求调整 */
                                    max-width: 130px;
                                    font-size: 14px; /* 字体大小 */
                                }
                                
                                QComboBox::drop-down {
                                    subcontrol-origin: padding;
                                    subcontrol-position: top right;
                                    width: 20px; /* 下拉按钮宽度 */
                                    border-left: 1px solid #ccc; /* 分割线，使得下拉按钮与输入框区分开 */
                                    border-top-right-radius: 3px; /* 保持圆角一致性 */
                                    border-bottom-right-radius: 3px;
                                }

                                QComboBox::down-arrow {
                                    image: url('images/down_arrow.png'); /* 使用自定义下拉箭头图标替换默认样式 */
                                    width: 12px;
                                    height: 12px;
                                }
                                
                                QComboBox::item {
                                    color: black; /* 下拉列表项的文字颜色 */
                                    padding: 5px 20px;
                                }
                                
                                QComboBox::item:selected {
                                    background-color: #f0f0f0; /* 选中状态的背景色 */
                                }
                            """


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
                            newChatBtn
                            regenerateBtn
                            stopOutputBtn
                            lastChatBtn
                            recycleTokensBtn
                    2. rightWidget
                        rightfuncWidget (rightfuncVerticalLayout)
                            platformHorizontalLayout
                                platformLabel
                                platformCbx
                            modelHorizontalLayout
                                modelLabel
                                modelCbx
                            memoryHorizontalLayout
                                memoryLabel
                                memoryInput
                            assiciateDbHorizontalLayout
                                assiciateDbLabel
                                assiciateDbCheckBox
                            separator

        """

        # TODO
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
        self.sendBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 10px; font-weight: bold;")
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
        self.newChatBtn.setStyleSheet(
            "color: white; background-color: rgb(46, 139, 87); border-radius: 10px; font-weight: bold;")
        self.newChatBtn.setIcon(QIcon("./images/newChat.png"))

        self.btnHorizontalLayout.addWidget(self.newChatBtn)

        self.regenerateBtn = QtWidgets.QPushButton(self.leftWidget)
        self.regenerateBtn.setFixedHeight(30)
        self.regenerateBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 10px; font-weight: bold;")
        self.regenerateBtn.setIcon(QIcon("./images/recycle.png"))

        self.btnHorizontalLayout.addWidget(self.regenerateBtn)

        self.stopOutputBtn = QtWidgets.QPushButton(self.leftWidget)
        self.stopOutputBtn.setFixedHeight(30)
        self.stopOutputBtn.setStyleSheet(
            "color: white; background-color: rgb(220, 80, 100); border-radius: 10px; font-weight: bold;")
        self.stopOutputBtn.setIcon(QIcon("./images/stop.png"))
        # self.stopOutputBtn.hide()
        self.btnHorizontalLayout.addWidget(self.stopOutputBtn)

        self.lastChatBtn = QtWidgets.QPushButton(self.leftWidget)
        self.lastChatBtn.setFixedHeight(30)
        self.lastChatBtn.setStyleSheet(
            "color: white; background-color: rgb(23, 180, 200); border-radius: 10px; font-weight: bold;")
        self.lastChatBtn.setIcon(QIcon("./images/upperArrow.png"))

        self.btnHorizontalLayout.addWidget(self.lastChatBtn)

        self.recycleTokensBtn = QtWidgets.QPushButton(self.leftWidget)
        self.recycleTokensBtn.setFixedHeight(30)
        self.recycleTokensBtn.setStyleSheet(
            "color: white; background-color: rgb(123, 104, 238); border-radius: 10px; font-weight: bold;")
        self.recycleTokensBtn.setIcon(QIcon("./images/recycle1.png"))

        self.btnHorizontalLayout.addWidget(self.recycleTokensBtn)

        # ! TODO right widget function
        self.rightfuncWidget = QtWidgets.QWidget(self.rightWidget)
        self.rightfuncWidget.setFixedHeight(280)

        self.rightfuncVerticalLayout = QtWidgets.QVBoxLayout(
            self.rightfuncWidget)
        self.rightfuncVerticalLayout.setSpacing(15)

        # platform
        self.platformHorizontalLayout = QtWidgets.QHBoxLayout()
        self.platformHorizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.platformHorizontalLayout.setSpacing(15)

        self.rightfuncVerticalLayout.addLayout(self.platformHorizontalLayout)

        self.platformLabel = QtWidgets.QLabel(self.rightfuncWidget)
        self.platformLabel.setFont(QFont("", 12, QFont.Bold))
        self.platformHorizontalLayout.addWidget(self.platformLabel)

        self.platformCbx = QtWidgets.QComboBox(self.rightfuncWidget)

        self.platformCbx.setStyleSheet(RIGHT_CBX_STYLE)

        self.platformHorizontalLayout.addWidget(self.platformCbx)

        # model
        self.modelHorizontalLayout = QtWidgets.QHBoxLayout()
        self.modelHorizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.modelHorizontalLayout.setSpacing(15)

        self.rightfuncVerticalLayout.addLayout(self.modelHorizontalLayout)

        self.modelLabel = QtWidgets.QLabel(self.rightfuncWidget)
        self.modelLabel.setFont(QFont("", 12, QFont.Bold))
        self.modelHorizontalLayout.addWidget(self.modelLabel)

        self.modelCbx = QtWidgets.QComboBox(self.rightfuncWidget)

        self.modelCbx.setStyleSheet(RIGHT_CBX_STYLE)

        self.modelHorizontalLayout.addWidget(self.modelCbx)

        # memory items
        self.memoryHorizontalLayout = QtWidgets.QHBoxLayout()
        self.memoryHorizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.memoryHorizontalLayout.setSpacing(15)
        self.rightfuncVerticalLayout.addLayout(self.memoryHorizontalLayout)

        self.memoryLabel = QtWidgets.QLabel(self.rightfuncWidget)
        self.memoryLabel.setFont(QFont("", 12, QFont.Bold))
        self.memoryHorizontalLayout.addWidget(self.memoryLabel)

        self.memoryInput = QtWidgets.QLineEdit(self.rightfuncWidget)
        self.memoryInput.setAlignment(Qt.AlignCenter) 
        self.memoryInput.setFixedWidth(80)
        self.memoryHorizontalLayout.addWidget(self.memoryInput)

        self.memoryInput.setStyleSheet("""
            QLineEdit {
                background-color: #eeeeee; /* 设置背景颜色为白色 */
                border: 1px solid #ccc; /* 边框为浅灰色，宽度为1px */
                border-radius: 2px; /* 边框圆角较小，显得更为扁平 */
                padding: 4px; /* 内边距使得输入区域与边框有一定的间距 */
                font-size: 14px; /* 字体大小 */
                color: #333; /* 文字颜色 */
            }

            QLineEdit:hover {
                border-color: #999; /* 鼠标悬停时边框变为浅灰色 */
            }

            QLineEdit:focus {
                border-color: #007aff; /* 获取焦点时边框变为蓝色，显示交互状态 */
                outline: none; /* 去除默认的轮廓线 */
            }
        """)

        # associate database checkbox
        self.assiciateDbHorizontalLayout = QtWidgets.QHBoxLayout()
        self.assiciateDbHorizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.assiciateDbHorizontalLayout.setSpacing(15)

        self.rightfuncVerticalLayout.addLayout(
            self.assiciateDbHorizontalLayout)

        self.assiciateDbLabel = QtWidgets.QLabel(self.rightfuncWidget)
        self.assiciateDbLabel.setFont(QFont("", 12, QFont.Bold))
        self.assiciateDbHorizontalLayout.addWidget(self.assiciateDbLabel)

        self.assiciateDbHorizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.assiciateDbHorizontalLayout_1.setContentsMargins(90, 5, 5, 5)
        self.assiciateDbHorizontalLayout_1.setSpacing(15)

        self.rightfuncVerticalLayout.addLayout(
            self.assiciateDbHorizontalLayout_1)

        self.assiciateDbCheckBox = SlideCheckBox(self.rightfuncWidget)
        self.assiciateDbCheckBox.setFont(QFont("", 12, QFont.Bold))
        self.assiciateDbCheckBox.setIconSize(QSize(55, 55))
        self.assiciateDbHorizontalLayout_1.addWidget(self.assiciateDbCheckBox)

        self.separator = QtWidgets.QFrame(self.rightfuncWidget)
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)  # 设置形状为水平线
        self.separator.setFrameShadow(
            QtWidgets.QFrame.Sunken)  # 设置阴影效果，使其看起来像一个分隔符
        self.separator.setStyleSheet("QFrame { background-color: black; }")

        self.rightfuncVerticalLayout.addWidget(self.separator)

        # history
        self.histWidget = QtWidgets.QWidget(self.rightWidget)
        self.histWidget.setGeometry(QRect(5, 275, 235, 490))
        # self.histWidget.setStyleSheet("""
        #                     background-color: rgb(220, 220, 220);
        #                     border-radius:10px;
        #                     border:3px solid #34495e;
        #                 """)
        self.histVerticalLayout = QtWidgets.QVBoxLayout(self.histWidget)
        self.histVerticalLayout.setSpacing(20)
        
        self.histLabel = QtWidgets.QLabel("History Chats: ", self.histWidget)
        self.histLabel.setFont(QFont("黑体", 14, QFont.Bold))
        self.histVerticalLayout.addWidget(self.histLabel)

        self.histContentWidget = QtWidgets.QWidget(self.histWidget)
        self.histContentVerticalLayout = QtWidgets.QVBoxLayout(self.histContentWidget)
        self.histContentVerticalLayout.setSpacing(20)

        self.histScrollArea = QtWidgets.QScrollArea(self.histWidget)
        self.histScrollArea.setStyleSheet("""
                                            border:initial;
                                            border: 0px solid;
                                        """)
        self.histScrollArea.setWidgetResizable(True)
        self.histScrollArea.setWidget(self.histContentWidget)
        
        self.histVerticalLayout.addWidget(self.histScrollArea)

        # TODO demo
        from chat.widgetRewite import MyLabel
        for _ in range(200):
            label = MyLabel("history item",
                            self.histContentWidget)
            label.setFixedWidth(180)
            label.setWordWrap(True)
            self.histContentVerticalLayout.addWidget(label)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "chatWidgetFrame"))
        self.sendBtn.setText(_translate("MainWindow", "Send"))
        self.newChatBtn.setText(_translate("MainWindow", "New chat"))
        self.regenerateBtn.setText(_translate("MainWindow", "Regenerate"))
        self.lastChatBtn.setText(_translate("MainWindow", "Last chat"))
        self.recycleTokensBtn.setText(
            _translate("MainWindow", "Recycle tokens"))
        self.stopOutputBtn.setText(_translate("MainWindow", "Stop output"))
        self.platformLabel.setText(_translate("MainWindow", "Platform:"))
        self.modelLabel.setText(_translate("MainWindow", "Model:"))
        self.memoryLabel.setText(_translate("MainWindow", "Memory items: "))
        self.assiciateDbLabel.setText(_translate(
            "MainWindow", "Accociate database: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chatWidgetFrame = ChatWidgetFrame()
    chatWidgetFrame.show()
    sys.exit(app.exec())
