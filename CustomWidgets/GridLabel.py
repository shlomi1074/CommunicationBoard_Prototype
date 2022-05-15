import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from gtts import gTTS
from playsound import playsound


class GridLabel(QLabel):
    def __init__(self,  name, text, pixmap, parent=None):
        super().__init__(parent)
        self.name = name
        self.text = text
        self.pixmap = r'.\Resources\apple-icon.png'
        self.setPixmap(QPixmap(self.pixmap))

    def mouseReleaseEvent(self, event):
        temp = self.name.replace(" ", "")
        sound_name = temp + ".mp3"
        try:
            tts = gTTS(self.text, lang='iw', slow=True)
            tts.save(sound_name)
            playsound(sound_name)
            if os.path.exists(sound_name):
                os.remove(sound_name)
        except:
            if os.path.exists(sound_name):
                os.remove(sound_name)
