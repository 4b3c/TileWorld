import pygame
import constants as cts

# All these scenes extend the Scene class
from gui.main_menu import MainMenu
from gui.settings import Settings
from gui.game import Game
from gui.pause import Pause
from gui.selector import Selector
from gui.new_world import NewWorld

# Initialize pygame and pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")

# Create all the scenes
mainmenu = MainMenu()
selector = Selector()
settings = Settings()
game = Game("Weaven")
pause = Pause()
newworld = NewWorld()

scenes = {
	"Settings": settings,
	"Play": selector,
	"Resume": game,
	"Pause": pause,
	"New World": newworld
}

scene_traverse = [mainmenu] # A list of the traversed scenes to easily go to previous menus

while True:
	scene_traverse[-1].switching()
	next_scene = scene_traverse[-1].run(clock, window) # Each scene has a run function which loops until a scene change exits the function
	
	if (next_scene in scenes):
		scene_traverse.append(scenes[next_scene]) # In most cases just get the next scene using the dictionary

	elif (next_scene == "Main Menu"):
		scene_traverse = [mainmenu] # Clears the traverse list every time we get back to the main menu

	elif (next_scene == "Back"):
		scene_traverse.pop(-1) # Back just removes the last scene from the list so we effectively go to the previous scene/menu

	elif (next_scene == "Quit"):
		break # Quit exits the game

	elif (next_scene.startswith("Open ")): # Handling the game scene is a little tricky because it needs to know which world so we use "Open [filename]"
		if (scenes["Resume"].filename != next_scene.removeprefix("Open ")):
			scenes["Resume"] = Game(next_scene.removeprefix("Open "))
		next_scene = "Resume"
		scene_traverse.append(scenes[next_scene])
