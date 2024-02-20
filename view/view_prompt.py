# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_prompt.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1001, 762)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 231, 761))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(55, 0, 55, 0)
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        font = QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalLayoutWidget_2 = QWidget(Form)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(290, 70, 101, 111))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.verticalLayoutWidget_3 = QWidget(Form)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(400, 70, 541, 491))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSpacing(30)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 20, 0, 20)
        self.comboBox = QComboBox(self.verticalLayoutWidget_3)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_3.addWidget(self.comboBox)

        self.textEdit = QTextEdit(self.verticalLayoutWidget_3)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout_3.addWidget(self.textEdit)

        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(400, 609, 541, 61))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(80)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(30, 0, 30, 0)
        self.pushButton_5 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout.addWidget(self.pushButton_5)

        self.pushButton_4 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"GPT SETTING", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"API", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Prompt", None))
        self.label.setText(QCoreApplication.translate("Form", u"name", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"text", None))
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"save new", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"delete", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"modify", None))
    # retranslateUi

