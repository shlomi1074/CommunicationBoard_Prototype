import os
import gtts
import playsound
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from gtts import gTTS
from playsound import playsound
import os

class GridLabel(QLabel):
    def __init__(self,  name, text, pixmap, parent=None):
        super().__init__(parent)
        self.name = name
        self.text = text
        self.pixmap = pixmap
        self.setPixmap(QPixmap(self.pixmap))
        self.parent = parent

    def mouseReleaseEvent(self, event):
        sound_name = os.getcwd() + r"\output.mp3"
        sound_name = sound_name.replace("\\", "/")
        if os.path.exists(sound_name):
            os.remove(sound_name)
        try:
            tts = gTTS(self.text, lang='iw', slow=False)
            tts.save(sound_name)
            playsound(sound_name)
        except Exception as e:
            print("failed to play audio " + str(e))



