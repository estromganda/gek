import sys

from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QTextEdit, QGroupBox, QVBoxLayout, QGridLayout, QRadioButton, \
    QHBoxLayout, QPushButton, QApplication

from functions import binaryToDecimal, binaryToHex, hexadecimalToDecimal, hexadecimalToBinary, resizeElement, \
    asciiToBinary, binaryToAscii


class ConverterWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # Widget member
        # Radio buttons for the choice of entry
        self.btnDecimal = QRadioButton(self.tr("Decimal"))
        self.btnBin = QRadioButton(self.tr("Binary"))
        self.btnHex, self.btnAuto = QRadioButton(self.tr("Hexadecimal")), QRadioButton(self.tr("Auto detect"))
        self.btnConvert = QPushButton(self.tr("Convert"))
        self.btnAuto.setChecked(True)

        # adding of radio button in a group box
        self.inputChooserWidget = QGroupBox()
        self.inputChooserWidget.setLayout(QHBoxLayout())
        self.inputChooserWidget.layout().addWidget(QLabel(self.tr("Input type: ")))
        self.inputChooserWidget.layout().addWidget(self.btnDecimal)
        self.inputChooserWidget.layout().addWidget(self.btnBin)
        self.inputChooserWidget.layout().addWidget(self.btnHex)
        self.inputChooserWidget.layout().addWidget(self.btnAuto)

        self.setWindowTitle(self.tr("Converter"))
        self.centralWidget = QWidget()
        label = QLabel("<div style='color: blue; font-size:50px; font-style:oblique'>" + "Converter" + "</div>")
        label.setAlignment(Qt.AlignCenter)
        self.decimalWidget, decimalContainer = ConverterWidget.createChild("Decimal value")
        self.binaryWidget, binaryContainer = ConverterWidget.createChild("Binary value")
        self.hexWidget, hexContainer = ConverterWidget.createChild("Hexadecimal value")
        self.asciiWidget, asciiContainer = ConverterWidget.createChild("Ascii value")

        layout = QGridLayout()

        # adding children's Widget in the layout
        layout.addWidget(label, 0, 0, 1, 2, Qt.AlignCenter)
        layout.addWidget(self.inputChooserWidget, 1, 0, 1, 2)
        layout.addWidget(decimalContainer, 2, 0, 1, 1)
        layout.addWidget(hexContainer, 2, 1, 1, 1)
        layout.addWidget(binaryContainer, 3, 0, 1, 1)
        layout.addWidget(asciiContainer, 3, 1, 1, 1)
        layout.addWidget(self.btnConvert, 4, 0, 1, 2, Qt.AlignCenter)
        self.centralWidget.setLayout(layout)
        self.setCentralWidget(self.centralWidget)

        # Connection
        # with radio Buttons
        self.btnConvert.clicked.connect(self.onConversion)
        self.btnBin.clicked.connect(self.onChooseInputType)
        self.btnDecimal.clicked.connect(self.onChooseInputType)
        self.btnHex.clicked.connect(self.onChooseInputType)
        self.btnAuto.clicked.connect(self.onChooseInputType)
        # with input's widget
        self.decimalWidget.installEventFilter(self)
        self.hexWidget.installEventFilter(self)
        self.binaryWidget.installEventFilter(self)
        self.asciiWidget.installEventFilter(self)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:

        if a1.type() == QEvent.KeyRelease and self.btnAuto.isChecked():
            if a0 == self.decimalWidget:
                self.onDecimalTextChanged()
                return True
            elif a0 == self.binaryWidget:
                self.onBinaryTextChanged()
                return True
            elif a0 == self.hexWidget:
                self.onHexadecimalTextChanged()
                return True
            elif a0 == self.asciiWidget:
                self.onAsciiTextChanged()
            else:
                pass
        return QMainWindow.eventFilter(self, a0, a1)

    def onDecimalTextChanged(self):
        decimalValue = self.decimalWidget.toPlainText().split(" ")
        if len(decimalValue) == 0:
            return
        for i in range(len(decimalValue)):
            if not decimalValue[i].isnumeric():
                return
        binaryValue = [bin(int(i))[2:] for i in decimalValue if i != " " and i != ""]
        hexValue = [hex(int(i))[2:] for i in decimalValue if i != " " and i != ""]
        binaryValue = resizeElement(binaryValue, 8)
        hexValue = resizeElement(hexValue, 2)

        self.binaryWidget.setText(" ".join(binaryValue))
        self.hexWidget.setText(" ".join(hexValue))
        self.asciiWidget.setText(binaryToAscii(" ".join(binaryValue)))

    def onBinaryTextChanged(self):
        binaryText = self.binaryWidget.toPlainText()
        if len(binaryText) == 0:
            return
        self.decimalWidget.setText(binaryToDecimal(binaryText))
        self.hexWidget.setText(binaryToHex(binaryText))
        self.asciiWidget.setText(binaryToAscii(binaryText))

    def onHexadecimalTextChanged(self):
        hexValue = self.hexWidget.toPlainText().split(" ")
        if len(hexValue) == 0:
            return
        binaryValue = [str(hexadecimalToBinary(it)) for it in hexValue if it != ""]
        binaryValue = resizeElement(binaryValue, 8)
        self.decimalWidget.setText(hexadecimalToDecimal(self.hexWidget.toPlainText()))
        self.binaryWidget.setText(" ".join(binaryValue))
        self.asciiWidget.setText(binaryToAscii(" ".join(binaryValue)))

    def onChooseInputType(self):
        self.decimalWidget.setReadOnly(not (self.btnDecimal.isChecked() or self.btnAuto.isChecked()))
        self.binaryWidget.setReadOnly(not (self.btnBin.isChecked() or self.btnAuto.isChecked()))
        self.hexWidget.setReadOnly(not (self.btnHex.isChecked() or self.btnAuto.isChecked()))

    def onAsciiTextChanged(self):
        self.binaryWidget.setPlainText(asciiToBinary(self.asciiWidget.toPlainText()))
        self.hexWidget.setText(binaryToHex(self.binaryWidget.toPlainText()))
        self.decimalWidget.setText(binaryToDecimal(self.binaryWidget.toPlainText()))

    def onConversion(self):
        if self.btnAuto.isChecked():
            return
        if self.btnDecimal.isChecked():
            self.onDecimalTextChanged()
        elif self.btnBin.isChecked():
            self.onBinaryTextChanged()
        elif self.btnHex.isChecked():
            self.onHexadecimalTextChanged()
        else:
            pass

    @staticmethod
    def createChild(txt: str):
        groupBox = QGroupBox(txt)
        content = QTextEdit()
        groupBox.setLayout(QVBoxLayout())
        groupBox.layout().addWidget(content)
        return content, groupBox


def main():
    app = QApplication(sys.argv)
    w = ConverterWidget()
    w.show()
    w.resize(780, 480)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
