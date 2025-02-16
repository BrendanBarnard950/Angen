from PyQt6.QtWidgets import (
    QApplication, 
    QWidget,
    QLabel,
    QListWidgetItem,
    QHBoxLayout,
    QSizePolicy,
    QAbstractItemView,
    QFileDialog,
    QMessageBox,
    QMainWindow,
)

import sys
import os

from model.model_handler import ModelHandler
from context_engine.context_handler import ContextHandler
from UI.main_window_ui_design import Ui_MainWindow

from docx import Document
import fitz

class MainWindow(QWidget, Ui_MainWindow):
    # ============================================================================================================ #
    def __init__(self, *args, **kwargs):
        """
        We set up the entire UI here.
        """
        
        super().__init__(*args, **kwargs)
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        
        self.model_handler = ModelHandler()
        self.context_handler = None
        
        self.db_path = None
        self.context_file_path = None
        
        self.ui.catagory_dropdown.addItems(['Chapter', 'Magic System', 'Worldbuilding', 'Characters'])
        
        self.connectSignals()
        
        self.main_window.show()
        
    # ============================================================================================================ #
    def connectSignals(self):
        """
        This sucks royally. Need to manually connect all the slots and signals because for some
        reason I cant just give QT Designer a method name.
        """
        self.ui.send_chat_button.clicked.connect(self.sendMessage)
        self.ui.chat_tab_db_selection.clicked.connect(self.setupContextFolder)
        self.ui.data_tab_db_selection.clicked.connect(self.setupContextFolder)
        self.ui.added_context_selection_data.clicked.connect(self.contextUploadDialog)
        self.ui.submit_contex_button.clicked.connect(self.uploadContext)
        
    # ============================================================================================================ #    
    def addMessage(self, text, align_right=False):
        """
        Handle adding the message to the chat list
        """
        # These custom widgets are pretty robust.
        message_widget = QWidget()
        
        # I'll be real for now I dont get why I'm using this, I'll replace it or justify it later
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
            "background-color:rgb(162, 198, 255); border-radius: 5px; padding: 8px; font-size: 18px; color:rgb(0,0,0);"
        )
            layout.addStretch()
            layout.addWidget(label)
        else:
            label.setStyleSheet(
            "background-color:rgb(170, 255, 162); border-radius: 5px; padding: 8px; font-size: 18px; color:rgb(0,0,0);"
        )
            layout.addWidget(label)
            layout.addStretch()
            
        message_widget.setLayout(layout)
        
        #ToDo: I can't select text. Should probably find a way to fix that.
        message_item = QListWidgetItem(self.ui.chat_history)
        message_item.setSizeHint(message_widget.sizeHint())
        self.ui.chat_history.addItem(message_item)
        self.ui.chat_history.setItemWidget(message_item, message_widget)
        # Ensure we auto-scroll to the most recent message, cause manual scrolling is for dweebs.
        self.ui.chat_history.scrollToItem(message_item, hint=QAbstractItemView.ScrollHint.EnsureVisible)
    
    # ============================================================================================================ #    
    def sendMessage(self):
        """
        Send the message to the LLM
        """
        user_message = self.ui.chat_box.toPlainText().strip()
        if user_message:
            self.addMessage(user_message, align_right=True)
            
            self.ui.chat_box.clear()
            
            processed_prompt = self.context_handler.process_prompt(user_message)
            
            model_response = self.model_handler.promptLLM(prompt=processed_prompt)

            self.handleModelResponse(model_response)
    
    # ============================================================================================================ #    
    def handleModelResponse(self, model_response):
        """
        Pipe model response to front end.
        I know this only does one thing, but I'm keeping it seperate in case I ever need to do other post-processing
        on the resonse before it gets added to the chat log
        Args:
            model_response (str): The response the model generated
        """
        self.addMessage(model_response, align_right=False)
    
    # ============================================================================================================ #    
    def setupContextFolder(self):
        """
        Opens dialogue box to get location of the folder for the ChromaDB database
        """
        self.db_path = QFileDialog.getExistingDirectory(self, "Select Folder:")
        self.ui.context_path_label.setText(self.db_path)
        name = self.db_path.split('/')[-1].lower().replace(' ', '_')
        self.context_handler = ContextHandler(self.db_path, name)
    
    # ============================================================================================================ #    
    def contextUploadDialog(self):
        """
        Opens dialogue box to get user's context file they want to upload
        """
        self.context_file_path = QFileDialog.getOpenFileName(self, "Select File:")[0]
        self.ui.db_path_label.setText(self.context_file_path)
    
    # ============================================================================================================ #    
    def uploadContext(self):
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
            
            context_info = self.decodeContextFile()
            if context_info:     
                tags = self.ui.tags_box.text()
                catagory = str(self.ui.catagory_dropdown.currentText())
                self.context_handler.process_context(context_info, tags, catagory)
                
                self.ui.db_path_label.setText("")
                self.context_file_path = ""
                self.ui.tags_box.setText("")
            
    # ToDo: Fix file decoding, and add type hinting to file selection box
    # ============================================================================================================ #
    def decodeContextFile(self):
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
# ============================================================================================================ #
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 
    window = MainWindow()
    sys.exit(app.exec())
        