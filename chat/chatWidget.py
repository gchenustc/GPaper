from PySide6 import QtGui, QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QTextBrowser
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtCore import Qt
import sys
from chat.chatWidgetFrame import ChatWidgetFrame


class ChatWidget(ChatWidgetFrame):
    def __init__(self, parent=None):
        super(ChatWidget, self).__init__(parent)
        self.setupUi()
        # the number of bubbles
        self.sum = 0
        self.widgetlist = []  # 记录气泡
        self.text = ""                                              # 存储信息
        self.icon = QtGui.QPixmap(
            "images/pdf.png")                          # 头像
        # 设置聊天窗口样式 隐藏滚动条
        self.leftScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.leftScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 信号与槽
        self.sendBtn.clicked.connect(self.createBubble)  # 创建气泡
        self.sendBtn.clicked.connect(self.reviseBubbleLenth)  # 修改气泡长宽
        self.userInput.undoAvailable.connect(self.Event)  # 监听输入框状态
        scrollbar = self.leftScrollArea.verticalScrollBar()
        scrollbar.rangeChanged.connect(
            self.adjustScrollToMaxValue)  # 监听窗口滚动条范围

    # 回车绑定发送
    def Event(self):
        if not self.userInput.isEnabled():  # 这里通过文本框的是否可输入
            self.userInput.setEnabled(True)
            self.sendBtn.click()
            self.userInput.setFocus()

    # 创建气泡
    def createBubble(self):
        self.text = self.userInput.toPlainText()
        self.userInput.setPlainText("")
        self.sum += 1
        if self.sum % 2:   # 根据判断创建左右气泡
            # 调用new_widget.py中方法生成左气泡
            self.setChatReturn(
                self.icon, self.text, QtCore.Qt.LeftToRight)
            QApplication.processEvents()                                # 等待并处理主循环事件队列
        else:
            # 调用new_widget.py中方法生成右气泡
            self.setChatReturn(
                self.icon, self.text, QtCore.Qt.RightToLeft)
            QApplication.processEvents()                                # 等待并处理主循环事件队列

        # 你可以通过这个下面代码中的数组单独控制每一条气泡
        # self.widgetlist.append(self.widget)
        # print(self.widgetlist)
        # for i in range(self.sum):
        #     f=self.widgetlist[i].findChild(QTextBrowser)    #气泡内QTextBrowser对象
        #     print("第{0}条气泡".format(i),f.toPlainText())

    # 修改气泡长宽

    def reviseBubbleLenth(self):
        font = QFont()
        font.setPointSize(12)
        font.setFamily("微软雅黑")
        fm = QFontMetrics(font)
        textWidth = fm.boundingRect(self.text).width() + 83

        if self.sum != 0:
            if textWidth > 832:  # 宽度上限
                textWidth = int(
                    self.textBrowser.document().size().width())+83  # 固定宽度
            self.messageWidget.setMinimumSize(textWidth, int(
                self.textBrowser.document().size().height()) + 25)  # 规定气泡大小
            self.messageWidget.setMaximumSize(textWidth, int(
                self.textBrowser.document().size().height()) + 25)  # 规定气泡大小
            self.leftScrollArea.verticalScrollBar().setValue(10)

    # 窗口滚动到最底部
    def adjustScrollToMaxValue(self):
        scrollbar = self.leftScrollArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def setChatReturn(self, ico, text, dir):  # head portrait, text, direction

        if not text:
            return

        self.messageWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.messageWidget.setLayoutDirection(dir)
        self.messageWidget.setStyleSheet("""border: 0px;""")

        self.messageHorizontalLayout = QtWidgets.QHBoxLayout(
            self.messageWidget)

        self.headLabel = QtWidgets.QLabel(self.messageWidget)
        self.headLabel.setMaximumSize(QtCore.QSize(40, 40))
        self.headLabel.setText("")
        self.headLabel.setPixmap(ico)
        self.headLabel.setScaledContents(True)
        self.headLabel.setStyleSheet("""border:0px solid #34495e;""")

        self.messageHorizontalLayout.addWidget(self.headLabel)

        self.textBrowser = QtWidgets.QTextBrowser(self.messageWidget)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setStyleSheet("""
                                        padding:2px;
                                        background-color: rgba(71,121,214,40);
                                        border-radius: 10px;
                                        font: 12pt '微软雅黑';
                                       """)
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 0))

        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.messageHorizontalLayout.addWidget(self.textBrowser)
        self.outputVerticalLayout.addWidget(self.messageWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChatWidget()
    win.show()
    sys.exit(app.exec())
