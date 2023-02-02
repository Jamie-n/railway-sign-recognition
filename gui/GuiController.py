from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

class MyGridLayout(Widget):
    pass


class MyApp(App):
    def build(self):
        Window.size = (1260, 720)

        return MyGridLayout()


def initialize():
    MyApp().run()