from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton,
    QGridLayout,
    QLabel,
    QTextEdit,
    QTabWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextOption
import sys

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setMinimumSize(1000,700)
        
        self.setWindowTitle("Angen")
        
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        
        tab = QTabWidget(self)
        
        ### Set up the chat tab ###
        # Labels
        chat_label = QLabel('Enter message:')
        history_label = QLabel('Chat History: ') 
        
        # Widgets
        self.line_edit = QTextEdit()
        self.line_edit.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.line_edit.setFixedHeight(50)
        self.chat_history = QListWidget()
        self.chat_history.setWordWrap(True)
        send_chat_button = QPushButton('Send', clicked=self.send_message)      
        chat_page = QWidget(tab)
        
        # Define Layout, add items to layout
        chat_page_layout = QGridLayout()
        chat_page.setLayout(chat_page_layout)
        
        # The scrolling on the chathistory is horrible.
        # ToDo: Look into better scrolling. Smoother?
        chat_page_layout.addWidget(history_label, 0, 0, 1, 2)
        chat_page_layout.addWidget(self.chat_history, 1, 0, 2, 2)
        chat_page_layout.addWidget(chat_label, 3, 0, 1, 2)
        chat_page_layout.addWidget(self.line_edit, 4, 0, 1, 2)
        chat_page_layout.addWidget(send_chat_button, 5, 0, 1, 2)
        
        ### Set up data tab ###
        data_page = QWidget(tab)
        data_page_layout = QGridLayout()
        data_page.setLayout(data_page_layout)
        
        ### Finalise tabs ###
        tab.addTab(chat_page, 'Chat')
        tab.addTab(data_page, 'Data Ingress')
        
        main_layout.addWidget(tab, 0, 0, 2, 1)
        
        self.show()
        
    def add_message(self, text, alight_right=False):
        """
        Handle adding the message to the chat list
        """
        # These custom widgets are pretty robust. I want to make this more like a texting UI, so...
        # ToDo: Texting-like interface, maybe chat bubbles?
        message_widget = QWidget()
        
        # I'll be real for now I dont get why I'm using this, I'll replace it or justify it alter
        layout = QHBoxLayout()
        
        label = QLabel(text)
        label.setWordWrap(True)
        
        label.setMaximumWidth(900)
        label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred) 
        
        
        label.adjustSize()
        
        # There is probably a dozen better ways to do this styling, but for now this works
        if alight_right:
            label.setStyleSheet(
            "background-color:rgb(162, 198, 255); border-radius: 5px; padding: 8px; font-size: 18px;"
        )
            layout.addStretch()
            layout.addWidget(label)
        else:
            label.setStyleSheet(
            "background-color:rgb(170, 255, 162); border-radius: 5px; padding: 8px; font-size: 18px;"
        )
            layout.addWidget(label)
            layout.addStretch()
            
        message_widget.setLayout(layout)
        
        message_item = QListWidgetItem(self.chat_history)
        message_item.setSizeHint(message_widget.sizeHint())
        self.chat_history.addItem(message_item)
        self.chat_history.setItemWidget(message_item, message_widget)
        
    def send_message(self):
        """
        Send the message to the LLM
        """
        # Placeholder for now so I can just tinker with stuff, will actually
        # send amessage in the future
        user_message = self.line_edit.toPlainText().strip()
        if user_message:
            self.add_message(user_message, alight_right=True)
            
            self.line_edit.clear()
            
            # Calling this here temporarily so I can BS a call-and-response.
            self.handle_model_response()
        
    def handle_model_response(self):
        """
        Pipe model response to front end.
        """
        self.add_message("Placeholder", alight_right=False)
        #model_response = self.line_edit.toPlainText().strip()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
        