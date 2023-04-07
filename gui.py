import sys
from PySide6.QtCore import Qt, QTimer, QRect, QPoint
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from guifunc_show_pitch_librosa import runRead

class AlwaysOnTopWidget(QWidget):
    def __init__(self, text_func):
        super().__init__()
        
        # Set the window flags to always stay on top and remove the window frame
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
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
        palette.setColor(QPalette.WindowText, Qt.magenta)
        self.label.setPalette(palette)
        
        # Connect the timer to the text update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_text(text_func()))
        self.timer.start(2) # Update text every 0.01 second
        
        # Set the widget size to be slightly smaller than the screen geometry
        screen_geometry = QApplication.primaryScreen().geometry()
        #self_width = int(screen_geometry.width() * 0.4)
        #self_height = int(screen_geometry.height() * 0.3)
        self_width = int( screen_geometry.width() / self.label.width())
        self_height = int(self.label.height() / self.label.height())
        #self.setMinimumSize(self_width, self_height)
        
        # Set the widget's position to the bottom-right corner of the screen
        self.screen_rect = QApplication.primaryScreen().geometry()
        self.move(self.screen_rect.bottomRight() - self.rect().bottomRight())
        print(self.screen_rect.bottomRight())
        print(self.rect().bottomRight())
        #self.move(screen_rect.bottomRight())
        
        
        # Remove the window title
        self.setWindowTitle("")
    
    def update_text(self, text):
        self.label.setText(text)
        self.label.adjustSize()
        #self.label.setMaximumSize(self.label.width() + 10, self.label.height() + 10)
        self.resize(self.label.size())
        self.update_position()
        #print(self.height())
    
    def update_position(self):
        self.move(self.screen_rect.bottomRight() - self.rect().bottomRight())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Define a function to generate the text
    def text_func():
        import datetime
        rs = str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute)
        return rs
    
    # Create the widget with the text function
    widget = AlwaysOnTopWidget(runRead)
    
    # Show the widget
    widget.show()
    
    sys.exit(app.exec())
