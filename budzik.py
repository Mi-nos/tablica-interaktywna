from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label #czasami przydatny
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import threading
from playsound import playsound



class AlarmApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        # odliczanie
        self.time_input = TextInput(text="MM:SS", font_size=50, halign='center', readonly=False)
        self.add_widget(self.time_input)

        # Przycisk do uruchomienia alarmu
        self.start_button = Button(text="Ustaw Budzik", font_size=50,  on_press=self.set_alarm)
        self.add_widget(self.start_button)
        self.clock_event = None  # Zmienna do przechowywania zegara

    def set_alarm(self, instance):
        try:
            # Parsowanie czasu w formacie MM:SS
            time_parts = self.time_input.text.split(":")
            if len(time_parts) != 2: #jeśli format jest niezgodny to nie działa
                return

            minutes = int(time_parts[0])
            seconds = int(time_parts[1])
            self.total_seconds = minutes * 60 + seconds

            if self.total_seconds <= 0:
                return

            # Ustawienie pola tekstowego jako tylko do odczytu
            self.time_input.readonly = True

            self.start_timer()
        except ValueError:
            pass

    def start_timer(self):
        if self.clock_event:
            self.clock_event.cancel()
        self.clock_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.total_seconds > 0:
            minutes, seconds = divmod(self.total_seconds, 60)
            self.time_input.text = f"{minutes:02}:{seconds:02}"  #aktualizacja czasu
            self.total_seconds -= 1
        else:
            self.time_input.text = "00:00"
            Clock.unschedule(self.clock_event)
            self.play_alarm_sound()
            self.time_input.readonly = False  #odblokuj jak skończysz odlizać

    def play_alarm_sound(self):
        threading.Thread(target=lambda: playsound("C:/Users/Student/Desktop/test/alarmclock.mp3"), daemon=True).start() #dodaj przycisk snooze

class AlarmClockApp(App):
    def build(self):
        return AlarmApp()

if __name__ == "__main__":
    AlarmClockApp().run()


#TODO rozdziel to wszystko na widoki z kivy language i logikę (2 pliki)
