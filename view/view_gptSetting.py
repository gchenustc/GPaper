# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_gptSetting.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1001, 760)
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
        self.verticalLayoutWidget_2.setGeometry(QRect(390, 0, 131, 761))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.verticalLayoutWidget_3 = QWidget(Form)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(610, -1, 241, 761))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setSpacing(120)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.verticalLayout_3.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.verticalLayout_3.addWidget(self.lineEdit_3)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget_3)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout_3.addWidget(self.lineEdit)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"GPT SETTING", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"API", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Prompt", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"platform", None))
        self.label.setText(QCoreApplication.translate("Form", u"Keys", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"host", None))
    # retranslateUi

