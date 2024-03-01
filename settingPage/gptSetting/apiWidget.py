from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (
    QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QMessageBox)
from dao import apiDao, modelDao
from entity.apiModel import Api
from entity.modelModel import Model

GPT_MODEL = {
    "openAi": [
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-3.5-turbo-16k",
        "gpt-4-1106-preview",
        "gpt-4"
    ],
    "qianWen": [
        "qwen-turbo",
        "qwen-plus",
        "qwen-max",
        "qwen-max-1201",
        "qwen-max-longcontext"
    ]
}


class ApiWidget(QWidget):
    def __init__(self):
        super().__init__()

        # check if api exists, if not, add default api
        if not apiDao.getAllApis():
            # init api table
            api1 = Api(platform=list(GPT_MODEL.keys())[0], selected=0)
            api2 = Api(platform=list(GPT_MODEL.keys())[1], selected=1)
            apiDao.addApi(api1)
            apiDao.addApi(api2)

            # init model table
            for model in list(GPT_MODEL.values())[0]:
                if model == "gpt-3.5-turbo-1106":
                    model = Model(name=model, apiId=1, selected=1)
                else:
                    model = Model(name=model, apiId=1, selected=0)
                modelDao.addModel(model, True)

            for model in list(GPT_MODEL.values())[1]:
                if model == "qwen-max-longcontext":
                    model = Model(name=model, apiId=2, selected=1)
                else:
                    model = Model(name=model, apiId=2, selected=0)
                modelDao.addModel(model, True)

        self.setupUi()

        self.confirmBtn.clicked.connect(self.confirmBtnClicked)

        self.platformCbx.currentIndexChanged.connect(
            self.platformCbxIndexChanged)

        self.initInput()

    def setupUi(self):

        font = QFont()
        font.setPointSize(20)

        # image
        qianwenPixmap = QPixmap("images/qianwen.png")
        qianwenScaledPixmap = qianwenPixmap.scaled(
            100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        qianWenLabel = QLabel(self)
        qianWenLabel.setPixmap(qianwenScaledPixmap)
        qianWenLabel.setGeometry(360, 45, 100, 100)

        openaiPixmap = QPixmap("images/openai.png")
        openaiScalePixmap = openaiPixmap.scaled(
            300, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        openaiLabel = QLabel(self)
        openaiLabel.setPixmap(openaiScalePixmap)
        openaiLabel.setGeometry(550, 45, 300, 100)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(340, 165, 131, 430))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.platformLabel = self.createQLabel(u"platformLabel", font)
        self.keyLabel = self.createQLabel(u"keyLabel", font)
        self.hostLabel = self.createQLabel(u"hostLabel", font)

        font = QFont()
        font.setPointSize(16)

        # right input
        self.verticalLayoutWidget_edit = QWidget(self)
        self.verticalLayoutWidget_edit.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_edit.setGeometry(QRect(520, 200, 370, 360))
        self.verticalLayout_edit = QVBoxLayout(self.verticalLayoutWidget_edit)
        self.verticalLayout_edit.setSpacing(90)
        self.verticalLayout_edit.setObjectName(u"verticalLayout_edit")
        self.verticalLayout_edit.setContentsMargins(0, 0, 0, 0)

        # platform input
        self.platformCbx = QComboBox(self.verticalLayoutWidget_edit)
        self.platformCbx.setObjectName(u"platFormInput")
        self.platformCbx.setFont(font)
        self.platformCbx.setFixedHeight(40)

        self.verticalLayout_edit.addWidget(self.platformCbx)

        # key input
        self.keyInput = QLineEdit(self.verticalLayoutWidget_edit)
        self.keyInput.setObjectName(u"keyInput")
        self.keyInput.setFont(font)
        self.keyInput.setFixedHeight(40)

        self.verticalLayout_edit.addWidget(self.keyInput)

        # host input
        self.hostInput = QLineEdit(self.verticalLayoutWidget_edit)
        self.hostInput.setObjectName(u"hostInput")
        self.hostInput.setFont(font)
        self.hostInput.setFixedHeight(40)

        self.verticalLayout_edit.addWidget(self.hostInput)

        self.confirmBtn = QPushButton(self)
        self.confirmBtn.setObjectName(u"searchBtn")
        self.confirmBtn.setGeometry(QRect(813, 630, 80, 28))
        self.confirmBtn.setStyleSheet(
            "color: white; background-color: rgb(65, 105, 225); border-radius: 5px; font-weight: bold;")
        self.confirmBtn.setFixedHeight(35)

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def createQLabel(self, objectName, font):
        # platform label
        result = QLabel(self.verticalLayoutWidget)
        result.setObjectName(objectName)
        result.setFont(font)

        self.verticalLayout.addWidget(result)

        return result

    def retranslateUi(self):
        self.platformLabel.setText(
            QCoreApplication.translate("Form", u"platform", None))
        self.keyLabel.setText(QCoreApplication.translate("Form", u"Key", None))
        self.hostLabel.setText(
            QCoreApplication.translate("Form", u"host", None))
        self.confirmBtn.setText(
            QCoreApplication.translate("Form", u"Confirm", None))

    def freshInput(self) -> bool:
        api = apiDao.getApifromSelected(selected=1)[0]
        self.keyInput.setText(api.key)
        self.hostInput.setText(api.host)

    def initInput(self):
        apis = apiDao.getAllApis()

        sortedApis = []

        for api in apis:
            if api.selected:
                sortedApis.insert(0, api)
            else:
                sortedApis.append(api)

        # init platformCbx
        for api in sortedApis:
            self.platformCbx.addItem(api.platform)

        # init key and host input
        self.freshInput()

    def platformCbxIndexChanged(self):
        self.platformCbx.currentIndexChanged.disconnect()

        platform = self.platformCbx.currentText().strip()

        # change selected status
        apis = apiDao.getAllApis()

        for api in apis:

            api.selected = 1 if api.platform == platform else 0

            if not apiDao.modifyApiFromId(api):
                QMessageBox.critical(
                    None, "Error", "Failed to modify api (while change api selected status))")

        # fresh input
        self.freshInput()

        self.platformCbx.currentIndexChanged.connect(
            self.platformCbxIndexChanged)

    def confirmBtnClicked(self):

        api = apiDao.getApifromSelected(selected=1)[0]

        key = self.keyInput.text().strip()
        host = self.hostInput.text().strip()

        api.key = key
        api.host = host

        if not apiDao.modifyApiFromId(api):
            QMessageBox.critical(None, "Error", "Failed to modify api")
        QMessageBox.information(None, "Success", "Modify api successfully")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = ApiWidget()
    main.show()

    sys.exit(app.exec())
