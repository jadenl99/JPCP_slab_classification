import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 1")

class MainWindow2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window 2")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create instances of both windows
    window1 = MainWindow1()
    window2 = MainWindow2()

    # Show both windows
    window1.show()
    window2.show()

    sys.exit(app.exec_())