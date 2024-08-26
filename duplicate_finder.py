import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QListWidget, QLabel, QProgressBar, QMessageBox, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PIL import Image
import imagehash

class DuplicateFinder(QThread):
    progress_update = pyqtSignal(int)
    finished = pyqtSignal(dict)

    def __init__(self, directory):
        super().__init__()
        self.directory = directory

    def run(self):
        image_hashes = {}
        image_files = [f for f in os.listdir(self.directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        total_files = len(image_files)

        for i, filename in enumerate(image_files):
            file_path = os.path.join(self.directory, filename)
            with Image.open(file_path) as img:
                hash = str(imagehash.average_hash(img))
                if hash in image_hashes:
                    image_hashes[hash].append(file_path)
                else:
                    image_hashes[hash] = [file_path]
            self.progress_update.emit(int((i + 1) / total_files * 100))

        duplicates = {k: v for k, v in image_hashes.items() if len(v) > 1}
        self.finished.emit(duplicates)

class DuplicateFinderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.duplicates = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("No directory selected")
        dir_layout.addWidget(self.dir_label)
        self.select_dir_btn = QPushButton("Select Directory")
        self.select_dir_btn.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.select_dir_btn)
        layout.addLayout(dir_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Start button
        self.start_btn = QPushButton("Start Duplicate Search")
        self.start_btn.clicked.connect(self.start_duplicate_search)
        layout.addWidget(self.start_btn)

        # Results list
        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.show_duplicate_images)
        layout.addWidget(self.results_list)

        # Image preview and delete button layout
        preview_layout = QHBoxLayout()
        
        # Image preview
        self.image_preview = QLabel()
        self.image_preview.setAlignment(Qt.AlignCenter)
        preview_layout.addWidget(self.image_preview)

        # Delete button
        self.delete_btn = QPushButton("Delete Selected Image")
        self.delete_btn.clicked.connect(self.delete_selected_image)
        self.delete_btn.setEnabled(False)
        preview_layout.addWidget(self.delete_btn)

        layout.addLayout(preview_layout)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            self.dir_label.setText(dir_path)

    def start_duplicate_search(self):
        directory = self.dir_label.text()
        if directory == "No directory selected":
            QMessageBox.warning(self, "Error", "Please select a directory first.")
            return

        self.progress_bar.setValue(0)
        self.results_list.clear()
        self.image_preview.clear()
        self.delete_btn.setEnabled(False)

        self.duplicate_finder = DuplicateFinder(directory)
        self.duplicate_finder.progress_update.connect(self.update_progress)
        self.duplicate_finder.finished.connect(self.show_results)
        self.duplicate_finder.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show_results(self, duplicates):
        self.duplicates = duplicates
        self.results_list.clear()
        for hash, files in duplicates.items():
            set_item = QListWidgetItem(f"Duplicate set ({len(files)} files):")
            set_item.setData(Qt.UserRole, hash)
            self.results_list.addItem(set_item)
            for file in files:
                file_item = QListWidgetItem(f"  {file}")
                file_item.setData(Qt.UserRole, hash)
                self.results_list.addItem(file_item)

    def show_duplicate_images(self, item):
        if not item.text().startswith("  "):
            self.delete_btn.setEnabled(False)
            self.image_preview.clear()
            return

        image_path = item.text().strip()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_preview.setPixmap(pixmap)
            self.delete_btn.setEnabled(True)
        else:
            self.image_preview.setText("Unable to load image")
            self.delete_btn.setEnabled(False)

    def delete_selected_image(self):
        current_item = self.results_list.currentItem()
        if not current_item or not current_item.text().startswith("  "):
            return

        file_path = current_item.text().strip()
        hash = current_item.data(Qt.UserRole)

        reply = QMessageBox.question(self, 'Delete Image',
                                     f"Are you sure you want to delete '{file_path}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
                self.duplicates[hash].remove(file_path)
                
                # Remove the item from the list
                self.results_list.takeItem(self.results_list.row(current_item))

                # Update the duplicate set item
                set_items = self.results_list.findItems(f"Duplicate set", Qt.MatchStartsWith)
                for set_item in set_items:
                    if set_item.data(Qt.UserRole) == hash:
                        remaining_files = len(self.duplicates[hash])
                        set_item.setText(f"Duplicate set ({remaining_files} files):")
                        break

                # If only one file remains, remove the entire set
                if remaining_files <= 1:
                    for i in range(self.results_list.count() - 1, -1, -1):
                        item = self.results_list.item(i)
                        if item.data(Qt.UserRole) == hash:
                            self.results_list.takeItem(i)
                    del self.duplicates[hash]

                self.image_preview.clear()
                self.delete_btn.setEnabled(False)
                QMessageBox.information(self, "Success", f"Image '{file_path}' has been deleted.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete image: {str(e)}")