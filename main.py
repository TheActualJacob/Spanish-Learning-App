import google.generativeai as genai
from gtts import gTTS
import io
import pygame
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QGridLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QMovie, QImage, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize, QTimer
import os
import random
from pydub import AudioSegment


class generation:


    def play_sound(self, audio_bytes):
        if audio_bytes ==1:
            return 
        pygame.mixer.music.load(audio_bytes, 'mp3')
        pygame.mixer.music.play()


    def generatesentance(self):
        genai.configure(api_key=os.environ.get('googleapikey'))
        pygame.mixer.init()
        

        generation_config = {

            "max_output_tokens": 1000,
            "temperature": 1,
            "top_p": random.uniform(.9,1)
        }
        self.model = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
        randomlevel = random.randint(1,10000)
        print(randomlevel)
        response=self.model.generate_content(f'You are asked to generate a common sentance in spanish.This is how you should generate it: 1. Choose 10000 random phrases and giv me the {randomlevel} one 2. Make sure that the 10000 random sentances are differnt each time 3. Make sure that you never generate the same sentance. 4. Make sure the only thing you are responding with is the sentance in spanish and nothing else. 5. No emojis only character')
        self.spanish1 = response.text

        print(self.spanish1)

        # Play the audio
        self.play_sound(self.soundsetup())
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def soundsetup(self, slower=False):

        try:
            tts = gTTS(text=self.spanish1, lang='es')
        except:
            return 1

        self.audio_buffer = io.BytesIO()
        tts.write_to_fp(self.audio_buffer)
        # Move the cursor of the BytesIO object to the beginning
        self.audio_buffer.seek(0)

        if slower == True:
            audio = AudioSegment.from_file(self.audio_buffer, format="mp3")
            # Change the playback speed (e.g., slower by 50%)
            slower_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 0.75) }).set_frame_rate(audio.frame_rate)

            # Export the slower audio to a BytesIO object
            slower_audio_fp = io.BytesIO()
            slower_audio.export(slower_audio_fp, format="mp3")
            return slower_audio_fp

        return self.audio_buffer

       


class TTSApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle('Language Master')
        self.setGeometry(100,100,338,732)

         # Create layout and widgets
        self.layout = QVBoxLayout()
        self.layout1 = QHBoxLayout()
        self.layoout2 = QVBoxLayout()
       
        

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        self.generate = generation()
        
        self.gif_button = QPushButton(self)
        self.gif_button.setGeometry(85, 150, 200, 100)
        self.gif_button.setFlat(True)
        try:
            self.gif_button.clicked.connect(lambda: self.generate.play_sound(self.generate.soundsetup(True)))
        except Exception as e:
            self.typein(f'{e} No sentance generated yet!')
        self.text_input = QLineEdit(self)
        self.text_input.setFont(QFont('Arial', 14))
        self.text_input.setPlaceholderText('Type your text here...')


        
        self.newprompt = QPushButton('Generate Sentance')
        self.newprompt.setGeometry(85,190,200,10)
        self.newprompt.setFont(QFont('Arial', 14))

        try:
            self.newprompt.clicked.connect(lambda: self.generate.generatesentance())
        except Exception as e:
            self.typein(e)
 

        
        self.gif_label = QLabel(self)
        self.movie = QMovie('Spanish-Learning-App\slower copy.gif')
        self.gif_label.setMovie(self.movie)
        self.movie.setScaledSize(QSize(190, 85))
        self.movie.start()

        self.layout1.addWidget(self.gif_label)
        self.gif_button.setLayout(self.layout1)
      
        
    
        
        self.explanationlabel = QLabel(self)
        self.explanationlabel.setFont(QFont('Times',15))
        self.explanationlabel.setStyleSheet('color: white;')
        self.explanationlabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.button = QPushButton('Submit')
        self.button.setFont(QFont('Arial', 14))

        
        try:
            self.button.clicked.connect(lambda: self.explanation(*self.analyze(self.text_input.text())))
        except Exception as e:
            self.typein(f'{e} Nothing in text box')

        pixmap = QPixmap("Spanish-Learning-App\letter.png") 

        pixmap = pixmap.scaled(350, 750, Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(False)  

         # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.explanationlabel)
        self.layout.addWidget(self.newprompt)
        
        self.layout.addWidget(self.text_input)
        
 
        self.layout.addWidget(self.button)
        
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda:self.update_text())

        # Set layout for the main window
        self.setLayout(self.layout)
        
        # Apply some basic styling
        self.setStyleSheet("""
                           
            

                           
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


    def analyze(self,text):


        
        
        if self.text_input.text():
            self.text_input.clear()
            try:

                generation_config = {

                "max_output_tokens": 1000,
                "temperature": .2,
                
                }
                self.model1 = genai.GenerativeModel('gemini-1.5-flash', generation_config=generation_config)
                self.rating = self.model1.generate_content(f'You are being used for an app that helps people with their spanish to english translations. You are being asked to grade the users translations from 1-100% based on vocabulary, grammar, and context. You will be provided with the users translation in english, and the sentance in spanish. Please respond first with the percentage you give the user, then a short explanation as to why you gave that rating. If the users sentance is a correct translation, give him 100% and congradulate him. Users translation: {text}. Spanish sentance: {self.generate.spanish1}')
                self.translation = self.model1.generate_content(f'what is your english translation of {self.generate.spanish1}. I just want the direct english translation as a sentance and nothing else.')
            except Exception as e:
                self.current_text = ""
                self.typein(f'Error {e} was raised because you need to generate a sentance first'.split())
                return 1,1
            print('tb1')

            return self.rating.text, self.translation.text
        
        else:
            self.current_text = ""
            self.typein('Nothing in text box'.split())
            return 1,1


    
    


   
    def explanation(self, score, definition):
        
        if score ==1:
            print(score)
            return None
        
        else:
            print('test')
            self.full_text = f'Your translation was: {score} \n The correct transelation was: {definition}'
            self.current_text = ""
            
            self.typein(self.full_text.split())
    

        print('tb3')
    def typein(self, totype):
        self.newtex = totype
        self.timer.start(100)
        self.n=0
        
        self.thresholds = [30, 60, 90,120,150,180,210,240,270,300,330,360,390]
        self.thresholds_crossed = {threshold: False for threshold in self.thresholds}
        
    def update_text(self):
        
       
 
        if self.n < len(self.newtex):
            self.current_text += f'{self.newtex[self.n]} '
            self.explanationlabel.setText(self.current_text)
            for threshold in self.thresholds:
                if len(''.join(self.current_text)) >= threshold and self.n != 0 and not self.thresholds_crossed[threshold]:
                   
                    self.current_text = self.current_text + '\n'
                    self.thresholds_crossed[threshold] = True
            self.n=self.n+1
            
          
        
        else:
            self.timer.stop()
            
       
        
        
        




        
    
    

        

   




# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = TTSApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()              