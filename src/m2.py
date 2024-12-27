import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase

# Register the custom Arabic font
LabelBase.register(name="ArabicFont", fn_regular="fonts/Hafs.ttf")

class ArabicWordsApp(App):
    def build(self):
        # Load the words from words.json
        try:
            with open("/home/sa/Documents/app/quranicArabic/src/words.json", "r", encoding="utf-8") as file:
                words_data = json.load(file)
        except FileNotFoundError:
            return Label(text="Error: words.json not found", font_name="ArabicFont", font_size=24)
        except json.JSONDecodeError:
            return Label(text="Error: Failed to parse words.json", font_name="ArabicFont", font_size=24)

        # Create a layout
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Add Labels with Arabic words to the layout
        for english_word, arabic_word in words_data.items():
            arabic_label = Label(
                text=arabic_word,
                font_name="ArabicFont",
                font_size=40,
                halign="center",
                valign="middle"
            )
            arabic_label.bind(size=arabic_label.setter('text_size'))  # Adjust text wrapping
            layout.add_widget(arabic_label)

        return layout

if __name__ == "__main__":
    ArabicWordsApp().run()
