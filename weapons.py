 
from physics import test_laser_collision
import defines
from object_loader import loadObject, new_physic_object
from Box2D import b2PolygonShape
from math import pi, cos, sin
from panda3d.core import LineSegs, NodePath, LVector3
from direct.task import Task


class weapon(object):

    def __init__(self):
        self.power = 100
        self.last_time_fired = globalClock.getRealTime()
        self.last_time_laser_fired = globalClock.getRealTime()
        self.reload_time = 0.5
        self.laser_reload_time = 0.3
        self.bullet_speed = 1.25
        self.bullet_density = 0.5

        # Creates a bullet and adds it to the bullet list
    def fire(self, panda3dworld, entity_id):
        now = globalClock.getRealTime()
        if now - self.last_time_fired < self.reload_time:
            if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
                panda3dworld.keys["fire"] = 0
            elif defines.ENTITIES[entity_id]['CATEGORY'] == 'ship2':
                panda3dworld.keys["p2fire"] = 0
        else:
            self.last_time_fired = now
            new_bullet = loadObject("bullet.png", scale=0.2)
            pos = defines.ENTITIES[entity_id]["BODY"].position
            angle = 360 - defines.ENTITIES[entity_id]["NODE"].getR() 
            pos_x = pos.x + 0.5 * cos(angle* pi/180)
            pos_y = pos.y + 0.5 * sin(angle* pi/180)

            if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
                category_bits = 0x0002
                mask_bits = (0x0001 | 0x0003)
            elif defines.ENTITIES[entity_id]['CATEGORY'] == 'ship2':
                category_bits = 0x0003
                mask_bits = (0x0001 | 0x0002)

            physic_debug, physic_body  = new_physic_object(shape='box', scale=0.2, is_a_bullet=True, pos=(pos_x,pos_y), 
                                                        category_bits=category_bits, mask_bits=mask_bits, den=self.bullet_density)
            # physic_debug.reparentTo(new_bullet)

            new_bullet.setPos(physic_body.position.x, 55, physic_body.position.y)
            physic_body.linearVelocity.Set(defines.ENTITIES[entity_id]['BODY'].linearVelocity.x, defines.ENTITIES[entity_id]['BODY'].linearVelocity.y)
            physic_body.angularVelocity = defines.ENTITIES[entity_id]['BODY'].angularVelocity

            f = physic_body.GetWorldVector(localVector=( self.bullet_speed * cos(angle* pi/180), self.bullet_speed * sin(angle* pi/180)))
            p = physic_body.GetWorldPoint(localPoint=(0.0, 0))
            physic_body.ApplyLinearImpulse(f, p, True)


            sound = base.loader.loadSfx("sounds/fire.ogg")
            sound.setVolume(0.5)
            sound.play()

            defines.ENTITIES[defines.ENTITY_ID] = {'CATEGORY':"bullet", 'EXPIRE': now + 3, 'NODE':new_bullet, 'PHYSIC_NODE':physic_debug ,'BODY':physic_body, 'SHIELD':0, 'ENERGY':0}
            defines.ENTITY_ID += 1
            defines.ENTITIES[entity_id]['ENERGY'] -= 20
            if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
                panda3dworld.keys["fire"] = 0
            elif defines.ENTITIES[entity_id]['CATEGORY'] == 'ship2':
                panda3dworld.keys["p2fire"] = 0


    def fire_laser(self, panda3dworld, entity_id):
        now = globalClock.getRealTime()
        if now - self.last_time_laser_fired < self.laser_reload_time:
            if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
                panda3dworld.keys["fire"] = 0
            elif defines.ENTITIES[entity_id]['CATEGORY'] == 'ship2':
                panda3dworld.keys["p2fire"] = 0
        else:
            self.last_time_laser_fired = now

            pos = defines.ENTITIES[entity_id]["NODE"].getPos()
            angle = 360 - defines.ENTITIES[entity_id]["NODE"].getR() 
            # print angle
            start_pos_x = pos.x + 0.5 * cos(angle* pi/180)
            start_pos_y = pos.z + 0.5 * sin(angle* pi/180)
            pos_x = pos.x + 10 * cos(angle* pi/180)
            pos_y = pos.z + 10 * sin(angle* pi/180)

            callback = test_laser_collision(start_pos_x, start_pos_y, pos_x, pos_y)
            if callback.hit:
                pos_x = callback.point.x
                pos_y = callback.point.y
                for contact_id, entity in defines.ENTITIES.items(): 
                    if entity['BODY'].fixtures[0] == callback.fixture:
                        if entity['CATEGORY'] == "ship" or entity['CATEGORY'] == "ship2" or entity['CATEGORY'] == "asteroid":
                            entity['SHIELD'] -= 10
                        elif entity['CATEGORY'] == "bullet":
                            defines.ENTITIES[contact_id]['NODE'].removeNode()
                            defines.ENTITIES[contact_id]['PHYSIC_NODE'].removeNode()
                            defines.world.DestroyBody(defines.ENTITIES[contact_id]['BODY'])
                            del defines.ENTITIES[contact_id]
            ls = LineSegs("lines")
            ls.setColor(1,1,1,1)
            ls.drawTo(start_pos_x, 55, start_pos_y)
            ls.drawTo(pos_x, 55, pos_y)
            laser = ls.create(False)
            laserPath = render.attachNewNode(laser)
            laserPath.setBin("unsorted", 0)
            laserPath.setDepthTest(False)


            sound = base.loader.loadSfx("sounds/laser.ogg")
            sound.setVolume(0.2)
            sound.play()
 
            taskMgr.doMethodLater(0.05, remove_laser_task, 'remove laser', extraArgs=[laserPath], appendTask=True)

            defines.ENTITIES[entity_id]['ENERGY'] -= 5
            if defines.ENTITIES[entity_id]['CATEGORY'] == 'ship':
                panda3dworld.keys["fire"] = 0
            elif defines.ENTITIES[entity_id]['CATEGORY'] == 'ship2':
                panda3dworld.keys["p2fire"] = 0


def remove_laser_task(laser, task):
    laser.removeNode()
    return task.done