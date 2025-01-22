from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder
import re  # Regular expression library

Builder.load_string('''
<CalculatorLayout>:
    orientation: 'vertical'

    # Display area
    Label:
        id: display
        text: '0'
        font_size: 40
        size_hint_y: 0.2
        halign: 'right'
        valign: 'center'
        text_size: self.size

    Label:
        id: bin_display
        text: '0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000'
        font_size: 20
        size_hint_y: 0.1
        halign: 'right'
        valign: 'center'
        text_size: self.size

    # Mode toggles
    BoxLayout:
        size_hint_y: 0.1
        ToggleButton:
            text: 'HEX'
            group: 'mode'
            on_press: root.set_mode('hex')
        ToggleButton:
            text: 'DEC'
            group: 'mode'
            state: 'down'  # Default to decimal
            on_press: root.set_mode('dec')            
        ToggleButton:
            text: 'OCT'
            group: 'mode'
            on_press: root.set_mode('oct')
        ToggleButton:
            text: 'BIN'
            group: 'mode'
            on_press: root.set_mode('bin')
    BoxLayout:
        size_hint_y: 0.1
        ToggleButton:
            text: 'QWORD'
            group: 'word_length'
            state: 'down'  # Default to decimal
            on_press: root.word_length = 64
        ToggleButton:
            text: 'DWORD'
            group: 'word_length'
            on_press: root.word_length = 32
        ToggleButton:
            text: 'WORD'
            group: 'word_length'
            on_press: root.word_length = 16
        ToggleButton:
            text: 'BYTE'
            group: 'word_length'
            on_press: root.word_length = 8

    # Buttons layout
    GridLayout:
        cols: 5
        rows: 8
        size_hint_y: 0.7

        # First row
        Button:
            id: 7
            text: '7'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            id: 8
            text: '8'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            id: 9
            text: '9'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            text: '/'
            on_press: root.on_button_press(self.text)
        Button:
            id: A
            text: 'A'
            on_press: root.on_button_press(self.text)
            disabled: True

        # Second row
        Button:
            id: 4
            text: '4'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            id: 5
            text: '5'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            id: 6
            text: '6'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            text: '*'
            on_press: root.on_button_press(self.text)
        Button:
            id: B
            text: 'B'
            on_press: root.on_button_press(self.text)
            disabled: True

        # Third row
        Button:
            text: '1'
            on_press: root.on_button_press(self.text)
        Button:
            id: 2
            text: '2'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            id: 3
            text: '3'
            on_press: root.on_button_press(self.text)
            disabled: False
        Button:
            text: '-'
            on_press: root.on_button_press(self.text)
        Button:
            id: C
            text: 'C'
            on_press: root.on_button_press(self.text)
            disabled: True

        # Fourth row
        Button:
            text: 'CLEAR'
            on_press: root.clear_display()
        Button:
            text: '0'
            on_press: root.on_button_press(self.text)
        Button:
            text: '='
            on_press: root.calculate_result()
        Button:
            text: '+'
            on_press: root.on_button_press(self.text)
        Button:
            id: D
            text: 'D'
            on_press: root.on_button_press(self.text)
            disabled: True

        Button:
            text: 'MOD'
            on_press: root.on_button_press(self.text)
        Button:
            text: 'RSH'
            on_press: root.on_button_press(self.text)
        Button:
            text: 'LSH'
            on_press: root.on_button_press(self.text)
        Button:
            text: 'ROL'
            on_press: root.calculate_result()
        Button:
            id: E
            text: 'E'
            on_press: root.on_button_press(self.text)
            disabled: True

        Button:
            text: 'ROR'
            on_press: root.calculate_result()
        Button:
            text: 'AND'
            on_press: root.on_button_press(self.text)
        Button:
            text: 'OR'
            on_press: root.on_button_press(self.text)
        Button:
            text: 'XOR'
            on_press: root.on_button_press(self.text)
        Button:
            id: F
            text: 'F'
            on_press: root.on_button_press(self.text)
            disabled: True

        # Fifth row (added NOT and <- buttons)
        Button:
            text: 'NOT'
            on_press: root.on_button_press(self.text)
        Button:
            text: '<-'
            on_press: root.backspace()
        Button:
            text: ''
            disabled: True
        Button:
            text: ''
            disabled: True
        Button:
            text: ''
            disabled: True
''')

class CalculatorLayout(BoxLayout):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.first_element = ""
        self.second_element = ""
        self.current_operation = ""

        self.mode = "dec"
        self.result = "0"
        self.word_length = 64

        # konfiguracje przycisków
        self.hex_buttons = "23456789ABCDEF"
        self.dec_buttons = "23456789"
        self.oct_buttons = "234567"


    def set_mode(self, mode="dec"):
        """Ustawia tryb wyświetlania."""
        #najpierw
        self.mode = mode
        self.update_display()
        self.update_button_states()

    def update_button_states(self):
        """Aktualizuje stany przycisków w zależności od trybu."""
        #wyłącza przyciski nieznajdujące się w danej konfiguracji, włącza pozostałe (0 i 1 zawsze są włączone)
        if self.mode == "hex":
            for button_id in self.hex_buttons:
                self.ids[button_id].disabled = False

        elif self.mode == "dec":
            for button_id in self.hex_buttons:
                self.ids[button_id].disabled = True
            for button_id in self.dec_buttons:
                self.ids[button_id].disabled = False

        elif self.mode == "oct":
            for button_id in self.hex_buttons:
                self.ids[button_id].disabled = True
            for button_id in self.oct_buttons:
                self.ids[button_id].disabled = False

        elif self.mode == "bin":
            for button_id in self.hex_buttons:
                self.ids[button_id].disabled = True


    def on_button_press(self, value):
        """
        Zarządza zdarzeniami związanymi z naciśnięciem przycisków.
        """
        #przypadek A: wybieramy operator
        if value in "+-*/MODRSHLSHANDORXOR":
            #przypadek 1A: nie ma pierwszego składnika -> nic nie robimy
            if self.first_element == "":
                return
            #przypadek 2A: mamy składniki i operator -> operacja "=" i zaznaczony operator jest nowym zapamiętanym operatorem
            if self.second_element != "":
                self.calculate_result() #calculate_result zawsze uruchamia update_display

            #przypadek 3A: mamy pierwszy składnik -> zapamiętaj operator
            self.current_operation = value
            self.second_element = ""
            return
        #przypadek B: wybieramy cyfrę -> wyświetlamy ją
        else:
            #przypadek 1B: nie ma wybranej operacji -> przypisz do pierwszego składnika
            if self.current_operation == "":
                self.first_element += value
                self.result = self.first_element
                self.update_display()
            #przypadek 2B: operacja jest wybrana -> przypisz do drugiego składnika
            else:
                self.second_element += value
                self.result = self.second_element
                self.update_display()


    def calculate_result(self):
        """
        Ewaluuje składniki i operację, wyświetla wynik, zapisuje go do pierwszego składnika.
        """
        #Przypadek A: Operatory jednoskładnikowe TODO
        if (self.current_operation == "ROL"):
            self.rol()
            return
        
        if (self.current_operation == "ROR"):
            self.ror()
            return

        self.current_operation = self.current_operation.replace('MOD', '%')
        self.current_operation = self.current_operation.replace('AND', '&')
        self.current_operation = self.current_operation.replace('OR', '|')
        self.current_operation = self.current_operation.replace('XOR', '^')
        self.current_operation = self.current_operation.replace('SHL', '<<')
        self.current_operation = self.current_operation.replace('SHR', '>>')

        #Przypadek B: Operatory dwuskładnikowe
        try:
            print("Obecna operacja: " + self.first_element + " " + self.current_operation + " " + self.second_element)
            self.result = eval(self.first_element + self.current_operation + self.second_element)
        #Przypadek C: klikniemy "=" bez wymaganych operatorów
        except SyntaxError:
            return
        except ZeroDivisionError: #wyłapywanie dzielenia przez zero
            self.result = "Cannot divide by zero"
            self.update_display()
        else:
            self.update_display()
            self.first_element = str(self.result)
            #

    def update_display(self):
        """
        Reaguje na wydarzenia wywołane przez inne przyciski
        """
        if self.mode == 'hex':
            self.ids.display.text = str(hex(int(self.result))[2:].upper())
        elif self.mode == 'dec':
            self.ids.display.text = str(self.result)
        elif self.mode == 'oct':
            self.ids.display.text = str(oct(int(self.result))[2:])
        elif self.mode == 'bin':
            self.ids.display.text = str(bin(int(self.result))[2:])

        binary = bin(int(self.result))[2:]  # Zamienia wynik na postać binarną
        padded_binary = binary.zfill(64)  # Wypełnia zerami do 64 bitów
        grouped_binary = ' '.join(
            [padded_binary[i:i + 4] for i in range(0, len(padded_binary), 4)])
        self.ids.bin_display.text = grouped_binary

    def clear_display(self):
        """
        Resetuje zapamiętane operatory i składniki.
        """
        self.current_operation = ""
        self.first_element = ""
        self.second_element = ""
        self.result = "0"
        self.update_display()


    def rol(self):
        """
        Rotate left (ROL) the value by the specified number of bits, considering the word length.
        """

        match = re.match(r'(\d+)\s*ROL\s*(\d+)', self.current_operation)
        if match:
            value = int(match.group(1))
            amount = int(match.group(2))
            result = ((value << amount) & ((1 << self.word_length) - 1)) | (value >> (self.word_length - amount))
            self.result = str(result)
            self.display_result()

    def ror(self):
        """
        Rotate right (ROR) the value by the specified number of bits, considering the word length.
        """

        match = re.match(r'(\d+)\s*ROR\s*(\d+)', self.current_operation)
        if match:
            value = int(match.group(1))
            amount = int(match.group(2))
            result = (value >> amount) | ((value << (self.word_length - amount)) & ((1 << self.word_length) - 1))
            self.result = str(result)
            self.display_result()


class CalculatorApp(App):
    def build(self):
        return CalculatorLayout()


if __name__ == "__main__":
    CalculatorApp().run()
