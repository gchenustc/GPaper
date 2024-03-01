from PySide6.QtCore import (QCoreApplication, QRect, Qt)
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (QApplication, QStackedWidget,
                               QLabel, QLineEdit, QPushButton, QSplitter, QVBoxLayout, QWidget)
from settingPage.gptSetting.apiWidget import ApiWidget
from settingPage.gptSetting.promptWidget import PromptWidget
from PySide6 import QtGui


class CustomPushButton(QPushButton):
    """CustomPushButton - if the button is focused, a color label will be shown on the left of the button"""

    def focusInEvent(self, event: QtGui.QFocusEvent):
        rect = self.geometry()
        print(f"{rect},{self.parent()}")
        self.foucsLabel = QLabel(self.parent().parent())
        self.foucsLabel.setGeometry(rect.x()-20, rect.y(), 5, rect.height())
        self.foucsLabel.setStyleSheet("background-color: #ffa500;")  # orange
        self.foucsLabel.show()
        super().focusInEvent(event)  # 调用父类的实现以保持默认行为

    def focusOutEvent(self, event: QtGui.QFocusEvent):
        self.foucsLabel.hide()
        super().focusOutEvent(event)


buttonStyle = """
    QPushButton {
        color: #333; /* 黑色文本 */
        border-radius: 4px; /* 可选，添加圆角以增加扁平感 */
        padding: 5px; /* 内边距，增强内容区域的空间感 */
        font-family: "Arial", sans-serif; /* 使用无衬线字体 */
        font-size: 30px;
        outline: none; /* 移除焦点轮廓 */
    }
    QPushButton:hover {
        color: #007aff; /* 鼠标悬停时，字体颜色变为蓝色 */
    }

    QPushButton:pressed {
        color: #fff /* 鼠标悬停时，字体颜色变为白色 */
    }
        """


class GptSettingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUi()

        self.apiBtn.clicked.connect(self.apiBtnClicked)
        self.promptBtn.clicked.connect(self.promptBtnClicked)

        self.api = ApiWidget()
        self.prompt = PromptWidget()

        self.stack.addWidget(self.api)
        self.stack.addWidget(self.prompt)
        # self.stack.setCurrentIndex(0)

        self.stack.setCurrentWidget(self.api)

    def setupUi(self):
        
        self.resize(1000, 760)

        # the right stack widget
        self.stack = QStackedWidget(self)
        self.stack.setGeometry(QRect(0, 0, 1000, 760))

        # left layout
        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 231, 761))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(55, 0, 55, 0)

        self.verticalLayoutWidget.setStyleSheet("background-color: #87cefa;")

        # API button
        self.apiBtn = CustomPushButton(self.verticalLayoutWidget)
        self.apiBtn.setObjectName(u"apiBtn")
        self.apiBtn.setStyleSheet(buttonStyle)

        self.verticalLayout.addWidget(self.apiBtn)

        # Prompt button
        self.promptBtn = CustomPushButton(self.verticalLayoutWidget)
        self.promptBtn.setObjectName(u"PromptBtn")

        self.promptBtn.setStyleSheet(buttonStyle)


        self.verticalLayout.addWidget(self.promptBtn)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate(
            "Form", u"Gpt Setting", None))
        self.apiBtn.setText(QCoreApplication.translate("Form", u"API", None))
        self.promptBtn.setText(
            QCoreApplication.translate("Form", u"Prompt", None))

    def apiBtnClicked(self):
        self.stack.setCurrentWidget(self.api)

    def promptBtnClicked(self):
        self.stack.setCurrentWidget(self.prompt)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = GptSettingWidget()
    main.show()

    sys.exit(app.exec())
