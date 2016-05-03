#! /usr/bin/env python2
from panda3d.core import loadPrcFileData
from panda3d.core import WindowProperties, AntialiasAttrib, GeomNode, loadPrcFileData,  PStatClient
import defines
defines.init_defines() 

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
import sys

from object_loader import loadObject, add_button
from graphics import init_labels, update_graphics
from ship import init_ship
from asteroids import spawnAsteroids
from physics import init_physics, update_physics, get_contacts_list, manage_contacts
from panda3d.core import TextNode, CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay
from game_logic import update_game_logic
from planet import init_planet, init_planet_logo

#####################################################
#   Sounds from http://www.freesfx.co.uk
#   
#
#
#####################################################


class SSS_2D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        # self.setFrameRateMeter(True)
        wp = WindowProperties()
        wp.setSize(1280, 720)
        wp.setFullscreen(False)
        self.win.requestProperties(wp)
        self.disableMouse()

        # Load the background starfield.
        self.setBackgroundColor((0, 0, 0, 1))

        self.font = loader.loadFont('textures/inconsolata.egg')

        self.bg = loadObject("star_field.png", scale=73, depth=200,
                             transparency=False)
        self.bg.setTag('back_ground', '1')
        self.bg.setSx(73*16/9)
        # Load the ship and set its initial velocity. Create a ship entity

        self.keys = {   "turnLeft": 0, 
                        "turnRight": 0,
                        "accel": 0, 
                        "fire": 0,
                        "laser": 0,
                        "e_to_s": 0, 
                        "s_to_e": 0,
                        "cloak": 0,
                        "p2turnLeft": 0, 
                        "p2turnRight": 0,
                        "p2accel": 0, 
                        "p2fire": 0,
                        "p2laser": 0,
                        "e_to_s2": 0, 
                        "s_to_e2": 0,
                        "cloak2": 0,
                        "toggle_debug": 0,
                        "e_field": 0,
                        "e_field2": 0,
                        "mouse_l": 0,
                    }

        self.accept("escape", sys.exit)  # Escape quits
        # Other keys events set the appropriate value in our key dictionary
        self.accept("a",     self.setKey, ["turnLeft", 1])
        self.accept("a-up",  self.setKey, ["turnLeft", 0])
        self.accept("d",    self.setKey, ["turnRight", 1])
        self.accept("d-up", self.setKey, ["turnRight", 0])
        self.accept("w",       self.setKey, ["accel", 1])
        self.accept("w-up",    self.setKey, ["accel", 0])
        self.accept("f",       self.setKey, ["fire", 1])
        self.accept("f-up",    self.setKey, ["fire", 0])
        self.accept("h",       self.setKey, ["laser", 1])
        self.accept("h-up",    self.setKey, ["laser", 0])
        self.accept("r",          self.setKey, ["e_to_s", 1])
        self.accept("r-up",          self.setKey, ["e_to_s", 0])
        self.accept("t",          self.setKey, ["s_to_e", 1])
        self.accept("t-up",          self.setKey, ["s_to_e", 0])
        self.accept("s",              self.setKey, ["cloak", 1])
        self.accept("s-up",           self.setKey, ["cloak", 0])
        self.accept("g",              self.setKey, ["e_field", 1])
        self.accept("g-up",           self.setKey, ["e_field", 0])

        self.accept("arrow_left",     self.setKey, ["p2turnLeft", 1])
        self.accept("arrow_left-up",  self.setKey, ["p2turnLeft", 0])
        self.accept("arrow_right",    self.setKey, ["p2turnRight", 1])
        self.accept("arrow_right-up", self.setKey, ["p2turnRight", 0])
        self.accept("arrow_up",       self.setKey, ["p2accel", 1])
        self.accept("arrow_up-up",    self.setKey, ["p2accel", 0])

        # NUMPAD for p2
        self.accept("1",              self.setKey, ["p2fire", 1])
        self.accept("1-up",           self.setKey, ["p2fire", 0])
        self.accept("3",              self.setKey, ["p2laser", 1])
        self.accept("3-up",           self.setKey, ["p2laser", 0])
        self.accept("4",              self.setKey, ["e_to_s2", 1])
        self.accept("4-up",           self.setKey, ["e_to_s2", 0])
        self.accept("5",              self.setKey, ["s_to_e2", 1])
        self.accept("5-up",           self.setKey, ["s_to_e2", 0])
        self.accept("2",              self.setKey, ["e_field2", 1])
        self.accept("2-up",           self.setKey, ["e_field2", 0])
        # NO NUMPAD for p2
        self.accept("l",              self.setKey, ["p2fire", 1])
        self.accept("l-up",           self.setKey, ["p2fire", 0])
        self.accept("'",              self.setKey, ["p2laser", 1])
        self.accept("'-up",           self.setKey, ["p2laser", 0])
        self.accept("o",              self.setKey, ["e_to_s2", 1])
        self.accept("o-up",           self.setKey, ["e_to_s2", 0])
        self.accept("p",              self.setKey, ["s_to_e2", 1])
        self.accept("p-up",           self.setKey, ["s_to_e2", 0])
        self.accept(";",              self.setKey, ["e_field2", 1])
        self.accept(";-up",           self.setKey, ["e_field2", 0])


        self.accept("arrow_down",              self.setKey, ["cloak2", 1])
        self.accept("arrow_down-up",           self.setKey, ["cloak2", 0])

        self.accept("f1",             self.setKey, ["toggle_debug", 1])
        self.accept("mouse1",         self.setKey, ["mouse_l", 1])
        self.accept("mouse1-up",         self.setKey, ["mouse_l", 0])

        init_menu(self)
        self.gameTask = taskMgr.add(self.menuLoop, "gameLoop")
        

    def init_game(self, player1, player2, asteroids, planets):
        init_labels(self)
        init_physics()

        if player1 == True:
            init_ship(self, "ship.png")
        if player2 == True:
            init_ship(self, "ship2.png", player2=True)

        if planets == 1:
            init_planet(self, pos=(2,2))
       
        if asteroids == 1:
            asteroids = 10
        else:
            asteroids = 0

            # init_planet(self, pos=(2,2))
            # init_planet(self, pos=(-2,-2))
            # init_planet(self, pos=(12,8))
            # init_planet(self, pos=(-12,-8))

        spawnAsteroids(self, asteroids)

    def setKey(self, key, val):
        self.keys[key] = val

    def reset_game(self, task):
        defines.GAME_ONGOING = 0
        for entity_id, entity in defines.ENTITIES.items():
            if (entity['CATEGORY'] == 'ship' or entity['CATEGORY'] == 'ship2') and entity['E_FIELD_ENABLED'] == True:
                defines.world.DestroyBody(entity['E_FIELD_BODY'])
                entity['E_FIELD_DEBUG_NODE'].removeNode()
                entity['E_FIELD_NODE'].removeNode()
            try:
                taskMgr.remove(entity['TASK'])
            except:
                print "No task"
            try:
                defines.ENTITIES[entity_id]['NODE'].removeNode()
            except:
                print "No node"
            try:
                defines.ENTITIES[entity_id]['PHYSIC_NODE'].removeNode()
            except:
                print "No physic node"
            try:
                defines.world.DestroyBody(defines.ENTITIES[entity_id]['BODY'])
            except:
                print "No body"
            del defines.ENTITIES[entity_id]
        self.energy1.removeNode()
        self.shield1.removeNode()
        self.energy2.removeNode()
        self.shield2.removeNode()
        self.life_bar2.removeNode()
        self.life_bar.removeNode()
        self.energy_bar.removeNode()
        self.energy_bar2.removeNode()
        self.winner.removeNode()
        init_menu(self)
        self.gameTask = taskMgr.add(self.menuLoop, "gameLoop")
        return Task.done  

    def gameLoop(self, task):
        if defines.GAME_ONGOING == 0:
            return Task.done
        dt = globalClock.getDt()
        update_game_logic(self, dt)
        manage_contacts(dt)
        update_physics(dt)
        update_graphics(self)
        get_contacts_list()
        return Task.cont   

    def menuLoop(self, task):
        for entity_id, entity in defines.ENTITIES.items():
            if entity['CATEGORY'] == 'button':
                if entity['LABEL'] == 'planet':
                    if entity['STATUS'] == 1:
                        defines.PLANET_ON = 1
                    else:
                        defines.PLANET_ON = 0
                if entity['LABEL'] == 'asteroids':
                    if entity['STATUS'] == 1:
                        defines.ASTEROIDS_ON = 1
                    else:
                        defines.ASTEROIDS_ON = 0
                if entity['LABEL'] == 'exit' and entity['STATUS'] == 1:
                    sys.exit()
                if entity['LABEL'] == 'new_game' and entity['STATUS'] == 1:
                    for entity_id, entity in defines.ENTITIES.items():
                        if entity['CATEGORY'] == 'button':
                            entity['BUTTON'].destroy()
                        elif entity['CATEGORY'] == 'menu_planet':
                            taskMgr.remove(entity['TASK'])
                        entity['NODE'].removeNode()
                        del defines.ENTITIES[entity_id]
                    self.init_game(player1=True, player2=True, planets=defines.PLANET_ON, asteroids=defines.ASTEROIDS_ON)
                    defines.GAME_ONGOING = 1
                    defines.GAME_WON = 0
                    self.gameTask = taskMgr.add(self.gameLoop, "gameLoop")
                    return Task.done
        return Task.cont   

def init_menu(self):
    init_planet_logo(self, pos=(22,12))    

    
    add_button(self, "New Game", 'new_game', 0,0.5, width=0.5) # self, text, posx, posy, width, hight
    add_button(self, "Asteroids", 'asteroids', 0,0.3, width=0.5) # self, text, posx, posy, width, hight
    add_button(self, "Planet", 'planet', 0,0.1, width=0.5) # self, text, posx, posy, width, hight
    add_button(self, "Exit", 'exit', 0,-0.1, width=0.5) # self, text, posx, posy, width, hight


 

game = SSS_2D()
game.run()