from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

class YourApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        #layout = GridLayout(cols=2)
        l0 = Label(text="Wykaz informacji o urzadzeniu")    #(kliknij w wybor)
        b1 = Button(text='Nazwa urzadzenia  :  Raspberry Pi 5')
        b2 = Button(text='Model  : Raspberry Pi 5 Model B Rev 1.0')
        #b3 = Button(text='')
        b4 = Button(text='Numer seryjny procesora  :  5afffa37823869ef')
        b5 = Button(text='Pamiec RAM  :  8Gi')
        b6 = Button(text='Pamiec urzadzenia : 42,9GB')
        b7 = Button(text='Wroc')

        #bindowanie klawiszy
        b1.bind(on_press=self.show_device_name)
        b2.bind(on_press=self.show_device_model)
        #b3.bind(on_press=self.show_device_compilation_number)
        b4.bind(on_press=self.show_processor_name)
        b5.bind(on_press=self.show_ram)
        b6.bind(on_press=self.show_device_storage)
        b7.bind(on_press=self.close_app)


        #dodawanie klawiszy do layoutu
        layout.add_widget(l0)
        layout.add_widget(b1)
        layout.add_widget(b2)
        #layout.add_widget(b3)
        layout.add_widget(b4)
        layout.add_widget(b5)
        layout.add_widget(b6)
        layout.add_widget(b7)

        return layout
    
    def show_device_name(self, instance):
        pass
    
    def show_device_model(self, instance):
        pass

    def show_device_compilation_number(self, instance):
        pass

    def show_processor_name(self, instance):
        pass

    def show_ram(self, instance):
        pass

    def show_device_storage(self, instance):
        pass

    def close_app(self, instance):
        App.get_running_app().stop()  # Zatrzymanie aplikacji


YourApp().run()