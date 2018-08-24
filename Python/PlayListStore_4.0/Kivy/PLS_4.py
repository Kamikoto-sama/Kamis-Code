from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.popup import Popup

Config.set("graphics","resizable",1)
Config.set("graphics","width",860)
Config.set("graphics","height",592)

VER = "4.0"
class CustomPopup(Popup):pass

class Root(BoxLayout):
	checkbox_is_active = ObjectProperty(False)

	def clicked(self, act, value):
		print("AEAH")

	blue = ObjectProperty(True)
	red = ObjectProperty(False)
	green = ObjectProperty(False)

	def switch_on(self,act,state):
		print("hello")

	def open(self):
		the_pop = CustomPopup()
		the_pop.open()

	def spinner(self,value):
		print("Spinner")

class MainForm1App(App):
	def build(self):
		Window.clearcolor = (.59,.59,.59,1)

		return Root()
MainForm1App().run()