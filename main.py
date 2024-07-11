import google.generativeai as genai
from gtts import gTTS
import io
import pygame
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QMovie, QImage, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize
import os
import random

genai.configure(api_key=os.environ.get('geminiapi'))
pygame.mixer.init()
generation_config = {

    "max_output_tokens": 1000,
    "temperature": 0

}

def play_sound(audio_bytes):
    pygame.mixer.music.load(audio_bytes, 'mp3')
    pygame.mixer.music.play()

model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)

randomlevel = random.randint(1,10000)
response=model.generate_content(f'Generate me a common but random spanish words sentance in mexican spanish that would be used in every day life a lot. Only give one spanish sentance and no english translation or anything else, just the sentance, I want it to be 7-15 words. Give me the {randomlevel}th response that you thought of.')


spanish = response.text

print(spanish)


tts = gTTS(text=spanish, lang='es')

audio_buffer = io.BytesIO()
tts.write_to_fp(audio_buffer)

# Move the cursor of the BytesIO object to the beginning
audio_buffer.seek(0)

# Play the audio
play_sound(audio_buffer)

# Keep the program running until the audio finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)


class TTSApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Language Master')
        self.setGeometry(100,100,338,732)

         # Create layout and widgets
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
       
        

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTrailing)
    
        

        self.text_input = QLineEdit(self)
        self.text_input.setFont(QFont('Arial', 14))
        self.text_input.setPlaceholderText('Type your text here...')
        
        
       
    
      
        self.gif_button = QPushButton(self)
        self.gif_button.setGeometry(85, 600, 200, 100)
        self.gif_button.setIcon(QIcon('slower.png'))
        self.gif_button.setIconSize(QSize(200, 100))
        self.gif_button.setFlat(True)
    
        
   
        
        self.button = QPushButton('Submit')
        self.button.setFont(QFont('Arial', 14))
        self.button.clicked.connect(self.analyze)

         # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_input)
 
        self.layout.addWidget(self.button)
        
        pixmap = QPixmap("letters.png") 
        
        self.gif_button.raise_()

        pixmap = pixmap.scaled(350, 750, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(False)  
        
        
        # Set layout for the main window
        self.setLayout(self.layout)
        
        # Apply some basic styling
        self.setStyleSheet("""
                           
             QMainWindow {
                background-color: #282e2a;
            }

                           
            QWidget {
                background-color: #282e2a;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            
        """)


    def analyze(self):
        text = self.text_input.text()
        if text:
            
            rating = model.generate_content(f'tell me how close from 1% to 100% is {text} for the spanish sentance {spanish}. Rate it based on vocabulary words transelated correctly, grammar, and context. If everything is correct, give 100%. I only want the percent rating and a one sentance explanation of what was translated wrong.')
            translation = model.generate_content(f'what is your english translation of {spanish}. I just want the direct english translation as a sentance and nothing else.')
            print(rating.text)
            print(translation.text)

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = TTSApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()              
