import defines
from object_loader import loadObject, new_physic_object
from Box2D import b2Vec2
from panda3d.core import LPoint3
from math import pi, cos, sin, sqrt, pow
from direct.task import Task
# from defines import AST_INIT_SCALE, SCREEN_X, SCREEN_Y, ENTITY_ID, ENTITIES
# from random import randint, choice

def init_planet(self, pos=(0,0)):
    planet = loadObject("planet0.png", scale=2, pos=LPoint3(0, 0))
    physic_debug, physic_body = new_physic_object( shape='circle', 
                                                    scale=2, 
                                                    pos=pos,
                                                    den=400.0)

    task = taskMgr.doMethodLater(0.5, animate_planet, 'animate planet', extraArgs=[planet, 0, defines.ENTITY_ID], appendTask=True)
    defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':"planet", 'NODE':planet, 
                'PHYSIC_NODE':physic_debug,'BODY':physic_body, 'SHIELD':999999, 'ENERGY':0, 'TASK': task}
    defines.ENTITY_ID += 1


def init_planet_logo(self, pos=LPoint3(0, 0)):
    planet = loadObject("planet0.png", scale=2, pos=LPoint3(0, 0))
    task = taskMgr.doMethodLater(0.5, animate_planet, 'animate planet', extraArgs=[planet, 0, defines.ENTITY_ID], appendTask=True)
    planet.reparentTo(render)
    planet.setPos(pos[0], 55, pos[1])
    defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':'menu_planet','NODE':planet,'BUTTON': None, 'TASK': task}
    defines.ENTITY_ID += 1

def planet_gravity():
    for entity_id, entity in defines.ENTITIES.items(): 
        if entity['CATEGORY'] != "planet":
            apply_planet_impulse(entity)

def apply_planet_impulse(entity):
    entity_body = entity["BODY"]
    entity_pos = entity["BODY"].position
    for planet_entity_id, planet_entity in defines.ENTITIES.items(): 
        if planet_entity['CATEGORY'] == "planet":
            planet_body = planet_entity['BODY']
            planet_pos = planet_body.position
            distance = sqrt(pow(entity_pos.x - planet_pos.x, 2) + pow(entity_pos.y-planet_pos.y, 2) ) +0.00001
            entity_mass = entity_body.fixtures[0].massData.mass + 1
            planet_mass = planet_body.fixtures[0].massData.mass + 1
            g = 6.674 * 0.0009
            accelleration = g * entity_mass * planet_mass / pow(distance,2) 
            x_vector = (planet_pos.x - entity_pos.x) * accelleration / distance
            y_vector = (planet_pos.y - entity_pos.y) * accelleration / distance
            f = b2Vec2(x_vector, y_vector)
            p = entity_body.GetWorldPoint(localPoint=(0.0, 0))
            entity_body.ApplyForce(f, p, True)
            # if  entity['CATEGORY'] == 'ship':
            #     print x_vector


def animate_planet(node, tick, entity_id, task):
    if tick == 0:
        tex_no = 0
    elif tick == 1:
        tex_no = 1
    elif tick == 2:
        tex_no = 2
    elif tick == 3:
        tex_no = 3
    elif tick == 4:
        tex_no = 4
    elif tick == 5:
        tex_no = 5
    elif tick == 6:
        tex_no = 5
    elif tick == 7:
        tex_no = 5
    elif tick == 8:
        tex_no = 6
    tex = loader.loadTexture("textures/planet%d.png" % tex_no)
    node.setTexture(tex, 1)
    tick += 1
    if tick > 8:
        tick = 0
    task = taskMgr.doMethodLater(0.5, animate_planet, 'animate planet', extraArgs=[node, tick, entity_id], appendTask=True)
    defines.ENTITIES[entity_id]['TASK'] = task
    return task.done