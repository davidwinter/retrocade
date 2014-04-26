import urwid
import os
import sys
import subprocess

class ArcadeRoms:

	def __init__(self, rom_path = 'roms'):
		self.rom_path = rom_path
	
	def get_games(self):
		dict = {}
		for file in os.listdir(self.rom_path):
			name = file.replace('.bin', '').replace('_', ' ')
			dict[name] = self.rom_path + file

		return dict

class ArcadeView:

	def __init__(self, games):
		self.games = games

	def render(self, controller):
		self.controller = controller
		buttons = [urwid.Text(u'''   ___  _____________  ____  ________   ___  ____
  / _ \/ __/_  __/ _ \/ __ \/ ___/ _ | / _ \/ __/
 / , _/ _/  / / / , _/ /_/ / /__/ __ |/ // / _/  
/_/|_/___/ /_/ /_/|_|\____/\___/_/ |_/____/___/  
                                                 '''), urwid.Divider()]
		for g in self.games:
			button = urwid.Button(g, self.chosen, g)
			buttons.append(button)

		quit = urwid.Button(u'Exit', self.quit, 'exit')
		buttons.append(urwid.Divider())
		buttons.append(quit)
		listbox = urwid.ListBox(urwid.SimpleFocusListWalker(buttons))
		urwid.MainLoop(urwid.Padding(listbox, left=10, right=10)).run()

	def chosen(self, button, choice):
		self.controller.play(choice)

	def quit(self, button, choice):
		raise urwid.ExitMainLoop()

class ArcadeController:

	def __init__(self, games, view):
		self.games = games
		self.view = view

	def run(self):
		view.render(self)

	def play(self, game):
		subprocess.Popen([sys.argv[1], self.games[game]], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

games = ArcadeRoms(sys.argv[2]).get_games()
view = ArcadeView(games)
controller = ArcadeController(games, view)
controller.run()