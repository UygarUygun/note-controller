import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget, QLabel

class AlwaysOnTopWidget(QWidget):
    def __init__(self, text_func):
        super().__init__()
        
        # Set the window flags to always stay on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Set the background color to transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set up the label to display the text
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        
        # Set the font and font size of the label
        font = self.label.font()
        font.setPointSize(36)
        self.label.setFont(font)
        
        # Set the palette to use a white text color
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        self.label.setPalette(palette)
        
        # Connect the timer to the text update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_text(text_func()))
        self.timer.start(1000) # Update text every 1 second
        
        # Set the widget size to be slightly smaller than the screen geometry
        screen_geometry = QApplication.primaryScreen().geometry()
        self_width = int(screen_geometry.width() * 0.8)
        self_height = int(screen_geometry.height() * 0.3)
        self.setFixedSize(self_width, self_height)
        
        # Center the widget on the screen
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def update_text(self, text):
        self.label.setText(text)
        self.label.adjustSize()
        self.label.resize(self.label.width() + 10, self.label.height() + 10)
        self.resize(self.label.size() + self.frameSize())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Define a function to generate the text
    def text_func():
        import datetime
        return str(datetime.datetime.now())
    
    # Create the widget with the text function
    widget = AlwaysOnTopWidget(text_func)
    
    # Show the widget
    widget.show()
    
    sys.exit(app.exec())
