from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanelItem, TabbedPanelHeader

Config.set("graphics","resizable",1)
Config.set("graphics","width",860)
Config.set("graphics","height",592)

# VARS
VER = "4.0"
# VARS

class NewP(BoxLayout):
	pass
class NewT(BoxLayout):
	pass

class Root(BoxLayout):
	font = "consolab"
	_main = 0

	def newP(self,main,PName):
		Tab = TabbedPanelItem(text = PName)
		Tab.add_widget(NewP())
		main.add_widget(Tab, index = 0)
		main.switch_to(Tab,do_scroll=True)
		self._main = main
	
	# def closeP(self,PName):
	# 	print(PName)
	# 	self._main.remove_widget(PName)

	def addP(self,PName, select_p, main):
		if PName.opacity ==0:
			PName.opacity = 1
			PName.focus = True
			PName.text ="PL" + str(len(select_p.values)+1)
			PName.select_all()
		else:
			PName.opacity = 0
			PName.focus = False
			select_p.text = PName.text
			select_p.values.insert(0,PName.text)
			self.newP(main, PName.text)

class MainFormApp(App):
	def build(self):
		global VER
		self.title = "PlayListStore " + VER
		return Root()
MainFormApp().run()