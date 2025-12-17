from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benkyosu")
        self.resize(400,300)


        self.label = QLabel("Song: None")
        self.label = QLabel("No folder selected")
        
        self.folder_button = QPushButton("Select osu! Folder")
        self.folder_button.clicked.connect(self.select_folder)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.on_play)
        
        

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.play_button)
        layout.addWidget(self.folder_button)
        self.setLayout(layout)

        self.selected_folder = None
        

    def on_play(self):
        #self.label.setText("Playing song...")
        print("Play")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select osu Songs Folder")
        if folder:
            self.selected_folder = folder
            self.label.setText(f"Selected folder:\n{folder}")
  

