from kivy.app import App
from kivy.uix.video import Video
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config

#f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\inactivity_time.txt', "w")
#f.write("0.0")
#f.close()

# Set window to fullscreen
Window.fullscreen = 'auto'

def get_video():
    f = open('C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\config.txt')
    temp = f.readline()
    f.close()
    print(temp)
    temp2 = ""
    for c in temp:
        if(c == '\\'):
            temp2 = temp2 + '\\\\'
        else:
            temp2 = temp2 + c

    return "C:\\Users\\dwase\\Desktop\\kivy\\wygaszacz_ekranu\\" + temp.strip()
    #return 'screensavers//clip_1.mp4'

class FullscreenVideoPlayer(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create video widget
        self.video = Video(
            #source='clip_1.mp4',
            source = get_video(),
            state='play',
            options={'allow_stretch': True, 'eos': 'loop'},
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        
        # Bind video events
        self.video.bind(eos=self.on_eos)
        self.add_widget(self.video)

    def on_touch_down(self, touch):
        exit(0)

    def on_eos(self, instance, value):
        """Loop video when it ends"""
        if value == 'eos':
            self.video.position = 0
            self.video.state = 'play'

class ScreenSaverPlayVideoApp(App):
    def build(self):
        return FullscreenVideoPlayer()

if __name__ == '__main__':
    ScreenSaverPlayVideoApp().run()