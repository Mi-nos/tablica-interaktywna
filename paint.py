from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.colorpicker import ColorPicker
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.boxlayout import BoxLayout

class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        color = (random(), 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 30.
            if touch.x >= 300:
                touch.ud['line'] = Line(points=(touch.x, touch.y))
            else:
                return

    def on_touch_move(self, touch):
        if touch.x >= 300:
            touch.ud['line'].points += [touch.x, touch.y]
        else:
            return

class MyPaintApp(App):


    def build(self):
        parent = Widget()
        testLayout = BoxLayout(size=(300,300))
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear', pos=(0,300))
        clearbtn.bind(on_release=self.clear_canvas)
        color_picker = ColorPicker()
        parent.add_widget(testLayout)
        testLayout.add_widget(color_picker)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()


#TODO możesz spróbować rozdzielić plik na widok .kv
