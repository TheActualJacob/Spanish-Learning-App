import google.generativeai as genai
from gtts import gTTS
import io
import pygame
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QFont, QPixmap, QIcon
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
response = model.generate_content('Generate me a common but random spanish words sentance in mexican spanish that would be used in every day life a lot. Only give one spanish sentance and no english translation or anything else, just the sentance, I want it to be 7-15 words. Make sure to give a diferent response each time')

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
        self.setGeometry(100, 100, 338, 732)

        # Create layout and widgets
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTrailing)
        self.label.setGeometry(0, 0, 338, 732)

        self.text_input = QLineEdit(self)
        self.text_input.setFont(QFont('Arial', 14))
        self.text_input.setPlaceholderText('Type your text here...')
        self.text_input.setGeometry(0, 20, 338, 40)
        
        self.gif_button = QPushButton(self)
        self.gif_button.setGeometry(75, 500, 200, 100)
        self.gif_button.setIcon(QIcon('slower.png'))
        self.gif_button.setIconSize(QSize(200, 100))
        self.gif_button.setFlat(True)

        self.button = QPushButton('Submit', self)
        self.button.setFont(QFont('Arial', 14))
        self.button.setGeometry(94, 450, 150, 40)
        self.button.clicked.connect(self.analyze)

        # Set up the background image for the label
        pixmap = QPixmap("letters.png")
        pixmap = pixmap.scaled(338, 732, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(False)
        
        self.gif_button.raise_()

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
