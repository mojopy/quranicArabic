from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Register the custom font
LabelBase.register(name='CustomFont', fn_regular=os.path.join(current_dir, '/resources/fonts/Hafs.ttf'))

class MyApp(App):
    def build(self):
        return Label(text='Hello, Quranic Arabic!', font_name='CustomFont')

if __name__ == '__main__':
    MyApp().run()