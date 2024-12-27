import flet as ft
import json
import random
from typing import Dict, List

class FlashcardApp:
    def __init__(self):
        self.words: Dict[str, str] = {}
        self.current_words: List[tuple] = []
        self.current_word: tuple = None
        self.is_showing_translation = False
        self.max_words = 0
        self.selected_words_count = 0
        self.drag_start_y = 0

    def load_words(self) -> None:
        """Load words from words.json file"""
        try:
            with open("words.json", "r", encoding="utf-8") as file:
                self.words = json.load(file)
                self.max_words = len(self.words)
        except FileNotFoundError:
            print("words.json file not found!")
            self.words = {}

    def update_word_selection(self, count: int) -> None:
        """Update the selection of words based on slider value"""
        self.selected_words_count = count
        items = list(self.words.items())[:count]
        self.current_words = items
        self.select_random_word()

    def select_random_word(self) -> None:
        """Select a random word from current selection"""
        if self.current_words:
            self.current_word = random.choice(self.current_words)
            self.is_showing_translation = False

    def main(self, page: ft.Page):
        page.title = "Flashcard App"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def on_slider_change(e):
            value = int(e.control.value)
            self.update_word_selection(value)
            word_text.value = self.current_word[0] if self.current_word else ""
            page.update()

        def on_card_tap(e):
            if self.current_word:
                self.is_showing_translation = not self.is_showing_translation
                word_text.value = (
                    self.current_word[1] if self.is_showing_translation 
                    else self.current_word[0]
                )
                page.update()

        def load_new_word():
            """Common function to load a new word"""
            self.select_random_word()
            word_text.value = self.current_word[0] if self.current_word else ""
            page.update()

        # Mouse drag handlers
        def on_pan_start(e):
            self.drag_start_y = e.local_y

        def on_pan_update(e):
            if self.drag_start_y - e.local_y > 50:  # Dragged upward
                load_new_word()
                self.drag_start_y = e.local_y

        # Touch swipe handlers
        def on_vertical_drag_start(e):
            self.drag_start_y = e.local_y

        def on_vertical_drag_update(e):
            if self.drag_start_y - e.local_y > 50:  # Swiped upward
                load_new_word()
                self.drag_start_y = e.local_y

        # Load words first
        self.load_words()

        # Create slider
        slider = ft.Slider(
            min=1,
            max=self.max_words,
            value=1,
            label="{value} words",
            on_change=on_slider_change,
        )

        # Create word text
        word_text = ft.Text(
            value="Tap slider to start",
            size=30,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
        )

        # Create card container with both mouse and touch handlers
        card = ft.Card(
            content=ft.GestureDetector(
                content=ft.Container(
                    content=word_text,
                    padding=20,
                    alignment=ft.alignment.center,
                    width=300,
                    height=200,
                ),
                # Mouse drag events
                on_pan_start=on_pan_start,
                on_pan_update=on_pan_update,
                # Touch swipe events
                on_vertical_drag_start=on_vertical_drag_start,
                on_vertical_drag_update=on_vertical_drag_update,
                # Tap event
                on_tap=on_card_tap,
            ),
            elevation=5,
        )

        # Create platform-specific instructions
        instruction_text = ft.Column(
            [
                ft.Text("Instructions:", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("1. Tap card to flip between English and Arabic", size=14),
                ft.Text("2. Swipe or drag upward for a new word", size=14),
                ft.Text("3. Use slider to adjust number of words", size=14),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Add elements to page
        page.add(
            ft.Column(
                [
                    slider,
                    ft.Container(height=20),
                    card,
                    ft.Container(height=20),
                    instruction_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

if __name__ == "__main__":
    app = FlashcardApp()
    ft.app(target=app.main, view=ft.AppView.WEB_BROWSER)  # Enable web view