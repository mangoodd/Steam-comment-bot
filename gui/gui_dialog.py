# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class UiDialog(object):

    def __init__(self, phrase):
        self.phrase = phrase

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 120)
        Dialog.setWindowIcon(QtGui.QIcon('../image/mstitel.jpg'))
        Dialog.setAcceptDrops(True)

        Dialog.setMouseTracking(False)
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        self.DialogLayout = QtWidgets.QVBoxLayout(Dialog)
        self.DialogLayout.setContentsMargins(10, 10, 10, 10)
        self.DialogLayout.setSpacing(8)
        self.DialogLayout.setObjectName("DialogLayout")

        self.YesOrNo = QtWidgets.QDialogButtonBox(Dialog)
        self.YesOrNo.setOrientation(QtCore.Qt.Horizontal)
        self.YesOrNo.setStandardButtons(QtWidgets.QDialogButtonBox.No | QtWidgets.QDialogButtonBox.Yes)
        self.YesOrNo.setObjectName("YesOrNo")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setText(self.phrase)
        self.DialogLayout.addWidget(self.label)
        self.DialogLayout.addWidget(self.YesOrNo)

        Dialog.setFixedSize(self.DialogLayout.sizeHint())

        self.retranslateUi(Dialog)
        self.YesOrNo.accepted.connect(Dialog.accept)  # type: ignore
        self.YesOrNo.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Внимание"))

    @staticmethod
    def initial():
        import sys

        app = QtWidgets.QApplication(sys.argv)
        Dialog = QtWidgets.QDialog()
        phrase = 'The selected page already has this comment.\nLeave one more?'
        ui = UiDialog(phrase)
        ui.setupUi(Dialog)
        Dialog.show()
        sys.exit(app.exec())


if __name__ == '__main__':
    UiDialog.initial()
