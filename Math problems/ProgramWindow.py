from Problem import Problem
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()
        self.showMaximized()


    def initUi(self):
        self.problem = Problem()
        self.hard_mode = False

        self.setWindowTitle("Math Problem")
        self.setStyleSheet("QWidget {font: 20pt calibri}")
        self.layout = QVBoxLayout()


        # Submission form:
        self.layout_submission = QHBoxLayout()

        self.lbl_input_info = QLabel("Answer:")
        self.layout_submission.addWidget(self.lbl_input_info)

        self.edit_input = QLineEdit()
        self.layout_submission.addWidget(self.edit_input)

        self.btn_submit = QPushButton("Check answer")   
        self.btn_submit.setMaximumSize(500, 100)
        print(self.edit_input.text())
        self.btn_submit.clicked.connect(lambda: self.check(self.edit_input.text()))
        self.layout_submission.addWidget(self.btn_submit)
        
        self.layout.addLayout(self.layout_submission)
        

        # Problem statement label
        self.lbl_statement = QLabel(self.problem.statement)
        self.layout.addWidget(self.lbl_statement)
        
        
        # Stretch moves rest to bottom of page
        self.layout.addStretch()

        # Switch mode
        self.btn_mode = QPushButton("Activate hard mode")

        # Messages label
        self.lbl_message = QLabel()
        self.layout.addWidget(self.lbl_message)

        self.setLayout(self.layout)

    def check(self, input):
        self.lbl_message.clear()
        self.edit_input.clear()
        self.problem.check(input)
        if self.problem.result == "ValueError":
            self.lbl_message.setText("Error: Bad input.")
        if self.problem.result == "correct":
            self.lbl_message.setText("Correct! Moving to next question.")
            self.problem = Problem()
            self.lbl_statement.setText(self.problem.statement)
        if self.problem.result == "incorrect":
            if self.problem.attempt == 2:
                self.problem.pose()
                self.lbl_statement.setText(self.problem.statement)
                self.lbl_message.setText("Incorrect. All attempts used. Numbers changed.")
            else:
                self.lbl_message.setText("Incorrect. Attempt " + 
                                         str(self.problem.attempt + 1) + 
                                         "/3. Previous answers: " + 
                                         ", ".join(self.problem.previous_answers))


def main(args):
    app = QApplication(args)
    app.setStyle("Fusion")
    window = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv)