import os
import glob
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.clock import Clock

Builder.load_string('''
<MainScreen>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    
    Label:
        text: 'Wybierz wygaszacz:'
        font_size: '20sp'
        size_hint_y: None
        height: 40
    
    ScrollView:
        size_hint_y: 0.7
        bar_width: 10
        
        GridLayout:
            id: file_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
            padding: 5
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.2
        spacing: 5
        
        Label:
            text: 'Czas do uruchomienia (sekundy):'
            size_hint_y: 0.3
            
        TextInput:
            id: timeout_input
            text: '300'
            input_filter: 'int'
            multiline: False
            size_hint_y: 0.3
            font_size: 20
            
        Button:
            text: 'ZATWIERDŹ'
            size_hint_y: 0.4
            on_press: root.save_config()
            background_color: 0, 0.7, 0, 1
            font_size: 20
    
    Label:
        text: root.status
        size_hint_y: None
        height: 30
        color: 1, 0, 0, 1
''')

class MainScreen(BoxLayout):
    status = StringProperty('Wybierz plik i podaj czas')
    selected_file = StringProperty('')
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_files, 0.1)

    def load_files(self, *args):
        folder = os.path.join(os.path.dirname(__file__), 'screensavers')
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            self.status = 'Utworzono folder screensavers'
        
        try:
            files = glob.glob(os.path.join(folder, '*.mp4'))
        except Exception as e:
            self.status = f'Błąd dostępu: {str(e)}'
            return
        
        grid = self.ids.file_grid
        grid.clear_widgets()
        
        if not files:
            self.status = 'Brak plików MP4 w folderze!'
            return
            
        for path in files:
            try:
                btn = Button(
                    text=os.path.basename(path),
                    size_hint_y=None,
                    height=50,
                    on_press=lambda instance, p=path: self.select_file(p),
                    background_color=(0.2, 0.6, 1, 1),
                    color=(1, 1, 1, 1),
                    font_size=16
                )
                grid.add_widget(btn)
            except Exception as e:
                self.status = f'Błąd tworzenia przycisku: {str(e)}'

    def select_file(self, path):
        try:
            self.selected_file = os.path.relpath(path, start=os.path.dirname(__file__))
            self.status = f'Wybrano: {os.path.basename(path)}'
        except Exception as e:
            self.status = f'Błąd wyboru pliku: {str(e)}'

    def save_config(self):
        if not self.selected_file:
            self.status = 'Nie wybrano pliku!'
            return
            
        timeout = self.ids.timeout_input.text
        
        try:
            timeout_int = int(timeout)
            if timeout_int <= 0:
                raise ValueError("Czas musi być większy od 0")
        except ValueError as e:
            self.status = f'Nieprawidłowy czas: {str(e)}'
            return
        
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(f'{self.selected_file}\n{timeout_int}')
            
            self.status = f'Zapisano konfigurację do:\n{config_path}'
        except PermissionError:
            self.status = 'Brak uprawnień do zapisu!'
        except Exception as e:
            self.status = f'Błąd zapisu: {str(e)}'

class ScreensaverApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    ScreensaverApp().run()