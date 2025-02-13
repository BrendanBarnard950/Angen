from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
    QVBoxLayout,
)
import sys

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setWindowTitle("Angen")
        
        send_chat_button = QPushButton('Send', clicked=self.send_message)
        
        # Not 100% sure how this works yet, for now just following the docs
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(send_chat_button)
        
        self.show()
        
    def send_message(self):
        """
        Send the message to the LLM
        """
        # Placeholder for now so I can just tinker with stuff, will actually
        # send amessage in the future
        print('Message')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
        