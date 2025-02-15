# ToDo: Fix the clusterfuck mess of class vars vs local vars
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
    QAbstractItemView,
    QFileDialog,
    QComboBox,
    QMessageBox,
)
from PyQt6.QtGui import QTextOption
import sys
import os

from model.model_handler import ModelHandler
from context_engine.context_handler import ContextHandler

from docx import Document
import fitz

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        """
        We set up the entire UI here.
        ToDo: Split off different tabs into seperate files, just for readiblity if nothing else
        """
        super().__init__(*args, **kwargs)
        
        self.model_handler = ModelHandler()
        self.context_handler = None
        
        self.setMinimumSize(1000,1000)
        
        self.setWindowTitle("Angen")
        
        main_layout = QGridLayout()
        self.setLayout(main_layout)
        
        tab = QTabWidget(self)
        
        self.db_path = None
        self.context_file_path = None
        
        ### Set up the chat tab ###
        # Labels
        context_location_label = QLabel('Existing Context Location:')
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
        self.db_selection = QPushButton('Select Folder for database', clicked=self.db_context_folder_dialogue)

        send_chat_button = QPushButton('Send', clicked=self.send_message)      
        
        # Define Layout, add items to layout
        chat_page = QWidget(tab)
        chat_page_layout = QGridLayout()
        chat_page.setLayout(chat_page_layout)
        
        chat_page_layout.addWidget(context_location_label, 0, 0, 1, 1)
        chat_page_layout.addWidget(self.db_selection, 0, 1, 1, 1)
        chat_page_layout.addWidget(history_label, 1, 0, 1, 2)
        chat_page_layout.addWidget(self.chat_history, 2, 0, 4, 2)
        chat_page_layout.addWidget(chat_label, 6, 0, 1, 2)
        chat_page_layout.addWidget(self.line_edit, 7, 0, 1, 2)
        chat_page_layout.addWidget(send_chat_button, 8, 0, 1, 2)
        
        ### Set up data tab ###
        # Labels
        context_location_label = QLabel('Existing Context Location:')
        file_upload_label = QLabel('File to upload to context:')
        catagory_label = QLabel('Catagory for uploaded context')
        tags_label = QLabel('Tags (seperated with comma):')
        
        self.db_path_label = QLabel('')
        self.context_path_label = QLabel('')
        
        # Widgets
        self.db_selection = QPushButton('Select Folder', clicked=self.db_context_folder_dialogue)
        self.added_context_selection_data = QPushButton('Select File', clicked=self.user_context_file_dialogue)
        self.catagory_dropdown = QComboBox()
        self.catagory_dropdown.addItems(['Chapter', 'Magic System', 'Geopolitics', 'Characters'])
        self.tags_box = QTextEdit()
        self.tags_box.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.tags_box.setFixedHeight(50)
        
        submit_context_button = QPushButton('Submit Context', clicked=self.handle_context)
        
        # Define Layout and add items
        data_page = QWidget(tab)
        data_page_layout = QGridLayout()
        data_page.setLayout(data_page_layout)
        
        data_page_layout.addWidget(context_location_label, 0, 0, 1, 2)
        data_page_layout.addWidget(self.db_selection, 1, 0, 1, 2)
        data_page_layout.addWidget(self.db_path_label, 2, 0, 1, 2)
        
        data_page_layout.addWidget(file_upload_label, 3, 0, 1, 2)
        data_page_layout.addWidget(self.added_context_selection_data, 4, 0, 1, 2)
        data_page_layout.addWidget(self.context_path_label, 5, 0, 1, 2)
        
        data_page_layout.addWidget(catagory_label, 6, 0, 1, 2)
        data_page_layout.addWidget(self.catagory_dropdown, 7, 0, 1, 2)
        data_page_layout.addWidget(tags_label, 8, 0, 1, 2)
        data_page_layout.addWidget(self.tags_box, 9, 0, 1, 2)
        data_page_layout.addWidget(submit_context_button, 10, 0, 1, 2)
        
        
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
            
            processed_prompt = self.context_handler.process_prompt(user_message)
            
            model_response = self.model_handler.promptLLM(prompt=processed_prompt)

            self.handle_model_response(model_response)
        
    def handle_model_response(self, model_response):
        """
        Pipe model response to front end.
        Args:
            model_response (str): The response the model generated
        """
        self.add_message(model_response, align_right=False)
        
    def db_context_folder_dialogue(self):
        """
        Opens dialogue box to get location of the fodler for the ChromaDB database
        """
        self.db_path = QFileDialog.getExistingDirectory(self, "Select Folder:")
        self.db_path_label.setText(self.db_path)
        name = self.db_path.split('/')[-1].lower().replace(' ', '_')
        self.context_handler = ContextHandler(self.db_path, name)
        
    def user_context_file_dialogue(self):
        """
        Opens dialogue box to get user's context file they want to upload
        """
        self.context_file_path = QFileDialog.getOpenFileName(self, "Select File:")[0]
        self.context_path_label.setText(self.context_file_path)
        
    def handle_context(self):
        """
        Passes the given context to the Context Engine for processing
        """
        if self.db_path == None:
            QMessageBox.warning(self, "An error has occured", "Please pick a path for your context database")
        elif self.context_file_path == None:
            QMessageBox.warning(self, "An error has occured", "Please select a context file to upload")
        
        else:
            # Make sure we don't keep re-initialising things if we dont have too
            if self.context_handler == None:
                self.db_path = QFileDialog.getExistingDirectory(self, "Select Folder:")
                self.db_path_label.setText(self.db_path)
                name = self.db_path.split('/')[-1].lower().replace(' ', '_')
                self.context_handler = ContextHandler(self.db_path, name)
            
            context_info = self.decode_file()
            if context_info:     
                tags = self.tags_box.toPlainText()
                catagory = str(self.catagory_dropdown.currentText())
                self.context_handler.process_context(context_info, tags, catagory)
            
    def decode_file(self):
        """
        Decodes the file into string lists that we can pass into the context handle
        """
        file_extention = os.path.splitext(self.context_file_path)[1].lower()
        
        if file_extention in ['.md', '.txt']:
            with open(self.context_file_path, encoding='utf-8') as file:
                context_info = file.read()
        elif file_extention == '.docx':
            word_doc = Document(self.context_file_path)
            context_info = "\n".join([para.text for para in word_doc.paragraphs])
        elif file_extention == '.pdf':
            pdf_doc = fitz.open(self.context_file_path)
            context_info = "\n".join([page.get_text("text") for page in pdf_doc])
        else:
            QMessageBox.warning(self, "An error has occured", "You selected an invalid file type")
            return None
        
        return context_info
        
# ToDo: Maybe move the main excecution out of here.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
        