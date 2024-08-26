import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget
from duplicate_finder import DuplicateFinderTab
from image_viewer import ImageViewerTab

class ImagePrepTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Prep Tool")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.init_ui()

    def init_ui(self):
        self.duplicate_finder_tab = DuplicateFinderTab()
        self.image_viewer_tab = ImageViewerTab()

        self.tabs.addTab(self.duplicate_finder_tab, "Duplicate Finder")
        self.tabs.addTab(self.image_viewer_tab, "Image Viewer")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImagePrepTool()
    window.show()
    sys.exit(app.exec_())