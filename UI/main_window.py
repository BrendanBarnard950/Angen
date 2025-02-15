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
    QAbstractItemView
)
from PyQt6.QtGui import QTextOption
import sys

from model.model_handler import ModelHandler

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.model_handler = ModelHandler()
        
        self.setMinimumSize(1000,1000)
        
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
        # Smooth scrolling, lets go! As usual, modern problems require 2011 Stackoverflow solutions
        self.chat_history.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.chat_history.verticalScrollBar().setSingleStep(20)
        self.chat_history.setWordWrap(True)

        send_chat_button = QPushButton('Send', clicked=self.send_message)      
        chat_page = QWidget(tab)
        
        # Define Layout, add items to layout
        chat_page_layout = QGridLayout()
        chat_page.setLayout(chat_page_layout)
        
        chat_page_layout.addWidget(history_label, 0, 0, 1, 2)
        chat_page_layout.addWidget(self.chat_history, 1, 0, 4, 2)
        chat_page_layout.addWidget(chat_label, 5, 0, 1, 2)
        chat_page_layout.addWidget(self.line_edit, 6, 0, 1, 2)
        chat_page_layout.addWidget(send_chat_button, 7, 0, 1, 2)
        
        ### Set up data tab ###
        data_page = QWidget(tab)
        data_page_layout = QGridLayout()
        data_page.setLayout(data_page_layout)
        
        ### Finalise tabs ###
        tab.addTab(chat_page, 'Chat')
        tab.addTab(data_page, 'Data Ingress')
        
        main_layout.addWidget(tab, 0, 0, 2, 1)
        
        self.show()
        
    def add_message(self, text, align_right=False):
        """
        Handle adding the message to the chat list
        """
        # These custom widgets are pretty robust.
        message_widget = QWidget()
        
        # I'll be real for now I dont get why I'm using this, I'll replace it or justify it alter
        # ToDo: Research layouts more in-depth
        layout = QHBoxLayout()

        label = QLabel(text)
        label.setWordWrap(True)
        
        label.setMaximumWidth(800)
        label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred) 
        
        # Doing this makes the text-bubble widget re-size to fit the label instead of stretching
        # to the max width
        label.adjustSize()
        
        # There is probably a dozen better ways to do this styling, but for now this works
        if align_right:
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
        
        #ToDo: I can't select text. Should probably find a way to fix that.
        message_item = QListWidgetItem(self.chat_history)
        message_item.setSizeHint(message_widget.sizeHint())
        self.chat_history.addItem(message_item)
        self.chat_history.setItemWidget(message_item, message_widget)
        # Ensure we auto-scroll to the most recent message, cause manual scrolling is for dweebs.
        self.chat_history.scrollToItem(message_item, hint=QAbstractItemView.ScrollHint.EnsureVisible)
        
    def send_message(self):
        """
        Send the message to the LLM
        """
        user_message = self.line_edit.toPlainText().strip()
        if user_message:
            self.add_message(user_message, align_right=True)
            
            self.line_edit.clear()
            
            model_response = self.model_handler.promptLLM(prompt=user_message)

            self.handle_model_response(model_response)
        
    def handle_model_response(self, model_response):
        """
        Pipe model response to front end.
        Args:
            model_response (str): The response the model generated
        """
        self.add_message(model_response, align_right=False)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
        