from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

class KebsCalcApp(App):
    def build(self):
        layout = FloatLayout()

        # Tytuł aplikacji
        title = Label(text="KebsCalc", font_size=50, size_hint=(None, None), size=(400, 100), pos=(150, 450))
        layout.add_widget(title)

        # Ilość mięsa
        meat_label = Label(text="Ilość mięsa(g):", font_size=25, size_hint=(None, None), size=(250, 50), pos=(50, 350))
        layout.add_widget(meat_label)

        # Pole do wprowadzania ilości mięsa
        self.meat_input = TextInput(font_size=25, size_hint=(None, None), size=(250, 50), pos=(300, 350))
        layout.add_widget(self.meat_input)

        # Cena
        price_label = Label(text="Cena(gr):", font_size=25, size_hint=(None, None), size=(250, 50), pos=(50, 250))
        layout.add_widget(price_label)

        # Pole do wprowadzania ceny
        self.price_input = TextInput(font_size=25, size_hint=(None, None), size=(250, 50), pos=(300, 250))
        layout.add_widget(self.price_input)

        # Przycisk do zatwierdzenia
        self.result_label = Label(text="", font_size=25, size_hint=(None, None), size=(400, 50), pos=(150, 100))
        layout.add_widget(self.result_label)

        calculate_button = Button(
            text="Poznaj współczynnik opłacalności",
            font_size=20,
            size_hint=(None, None),
            size=(400, 50),
            pos=(150, 50)
        )
        calculate_button.bind(on_press=self.calculate_efficiency)
        layout.add_widget(calculate_button)

        return layout

    def calculate_efficiency(self, instance):
        try:
            # Pobranie danych z pól tekstowych
            meat_amount = float(self.meat_input.text)
            price_per_gram = float(self.price_input.text)
            
            # Obliczenie współczynnika opłacalności
            efficiency = meat_amount / price_per_gram
            self.result_label.text = f"Współczynnik opłacalności: {efficiency:.2f}"
        except ValueError:
            self.result_label.text = "Błąd! Wprowadź poprawne dane."

if __name__ == "__main__":
    KebsCalcApp().run()
