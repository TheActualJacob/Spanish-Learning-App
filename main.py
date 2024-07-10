import google.generativeai as genai
from gtts import gTTS
import io
import pygame
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


genai.configure(api_key="")
pygame.mixer.init()
generation_config = {

    "max_output_tokens": 1000,
    "temperature": 0

}

def play_sound(audio_bytes):
    pygame.mixer.music.load(audio_bytes, 'mp3')
    pygame.mixer.music.play()

model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)


response=model.generate_content('Generate me a common but random spanish words sentance in mexican spanish that would be used in every day life a lot. Only give one spanish sentance and no english translation or anything else, just the sentance, I want it to be 7-15 words.')


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
        self.setWindowTitle('Text to Speech')
        self.setGeometry(100, 100, 400, 200)

         # Create layout and widgets
        self.layout = QVBoxLayout()
        
        self.label = QLabel('Transelate what you think you heard')
        self.label.setFont(QFont('Arial', 14))
        
        self.text_input = QLineEdit()
        self.text_input.setFont(QFont('Arial', 14))
        self.text_input.setPlaceholderText('Type your text here...')
        
        self.button = QPushButton('Submit')
        self.button.setFont(QFont('Arial', 14))
        self.button.clicked.connect(self.analyze)

         # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.button)
        
        # Set layout for the main window
        self.setLayout(self.layout)
        
        # Apply some basic styling
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
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
            
            rating = model.generate_content(f'tell me how close on a scale of one to ten is {text} for the spanish sentance {spanish}. I dont want anything else except for a number between 1 and ten that is the rating you give.')
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
