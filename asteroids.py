
import defines
from defines import AST_INIT_SCALE, SCREEN_X, SCREEN_Y, ENTITY_ID, ENTITIES
from object_loader import loadObject, new_physic_object
from random import randint, choice
from panda3d.core import LPoint3

def spawnAsteroids(self, quantity):
    for i in range(quantity):
        asteroid = loadObject("asteroid%d.png" % (randint(1, 3)),
                              scale=defines.AST_INIT_SCALE, pos=LPoint3(23, 23))
        physic_debug, physic_body  = new_physic_object( shape='circle', 
                                                        scale=defines.AST_INIT_SCALE, 
                                                        pos=(randint(-20, 20), randint(-15, 15)))

        f = physic_body.GetWorldVector(localVector=( randint(-40,40), randint(-40,40) ))
        p = physic_body.GetWorldPoint(localPoint=(0.0, 0))
        physic_body.ApplyLinearImpulse(f, p, True)

        defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':"asteroid", 'NODE':asteroid, 'PHYSIC_NODE':physic_debug,'BODY':physic_body, 'SHIELD':100, 'ENERGY':0}
        defines.ENTITY_ID += 1

def break_asteroid(self, entity_id):
    number = randint(2, 3)
    i = 0
    while i < number:
        asteroid = loadObject("asteroid%d.png" % (randint(1, 3)),
                              scale=defines.AST_INIT_SCALE/number, pos=LPoint3(23, 23))
        physic_debug, physic_body  = new_physic_object( shape='circle', 
                                                        scale=defines.AST_INIT_SCALE/number, 
                                                        pos=defines.ENTITIES[entity_id]['BODY'].position)
      

        physic_body.linearVelocity.Set(defines.ENTITIES[entity_id]['BODY'].linearVelocity.x, defines.ENTITIES[entity_id]['BODY'].linearVelocity.y)
        physic_body.angularVelocity = defines.ENTITIES[entity_id]['BODY'].angularVelocity

        f = physic_body.GetWorldVector(localVector=( randint(-5,5), randint(-5,5) ))
        p = physic_body.GetWorldPoint(localPoint=(0.0, 0))
        physic_body.ApplyLinearImpulse(f, p, True)

        defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':"asteroid", 'NODE':asteroid, 'PHYSIC_NODE':physic_debug,'BODY':physic_body, 'SHIELD':20, 'ENERGY':0}
        defines.ENTITY_ID += 1

        i += 1