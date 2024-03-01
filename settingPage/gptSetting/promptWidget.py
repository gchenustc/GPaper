from PySide6.QtCore import (QCoreApplication, QRect, Qt)
from PySide6.QtGui import (QFont, QPixmap, QStandardItemModel, QStandardItem)
from PySide6.QtWidgets import (QApplication, QMessageBox, QComboBox,
                               QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget)
from entity.promptModel import Prompt
from dao import promptDao


class PromptWidget(QWidget):
    def __init__(self):
        super().__init__()

        # check if prompt exists, if not, add default prompt
        if not promptDao.getAllPrompts():
            prompt = Prompt(name="default", text="", selected=1)
            if not promptDao.addPrompt(prompt):
                QMessageBox.critical(None, "Error", "Failed to add default prompt")

        self.setupUi()

        self.nameCbx.currentIndexChanged.connect(self.nameCbxIndexChanged)

        self.saveNewBtn.clicked.connect(self.saveNewBtnClicked)
        self.modifyBtn.clicked.connect(self.modityBtnClicked)
        self.deleteBtn.clicked.connect(self.deleteBtnCliced)

        self.initInput()
        
    def setupUi(self):
        font = QFont()
        font.setPointSize(20)

        self.createPixmap("images/qianwen.png", 100, 360)
        self.createPixmap("images/openai.png", 300, 550)

        self.verticalLayoutWidget = QWidget(self)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget.setGeometry(QRect(290, 150, 100, 140))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout_2")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # name label
        self.nameLabel = QLabel(self.verticalLayoutWidget)
        self.nameLabel.setObjectName(u"label")
        self.nameLabel.setFont(font)

        self.verticalLayout.addWidget(self.nameLabel)

        # text label
        self.textLabel = QLabel(self.verticalLayoutWidget)
        self.textLabel.setObjectName(u"textLabel")
        self.textLabel.setFont(font)

        self.verticalLayout.addWidget(self.textLabel)

        font = QFont()
        font.setPointSize(16)

        # input
        self.verticalLayoutWidget_2 = QWidget(self)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(400, 150, 541, 450))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSpacing(30)
        self.verticalLayout_2.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2.setContentsMargins(0, 20, 0, 20)

        # name combobox
        self.nameCbx = QComboBox(self.verticalLayoutWidget_2)
        self.nameCbx.setObjectName(u"comboBox")
        self.nameCbx.setEditable(True)
        self.nameCbx.setFixedHeight(40)
        self.nameCbx.setFont(font)

        self.verticalLayout_2.addWidget(self.nameCbx)

        # text input
        self.textInput = QTextEdit(self.verticalLayoutWidget_2)
        self.textInput.setObjectName(u"textEdit")
        self.textInput.setFont(font)

        self.verticalLayout_2.addWidget(self.textInput)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(400, 617, 541, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(120)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)

        self.saveNewBtn = self._extracted_from_setupUi_78(
            u"saveNewBtn",
            "color: white; background-color: rgb(46, 139, 87); border-radius: 5px; font-weight: bold;",
        )
        self.deleteBtn = self._extracted_from_setupUi_78(
            u"deleteBtn",
            "color: white; background-color: rgb(255, 100, 70); border-radius: 5px; font-weight: bold;",
        )
        self.modifyBtn = self._extracted_from_setupUi_78(
            u"modifyBtn",
            "color: white; background-color: rgb(65, 105, 225); border-radius: 5px; font-weight: bold;",
        )
        self.retranslateUi()

    def createPixmap(self, arg0, arg1, arg2):
        # image
        qianwenPixmap = QPixmap(arg0)
        qianwenScaledPixmap = qianwenPixmap.scaled(
            arg1, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        qianWenLabel = QLabel(self)
        qianWenLabel.setPixmap(qianwenScaledPixmap)
        qianWenLabel.setGeometry(arg2, 45, arg1, 100)

    # TODO Rename this here and in `setupUi`
    def _extracted_from_setupUi_78(self, arg0, arg1):
        # save new button
        result = QPushButton(self.horizontalLayoutWidget)
        result.setObjectName(arg0)
        result.setStyleSheet(arg1)
        result.setFixedHeight(35)

        self.horizontalLayout.addWidget(result)

        return result

    def retranslateUi(self):
        self.nameLabel.setText(
            QCoreApplication.translate("Form", u"name", None))
        self.textLabel.setText(
            QCoreApplication.translate("Form", u"text", None))
        self.saveNewBtn.setText(
            QCoreApplication.translate("Form", u"Save new", None))
        self.deleteBtn.setText(
            QCoreApplication.translate("Form", u"Delete", None))
        self.modifyBtn.setText(
            QCoreApplication.translate("Form", u"Modify", None))

    def freshInput(self) -> bool:
        
        currentIdx = self.nameCbx.currentIndex()
        if currentIdx == -1:
            return False
        
        # promptId = self.nameCbx.currentData(Qt.UserRole)
        promptId = promptDao.getPromptFromSelected(selected=1)[0].id
        
        prompt = promptDao.getPromptFromId(promptId)[0]
        self.textInput.setText(prompt.text)
        
        return True
        
    def initInput(self):
        self.nameCbx.currentIndexChanged.disconnect()

        self.nameCbxModel = QStandardItemModel()

        prompts = promptDao.getAllPrompts()[::-1]
        
        sprtedPrompts = []
        for prompt in prompts:
            if prompt.selected:
                sprtedPrompts.insert(0, prompt)
            else:
                sprtedPrompts.append(prompt)

        for prompt in sprtedPrompts:
            item = QStandardItem(prompt.name)
            item.setText(prompt.name)
            item.setData(prompt.id, role=Qt.UserRole)
            self.nameCbxModel.appendRow(item)

        self.nameCbx.setModel(self.nameCbxModel)

        self.freshInput()

        self.nameCbx.currentIndexChanged.connect(self.nameCbxIndexChanged)

    def nameCbxIndexChanged(self):
        self.nameCbx.currentIndexChanged.disconnect()
        
        currentPromptId = self.nameCbx.currentData(Qt.UserRole)
        
        allPrompts = promptDao.getAllPrompts()
        
        for prompt in allPrompts:
            prompt.selected = 1 if prompt.id == currentPromptId else 0
            if not promptDao.modifyPromptFromId(prompt):
                QMessageBox.critical(None, "Error", "Failed to modify the prompt (while change prompt selected status)")
                return
            
        self.freshInput()

        self.nameCbx.currentIndexChanged.connect(self.nameCbxIndexChanged)

    def saveNewBtnClicked(self):
        name = self.nameCbx.currentText().strip()
        text = self.textInput.toPlainText().strip()
        
        if not name.strip():
            QMessageBox.warning(None, "warning", "Name is null")
            return
        
        prompt = Prompt(name=name, text=text)
        if not promptDao.addPrompt(prompt):
            QMessageBox.critical(None, "Error", "Failed to add prompt")
            return
        QMessageBox.information(None, "Success", "Prompt added successfully")
        
        self.initInput()

    def modityBtnClicked(self):
        # certain if the name combobox existed
        if self.nameCbx.currentIndex() == -1:
            QMessageBox.warning(None, "warning", "No prompt existed, create a prompt first")
            return
        promptId = self.nameCbx.currentData(Qt.UserRole)
        prompt: Prompt = promptDao.getPromptFromId(promptId)[0]
        prompt.name = self.nameCbx.currentText().strip()
        prompt.text = self.textInput.toPlainText().strip()
        
        if not promptDao.modifyPromptFromId(prompt, True):
            QMessageBox.critical(None, "Error", "Failed to modify the prompt")
            return

        QMessageBox.information(None, "information", "Modify the prompt success")
        
        self.initInput()
    
    def deleteBtnCliced(self):
        if self.nameCbx.currentIndex() == -1:
            QMessageBox.warning(None, "warning", "No prompt existed, create a prompt first")
            return
        
        promptId = self.nameCbx.currentData(Qt.UserRole)
        if not promptDao.deletePromptFromId(promptId):
            QMessageBox.critical(None, "Error", "Failed to delete the prompt")
            return

        QMessageBox.information(None, "information", "Delete the prompt success")
        
        self.initInput()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    main = PromptWidget()
    main.show()

    sys.exit(app.exec())
