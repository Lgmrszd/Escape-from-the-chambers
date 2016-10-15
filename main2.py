from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import engine

class MyQPushButton(QtWidgets.QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.setStyleSheet( "QPushButton { border-image: url(/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_unactive.png); \
        border-top: 3px transparent;\
        border-bottom: 3px transparent;\
        border-right: 10px transparent; \
        border-left: 10px transparent; }\
        QPushButton::hover { border-image: url(/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_active.png); }\
        QPushButton::pressed { border-image: url(/home/mikhail/PycharmProjects/Escape-from-the-chambers/sprites/button_pressed.png); }\
        ")
        self.setFixedSize(QtCore.QSize(150, 60))
    

class MyForm(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def clickFileBtn(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/')[0]

    def clickPlayBtn(self):
        print(self.fname)
        engine.run_level(self.fname)

    def initUI(self):
        self.playButton = MyQPushButton('Играть!')
        self.playButton.clicked.connect(self.clickPlayBtn)
        
        self.selectButton = MyQPushButton('Выбрать уровень')
        self.selectButton.clicked.connect(self.clickFileBtn)
        
        self.exitButton = MyQPushButton('Выйти')
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        self.mainVBox = QtWidgets.QVBoxLayout()
        self.mainVBox.addWidget(self.playButton)
        self.mainVBox.addWidget(self.selectButton)
        self.mainVBox.addWidget(self.exitButton)
        
        self.uiwidget = QtWidgets.QWidget()
        self.uiwidget.setLayout(self.mainVBox)

        self.setCentralWidget(self.uiwidget)
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

