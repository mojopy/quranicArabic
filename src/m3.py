import json
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.text import LabelBase

# Register the custom Arabic font
LabelBase.register(name="ArabicFont", fn_regular="fonts/Hafs.ttf")

class PracticeWordsApp(App):
    def build(self):
        # Load the words from the JSON file
        try:
            with open("/home/sa/Documents/app/quranicArabic/src/words.json", "r", encoding="utf-8") as file:
                self.words_data = list(json.load(file).items())  # Convert to list for easier indexing
        except FileNotFoundError:
            return Label(text="Error: words.json not found", font_name="ArabicFont", font_size=24)
        except json.JSONDecodeError:
            return Label(text="Error: Failed to parse words.json", font_name="ArabicFont", font_size=24)

        # Initialize variables
        self.current_word = None
        self.showing_english = True

        # Main layout
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Input field for number of words
        self.input_field = TextInput(
            hint_text="Enter number of words to practice",
            multiline=False,
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.input_field)

        # Button to start practicing
        start_button = Button(
            text="Start Practice",
            size_hint=(1, 0.1),
            on_press=self.start_practice
        )
        layout.add_widget(start_button)

        # Label to display words
        self.word_label = Label(
            text="",
            font_name="ArabicFont",
            font_size=40,
            halign="center",
            valign="middle"
        )
        self.word_label.bind(size=self.word_label.setter('text_size'))  # Adjust text wrapping
        layout.add_widget(self.word_label)

        # Button to toggle between English and Arabic
        toggle_button = Button(
            text="Toggle Word",
            size_hint=(1, 0.1),
            on_press=self.toggle_word
        )
        layout.add_widget(toggle_button)

        return layout

    def start_practice(self, instance):
        # Get the number of words to practice
        try:
            num_words = int(self.input_field.text)
            if num_words <= 0 or num_words > len(self.words_data):
                raise ValueError
        except ValueError:
            self.word_label.text = "Invalid input! Enter a number between 1 and {}".format(len(self.words_data))
            return

        # Choose a random word from the first N words
        self.current_word = random.choice(self.words_data[:num_words])
        self.showing_english = True
        self.update_label()

    def toggle_word(self, instance):
        # Toggle between English and Arabic
        if self.current_word:
            self.showing_english = not self.showing_english
            self.update_label()
        else:
            self.word_label.text = "Press 'Start Practice' first!"

    def update_label(self):
        # Update the label text based on the toggle state
        if self.showing_english:
            self.word_label.text = self.current_word[0]  # English word
        else:
            self.word_label.text = self.current_word[1]  # Arabic word

if __name__ == "__main__":
    PracticeWordsApp().run()
