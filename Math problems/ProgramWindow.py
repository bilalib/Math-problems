from Problem import Problem
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import time


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        self.showMaximized()

    def initUi(self):
        self.setWindowTitle("Math Problem")
        self.setStyleSheet("QWidget {font: 20pt calibri}")
        problem = Problem()
        problem.pose()

        self.lbl_statement = QLabel(problem.statement)
        self.lbl_statement.setWordWrap(True)

        self.btn_submit = QPushButton("Check answer")   
        self.btn_submit.setMaximumSize(500, 100)
        self.btn_submit.clicked.connect(lambda: self.lbl_statement.setText(self.edit_input.text()))

        self.edit_input = QLineEdit()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_statement)
        self.layout.addWidget(self.btn_submit)

        # self.btn_submit.clicked.connect(problem.check(input))
        self.setLayout(self.layout)


def main(args):
    app = QApplication(args)
    app.setStyle("Fusion")
    window = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)